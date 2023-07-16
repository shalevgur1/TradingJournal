
from journal_manager import JournalManager
from ibapi_bridge import MessageType
from datetime import datetime
import yfinance as yf


class Trade:
    # * All trade properties are string *

    trade_fields_attr = {}               # A dict that contains all the fields of a trade taken from Trade Log sheet
    journal_manager = None               # The Journal Manager object that handles all the interaction with the Journal

    def __init__(self, manager:JournalManager, messages:list = None, **kwargs):
        """
        Can give how many arguments that you want but arguments must
        be fields in the Trade_Log that has no sub-fields.
        To set a sub-field, give the values to the properties after the
        creation of an instance of trade object.

        Requiered:
        # manager:JournalManager

        Optional:
        Initialize a trade with API message data.
        Gets a message from the type of list (like the output message from the ibapi_bridge)
        and create a trade according to the message type.  
        # message:list
        """
        
        # Setting exist and given Journal Manager
        self.journal_manager = manager

        # Gets Journal Fields from given Journal Manager
        self.trade_fields_attr = self.journal_manager.trade_fields

        # Replace all given fields name to a valid attributes name
        self._make_valid_attr_name()

        # Creates the Trade object attributes by Trade Log table fields
        self._set_attributes(kwargs)

        # Set trade values according to an API message if initialized with API message
        if(messages):
            self._set_attributes_message(messages)

    

    def _set_attributes_message(self, messages):
        # Check if LONG/SHORT message (should include 3 messages)
        if(len(messages) == 3):
            if messages[0][0] == MessageType.OPEN_ORDER:
                
                # Set next attributes:
                # Name Shortcut, Stock Exchange, Transmission Date and Time, Full Company Name, Stock Sector
                self.Name_Shortcut = messages[0][2].symbol
                self.Stock_Exchange = messages[0][2].exchange
                self.Transmission_Date.Date, self.Transmission_Date.Time = self._get_current_time()

                ticker = yf.Ticker(messages[0][2].symbol)
                self.Stock = ticker.info["longName"]            # Gest the stock's company full name from Yahoo Finance
                self.Sector = ticker.info["sector"]             # Gets the stock sector from Yahoo Finance

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
                    self.Entery.Position = 'LONG'
                    self.Entery.Order_Type = "Buy " + buy_orders[0].orderType
                    if buy_orders[0].orderType == 'MKT':
                        self.Entery.Transmit_Price = round(ticker.history(interval="1d")["Close"].iloc[-1], 2) # Gets the latest price - round it until 2 after decimal point
                    else:
                        self.Entery.Transmit_Price = buy_orders[0].lmtPrice
                    self.Entery.Amount = buy_orders[0].totalQuantity
                    for sell_order in sell_orders:
                        if sell_order.orderType == 'LMT':
                            self.Take_Profit.Price = sell_order.lmtPrice
                else:
                    # Short deal attributes
                    self.Entery.Position = 'SHORT'
                    self.Entery.Order_Type = "Sell " + sell_orders[0].orderType
                    if buy_orders[0].orderType == 'MKT':
                        self.Entery.Transmit_Price = round(ticker.history(interval="1d")["Close"].iloc[-1], 2) # Gets the latest price - round it until 2 after decimal point
                    else:
                        self.Entery.Transmit_Price = buy_orders[0].lmtPrice
                    self.Entery.Amount = sell_orders[0].totalQuantity
                    for buy_order in buy_orders:
                        if sell_order.orderType == 'LMT':
                            self.Take_Profit.Price = sell_order.lmtPrice

    def _set_attributes(self, kwargs):
        """
        Creates the Trade object attributes by Trade Log table fields
        Using a given dictionary of fields from the manager object.
        Using given values and keys for attributes as argument.
        """
        for field_key, field_value in self.trade_fields_attr.items():

            if field_value is None:
                # No sub-fields
                setattr(self, field_key, None)
                for given_key, given_value in kwargs.copy().items():
                    if given_key == field_key:
                        setattr(self, field_key, given_value)
                        del kwargs[given_key]
                        break
            else:
                # Has sub-fields, need to create sub-classes
                temp_dict = {}
                for sub_field in field_value:
                    has_value = False
                    for given_key, given_value in kwargs.copy().items():
                        if given_key == sub_field:
                            temp_dict[sub_field] = given_value
                            del kwargs[given_key]
                            has_value = True
                    if not has_value:
                        temp_dict[sub_field] = None
                setattr(self, field_key, type(field_key, (), temp_dict))

        # Check if there is extra not valid given arguments for not existing attributes
        if kwargs:
            temp_str = ''
            for given_key, given_value in kwargs:
                temp_str = temp_str + given_key + ' '
            raise ValueError("No such fields in Trade Log Table - Not existing attributes: " + temp_str)

    def _make_valid_attr_name(self):
        """
        Replace all given fields name to a valid attributes name
        """

        temp_dict = {}
        temp_list = []

        for field_key, field_value in self.trade_fields_attr.items():
            # Replace all not valid characters in fields names to valid ones
            field_key = field_key.replace(" ", "_").replace("%", "perce").replace("/", "")

            if field_value:
                for sub_field in field_value:
                    # Replace all not valid characters in fields names to valid ones
                    sub_field = sub_field.replace(" ", "_").replace("%", "perce").replace("/", "")
                    temp_list.append(sub_field)
                temp_dict[field_key] = temp_list
                temp_list = []
            else:
                temp_dict[field_key] = None

        self.trade_fields_attr = temp_dict

    def trade_attr_tostring(self):
        """
        Creates a string from Trade arguments names.
        Using the trade_fields_attr Dictionary.
        """
        fields_str = ''
        for key, value in self.trade_fields_attr.items():
            fields_str = fields_str + key
            if value is not None:
                fields_str = fields_str + ': | '
                for sub_val in self.trade_fields_attr[key]:
                    fields_str = fields_str + sub_val + ' | '
            fields_str = fields_str + '\n'

        return fields_str
    
    def _get_current_time(self):
        """
        Returns the current time and date in a format relevant to the 
        Trading Journal format:
        tuple (Date:str, Time:str)
        """
        t = datetime.now()
        return (str(t.day) + '/' + str(t.month) + '/' + str(t.year), str(t.hour) + ':' + str(t.minute))
    
    @classmethod
    def _get_class_attr(cls):
        """
        Returns the attributes names of the Trade class
        which can change according to the Trading Journal Excel file
        Excludes methods, dunder methods and internal (private) attributes
        """
        attributes = [attr for attr in dir(cls) if not callable(getattr(cls, attr)) and not attr.startswith("_")]
        return attributes
    
    def __str__(self):
        """
        String creator function to generate a string from 
        the current trade istance with all attributes according to
        the Trading Journal Excel file (which set at the __init__)
        """
        trade_str = ""
        for attr, value_or_subattr in self.trade_fields_attr.items():
            trade_str += attr + ': '
            if not value_or_subattr:
                trade_str += str(getattr(self, attr))
            else:
                for sub_attr in value_or_subattr:
                    trade_str += sub_attr + '-' + str(getattr(getattr(self, attr), sub_attr)) + ' | '
                trade_str  = trade_str[:-3]
            trade_str += '\n'
        return trade_str