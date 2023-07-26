from trade import Trade
from journal_manager import JournalManager
from ibapi_bridge import MessageType

from datetime import datetime
import yfinance as yf

class Converter:
    """
    This class is used for convert between different data types.
    
    Convert types:
    IBAPI - Trade objects
    """

    journal_manager = None      # The corresponding JournalManager object

    def __init__(self, journal_manager:JournalManager):
        """
        Initialize the converter with the relevant JournalManager object
        """
        self.journal_manager = journal_manager

    def _get_current_time(self):
        """
        Returns the current time and date in a format relevant to the 
        Trading Journal format:
        tuple (Date:str, Time:str)
        """
        t = datetime.now()
        return (str(t.day) + '/' + str(t.month) + '/' + str(t.year), str(t.hour) + ':' + str(t.minute))

    def IBAPI_to_trade(self, messages, trade:Trade=None):
        """
        Converts IBAPI data (messages) to Trade objects.
        Return the new-created/modified Trade object.
        """

        if not trade:   # trade argument not given
            trade = Trade(self.journal_manager)

        # Check if LONG/SHORT entering new position message (should include 3 messages)
        if(len(messages) == 3):
            if messages[0][0] == MessageType.OPEN_ORDER:
                
                # Set next attributes:
                # Name Shortcut, Stock Exchange, Transmission Date and Time, Full Company Name, Stock Sector
                trade.Name_Shortcut = messages[0][2].symbol
                trade.Stock_Exchange = messages[0][2].exchange
                trade.Transmission_Date.Date, trade.Transmission_Date.Time = self._get_current_time()

                ticker = yf.Ticker(messages[0][2].symbol)
                trade.Stock = ticker.info["longName"]            # Gest the stock's company full name from Yahoo Finance
                trade.Sector = ticker.info["sector"]             # Gets the stock sector from Yahoo Finance

                # Find deal type (LONG/SHORT - Market/Stop/Limit)
                # And set The next attributes
                # Position, Order Type, Stocks Amount, Transmit Price, TakeProfit Price
                buy_orders = []
                sell_orders = []
                for message in messages:
                    if message[3].action == 'BUY':
                        buy_orders.append(message[3])
                    else:
                        sell_orders.append(message[3])
                if len(buy_orders) == 1:
                    # LONG deal attributes
                    trade.Entery.Position = 'LONG'
                    trade.Entery.Order_Type = "Buy " + buy_orders[0].orderType
                    if buy_orders[0].orderType == 'MKT':
                        trade.Entery.Transmit_Price = round(ticker.history(interval="1d")["Close"].iloc[-1], 2) # Gets the latest price - round it until 2 after decimal point
                    else:
                        trade.Entery.Transmit_Price = buy_orders[0].lmtPrice
                    trade.Entery.Amount = buy_orders[0].totalQuantity
                    for sell_order in sell_orders:
                        if sell_order.orderType == 'LMT':
                            trade.Take_Profit.Price = sell_order.lmtPrice
                        elif sell_order.orderType == 'STP':
                            trade.Stop_Loss.Price = sell_order.auxPrice
                else:
                    # Short deal attributes
                    trade.Entery.Position = 'SHORT'
                    trade.Entery.Order_Type = "Sell " + sell_orders[0].orderType
                    if buy_orders[0].orderType == 'MKT':
                        trade.Entery.Transmit_Price = round(ticker.history(interval="1d")["Close"].iloc[-1], 2) # Gets the latest price - round it until 2 after decimal point
                    else:
                        trade.Entery.Transmit_Price = buy_orders[0].lmtPrice
                    trade.Entery.Amount = sell_orders[0].totalQuantity
                    for buy_order in buy_orders:
                        if buy_order.orderType == 'LMT':
                            trade.Take_Profit.Price = buy_order.lmtPrice
                        elif buy_order.orderType == 'STP':
                            trade.Stop_Loss.Price = buy_order.auxPrice
                            
        return trade
