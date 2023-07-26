# Here is the main function of the application and the Entery Point.
# The next things are occuring in this file & JournalAppMain function:
# 1) The connection to the TWS (other IBAPI tool) is initialized
# 2) Here you can configure the application                             <Maybe will be in a json file in the future>
# 3) Used as the application Manager/Master
# 4) Transfers data between the IB api bridge to the journal manager
#

from ibapi_bridge import IbapiClientBridge # Bridge between the IB API and the application - save data in queue
from trade import Trade                    # The Trade class which includes every trades data
from journal_manager import JournalManager # The journal manager class which read and write to the Excel file
from converter import Converter            # Class for manipulating different data types (for ex. IBAPI, trades)

import time
import threading
import signal
import queue



# >>>>>>>>>> All variables configuration are here <<<<<<<<<<

# Socket network info - (ip - local because the system is local, port, id)
# TWS Port: 7497    IBGW Port: 4002    ID: 0 (Master Client ID set to 0)
CONNECTION_INFO = ('127.0.0.1', 7497, 0)
IBapiClient = IbapiClientBridge()

JournalManagerObj = JournalManager()
ConverterObj = Converter(JournalManagerObj)

QUEUE_RECIVE_TIME = 1       # Amount of time to queue to recive all data from IB Servers
APP_DELAY_TIME = 1          # Amount app delay time for better performence (Not sure)



# >>>>>>>>>> Not Configured Variables <<<<<<<<<<
running = True              # Run flag to synchronize the termination of all threads
threads = []                # List of all threads



def disconnect_IBClient():
    """
    Function to disconnect the IBClient in securely
    """
    try:
        IBapiClient.disconnect()
    except:
        print("IBClient has been already disconnected by different thread/process.")


def handle_termination(*args):
    """
    If was triggered by some signal args will include the signal (number) and frame (frame object) arguments
    """
    global running
    running = False
    disconnect_IBClient()
# Two signals for activate secure termination in application termination cenario.
signal.signal(signal.SIGINT, handle_termination)
signal.signal(signal.SIGTERM, handle_termination)

# Future Fiture: more commands in the console except "exit" command
def TypeExitLoop():
    """
    Wait for "exit" input in the main console for application termination.
    Terminats the application securly.
    Activated in a seperate thread.
    """
    while running:
        try:
            user_input = input("\nEnter a command (type 'exit' to end session):\n")
        except:
            break
        if user_input == 'exit':
            break
        time.sleep(APP_DELAY_TIME) #Sleep interval to allow time for incoming price data
    handle_termination()


def MainApplicationLoop():
    """
    The Main application loop. 
    Here all the base logic of the appliaction is running and the application is managed.
    The main part of the application.
    """
    
    while running:
        time.sleep(APP_DELAY_TIME)

        # Constantly check if new message entered the API data queue
        if(IBapiClient.q_has_data):
            time.sleep(QUEUE_RECIVE_TIME)   # If has data in queue sleep for some time to let the queue get all relevant trade data.

            messages = []
            while not IBapiClient.api_data.empty():
                api_data = IBapiClient.api_data.get()
                print(api_data)
                messages.append(api_data)
            IBapiClient.q_has_data = False

            t = ConverterObj.IBAPI_to_trade(messages)
            print(t)
            JournalManagerObj.write_trade(t)




    handle_termination()


def JournalAppMain():
    """
    Entry point of the code.
    Build, Waits and starts all the threads from here.
    """
    global threads

    # Build all threads
    main_thread = threading.Thread(target=MainApplicationLoop, name="MainLoop")
    threads.append(main_thread)
    type_exit_thread = threading.Thread(target=TypeExitLoop, name="ExitLoop")
    threads.append(type_exit_thread)
    
    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish and terminate the application at the end
    for thread in threads:
        thread.join()
    handle_termination()


if __name__ == '__main__':
    
    # print([item.strip() for item in string1.split(',')])
    # j = JournalManager()
    # t = Trade(j, )
    # print(t.trade_attr_tostring())

    # Start the socket connection in a different thread
    # to not interfir it in the main block of the script
    # by other commands
    ip, port, id = CONNECTION_INFO
    IBapiClient.connect(ip, port, id)
    IBapiClient.run()

    # Put main in a try block to enable disconnecting the socket if an error ocures
    try:
        JournalAppMain()
    except:
        handle_termination()