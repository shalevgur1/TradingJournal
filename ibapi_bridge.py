"""
Orders in IBAPI are related each to a specific client that is responsible for them and 
that have created them. Important points:

(without invoking reqOpenOrders or reqAllOpenOrders)
* Clients with the ID of the client submitting the order will receive order status messages indicating changes in the order status.
* The client with Master Client ID (set in TWS/IBG) will receive order status messages for all clients.
* Client ID 0 will receive order status messages for its own (client ID 0) orders and also for orders submitted manually from TWS.

* There are not guaranteed to be orderStatus callbacks for every change in order status.
  For this reason, it is good to monitor 'execDetails' function in the EWrapper in addition for 'orderStatus'.
* 'execDetails' is called only if an order is filled either fully or partially.
"""


from ibapi.client import EClient
from ibapi.common import OrderId
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.order_state import OrderState
from ibapi.execution import Execution
from ibapi.execution import ExecutionFilter

import queue
import threading
import time


# An implementaion of the EWrapper perant class.
# The EWrapper is a callback interface for the EClient
# that responsible (the EClient) for interacting with the
# IB server and call the relevant method in the EWrapper to handle
# the recieved data. Here I emplemnt callback methods and customize
# them to my needs
class IbapiClientBridge(EWrapper, EClient):

    api_data = queue.Queue()

    def __init__(self):
        EClient.__init__(self, self)

    def connect(self, host, port, clientId):
        # Here only to generate interface to the parent conect function
        return super().connect(host, port, clientId)
    
    def run(self):
        # Override function for the client run function for
        # Start the socket connection in a different thread.
        # This wont interfir to the main block of the script
        socket_thread = threading.Thread(target=lambda: super().run(), daemon=True)
        socket_thread.start()
        time.sleep(1)   # Sleep interval to allow time for connection to server



    def orderStatus(self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float):
        print("\norderStatus")
        print("OrderId: " + orderId)
        print("Status: " + status)
        print("filled: " + filled)
        print("remaining: " + remaining)
        print("avgFillPrice: " + avgFillPrice)
        print("permId: " + permId)
        print("parentId: " + parentId)
        print("lastFillPrice: " + lastFillPrice)
        print("clientId: " + clientId)
        print("whyHeld: " + whyHeld)
        print("mktCapPrice: " + mktCapPrice)
        #print(orderId, status, filled, remaining, avgFillPrice, permId, parentId, lastFillPrice, clientId, whyHeld, mktCapPrice)
        pass

    def openOrder(self, orderId:OrderId, contract:Contract, order:Order, orderState:OrderState):
        print("\nopenOrder")
        print("OrderId: " + orderId)
        print("Contract: " + contract)
        print("Order: " + order)
        print("OrderState: " + orderState)
        print('\n')
        #print(orderId, contract, order, orderState)
        pass

    def execDetails(self, reqId:int, contract:Contract, execution:Execution):
        #print("execDetails")
        #print(reqId, contract, execution)
        pass
        
    def execDetailsEnd(self, reqId: int):
        #print("ExecDetailsEnd. ReqId:", reqId)
        pass

    def putApiData(self, data):
        self.api_data.put(data)

    def getApiData(self):
        self.api_data.get()






"""
def main():

    IBClient.reqMarketDataType(3) # Set Data stream to Delayed mode because do not have subscription for Live in paper account

    #Create contract object
    apl_contract = Contract()
    apl_contract.symbol = 'AAPL'
    apl_contract.secType = 'STK'
    apl_contract.exchange = 'SMART'
    apl_contract.currency = 'USD'

    #Request Market Data - example
    #IBClient.reqMktData(1, apl_contract, '', False, False, [])
    
    #Request Open Orders - example - Not needed if is Master Client 
    #IBClient.reqOpenOrders()

    #Request excecutions - only for filled or part filled orders
    #ex_filter = ExecutionFilter()
    #IBClient.reqExecutions(1, ExecutionFilter())

    while True:
        user_input = input("\nEnter a command (type 'exit' to end session):\n")
        if user_input == 'exit':
            break
        time.sleep(1) #Sleep interval to allow time for incoming price data
    IBClient.disconnect()


"""