# Here is the main function of the application and the Entery Point.
# The next things are occuring in this file & JournalAppMain function:
# 1) The connection to the TWS (other IBAPI tool) is initialized
# 2) Here you can configure the application                             <Maybe will be in a json file in the future>
# 3) Used as the application Manager/Master
# 4) Transfers data between the IB api bridge to the journal manager
#

from ibapi_bridge import IbapiClientBridge # Bridge between the IB API and the application - save data in queue

import time
import threading
import signal



# >>>>>>>>>> All variables configuration are here <<<<<<<<<<

# Socket network info - (ip - local because the system is local, port, id)
# TWS Port: 7497    IBGW Port: 4002    ID: 0 (Master Client ID set to 0)
CONNECTION_INFO = ('127.0.0.1', 7497, 0)
IBapiClient = IbapiClientBridge()




# >>>>>>>>>> Not Configured Variables <<<<<<<<<<
running = True              # Run flag to synchronize the termination of all threads
threads = []                # List of all threads



def disconnect_IBClient():
    """
    Function to disconnect the IBClient in securely
    """
    try:
        IbapiClientBridge.disconnect()
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
    print("\nEnter a command (type 'exit' to end session):\n")
    while running:
        user_input = input("\nEnter a command (type 'exit' to end session):\n")
        if user_input == 'exit':
            break
        time.sleep(1) #Sleep interval to allow time for incoming price data
    handle_termination()


def MainApplicationLoop():
    """
    The Main application loop. 
    Here all the base logic of the appliaction is running and the application is managed.
    The main part of the application.
    """
    while running:
        time.sleep(1)
    handle_termination()


def JournalAppMain():
    """
    Entry point of the code.
    Build, Waits and starts all the threads from here.
    """
    global threads

    # Build all threads
    main_thread = threading.Thread(target=MainApplicationLoop)
    threads.append(main_thread)
    type_exit_thread = threading.Thread(target=TypeExitLoop)
    threads.append(type_exit_thread)
    
    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish and terminate the application at the end
    for thread in threads:
        thread.join()
    handle_termination()


if __name__ == '__main__':
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