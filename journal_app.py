# Here is the main function of the application and the Entery Point.
# The next things are occuring in this file & JournalAppMain function:
# 1) The connection to the TWS (other IBAPI tool) is initialized
# 2) Here you can configure the application                             <Maybe will be in a json file in the future>
# 3) Used as the application Manager/Master
# 4) Transfers data between the IB api bridge to the journal manager
#

from ibapi_bridge import IbapiClientBridge # Bridge between the IB API and the application - save data in queue

import time



# >>>>>>>>>> All variables configuration are here <<<<<<<<<<

# Socket network info - (ip - local because the system is local, port, id)
# TWS Port: 7497    IBGW Port: 4002    ID: 0 (Master Client ID set to 0)
CONNECTION_INFO = ('127.0.0.1', 7497, 0)
IBapiClient = IbapiClientBridge()





def JournalAppMain():
    while True:
        user_input = input("\nEnter a command (type 'exit' to end session):\n")
        if user_input == 'exit':
            break
        time.sleep(1) #Sleep interval to allow time for incoming price data
    IbapiClientBridge.disconnect()


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
        IBapiClient.disconnect()