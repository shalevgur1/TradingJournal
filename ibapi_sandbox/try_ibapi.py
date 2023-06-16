
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import threading
import time


# An implementaion of the EWrapper perant class.
# The EWrapper is a callback interface for the EClient
# that responsible (the EClient) for interacting with the
# IB server and call the relevant method in the EWrapper to handle
# the recieved data. Here I emplemnt callback methods and customize
# them to my needs
class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def tickPrice(self, reqId, tickType, price, attrib):
        # 2 represents Ask price, 67 represents delayed Ask price
        if tickType == 67 and reqId == 1:
            print('The current ask price is: ', price)


def run_loop():
    app.run()

app = IBapi()
app.connect('127.0.0.1', 7497, 123)

# Start the socket connection in a different thread
# to not interfir it in the main block of the script
# by other commands
socket_thread = threading.Thread(target=run_loop, daemon=True)
socket_thread.start()

time.sleep(1)   # Sleep interval to allow time for connection to server

app.reqMarketDataType(3) # Set Data stream to Delayed mode because do not have subscription for Live in paper account

#Create contract object
apl_contract = Contract()
apl_contract.symbol = 'AAPL'
apl_contract.secType = 'STK'
apl_contract.exchange = 'SMART'
apl_contract.currency = 'USD'

#Request Market Data
app.reqMktData(1, apl_contract, '', False, False, [])

time.sleep(5) #Sleep interval to allow time for incoming price data
app.disconnect()