
from journal_manager import JournalManager


class Trade:
    # * All trade properties are string *

    trade_fields_attr = {}               # A dict that contains all the fields of a trade taken from Trade Log sheet
    journal_manager = None               # The Journal Manager object that handles all the interaction with the Journal


    def __init__(self, manager, **kwargs):
        """
        Can give how many arguments that you want but arguments must
        be fields in the Trade_Log that has no sub-fields.
        To set a sub-field, give the values to the properties after the
        creation of an instance of trade object.
        """

        # Setting exist and given Journal Manager
        self.journal_manager = manager

        # Gets Journal Fields from given Journal Manager
        self.trade_fields_attr = self.journal_manager.trade_fields

        # Replace all given fields name to a valid attributes name
        self._make_valid_attr_name()
        # Creates the Trade object attributes by Trade Log table fields
        self._set_attributes(kwargs)


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

    # Replace all given fields name to a valid attributes name
    def _make_valid_attr_name(self):

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

    # Creates a string from Trade arguments names.
    # Using the trade_fields_attr Dictionary.
    def trade_attr_tostring(self):
        fields_str = ''
        for key, value in self.trade_fields_attr.items():
            fields_str = fields_str + key
            if value is not None:
                fields_str = fields_str + ': | '
                for sub_val in self.trade_fields_attr[key]:
                    fields_str = fields_str + sub_val + ' | '
            fields_str = fields_str + '\n'

        return fields_str
