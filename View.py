"""
COMP3005 FALL21
ERIC JONES 101113060

This module handles a lot of heavy lifting
regarding the UI and item lists/selections
"""
from math import *
from CommandFramework import Executor
from DatabaseFramework import objectify, Item, quote

"""
ListData:
    used for a base class for items that are part of a list.
    this allows them to have selections
"""
class ListData:

    selected = None

    """
    select:
        used when the user desires to make a selection
        from a given list. The selection is stored as
        a class variable 'selected'
    inputs:
        selected: the selected data object
    returns: True to ensure the list is closed after selection
    """
    def select(self, selected: dict) -> bool:
        self.selected = selected
        return True

"""
ItemView:
    used as a view for the DatabaseFramework's Item class.
    displays detailed information about the selected item.
    because actions can be taken on individual items, this
    class is itself inherited from Executor as well as ListItem
"""
class ItemView(Executor, ListData):

    """
    inputs:
        item: the DatabaseFramework Item type
        viewerFunc: the function used in the preamble
            to print the detailed info about the item
    """
    def __init__(self, item, viewerFunc=print):
        super().__init__()        
        self.item = item
        self.viewerFunc = viewerFunc
        
        #add the return function
        self.add_command("b", self.back, "back", "Returns to the item list")

    """
    preamble:
        [OVERRIDE]
        now prints detailed information about the item
    """
    def preamble(self):
        self.viewerFunc(self.selected)

    """
    select
        [OVERRIDE]
        sets the instance and starts the executor
        functionality when selected
    """
    def select(self, selected: dict):
        super().select(selected)
        self.start()

    """
    back:
        return function
    returns: True to ensure closure of this executor loop
    """
    def back(self, param):
        return True

"""
ListHandler:
    handles a list of ListData
"""
class ListHandler:
    
    """
    inputs:
        cols: the keys of the data to print
        per_page: the number of entries per page
    """
    def __init__(self,cols: list,per_page: int=5):
        self.columns = cols
        self.per_page = per_page
        self.page = 0
        self.count = 0

    """
    print_list:
        prints out the list of data, formatted nicely
    """
    def print_list(self):
        #list of column names to use
        columns = []
        #list of column indexes to use
        column_ids = []

        #print search results and columns, formatted nicely
        print("{0} results found | page {1} of {2}".format(self.count, self.page + 1, (self.count // self.per_page) + 1))
        #go through each column
        for i in range(len(self.items["columns"])):
            #get column
            col = self.items["columns"][i]

            #if columns is empty or col is in columns
            #add the current index/name to the list
            if self.columns is None or col in self.columns:
                column_ids.append(i)
                columns.append(col.upper().center(20))

        #add separater 
        print('   ' + '|'.join(columns))
        print('-' * (21 * len(columns) - 1))
        #go through the data
        for i in range(min(self.per_page, len(self.items["rows"]))):
            #get row  
            row = self.items["rows"][i]

            #generate formatted line based on values
            formatted  = []
            for j in range(len(row)):
                val = row[j]
                #only add value to list if its index matches
                #the ones determined above
                if j not in column_ids:
                    continue

                #format the string to fit the box
                fitted = str(val)
                if len(fitted) > 20:
                    fitted = val[:18] + ".."
                fitted = fitted.ljust(20)
                formatted.append(fitted)
            #print the current line
            print("{0}: ".format(i) + '|'.join(formatted))

        
        print('-' * (21 * len(columns) - 1))

    """
    refresh:
        placeholder for refreshing the data
    """
    def refresh(self):
        pass            

    """
    get_item:
        gets the nth item, placeholder
    inputs:
        index: the index in the current list
    returns: item at index'th position in the list
    """
    def get_item(self, index: int):
        return index

    """
    next_page:
        increments the current page index, then refreshes the data
    """
    def next_page(self, param):
        self.page = min(self.page + 1, ceil(self.count / self.per_page))
        self.refresh()

    """
    prev_page:
        decrements the current page index, then refreshes the data
    """
    def prev_page(self, param):
        self.page = max(0, self.page - 1)
        self.refresh()

"""
ItemListHandler:
    a child of List, intended specifically for listing Items.
    includes support for filtering
"""
class ItemListHandler(ListHandler):

    """
    inputs:
        item: the DatabaseFramework.Item database item
        per_page: the number of lines per page
    """
    def __init__(self, item, cols: list=None,per_page: int=5):
        super().__init__(cols, per_page)
        self.item = item

        #filters holds the conditions
        #to limit the SQL statement
        self.filters = []
        #temp filters represents the
        #temporary, user-submitted filters
        self.temp_filters = []

    """
        [OVERRIDE]
        refresh:
            updates items and count using the SQL functionality of the Item class
    """
    def refresh(self):
        self.items = self.item.get(self.get_filters(), (self.per_page,self.page * self.per_page))
        self.count = self.item.get_count(self.get_filters())

    """
    get_filters:
        combines temp and permanent filters into one list
    returns: all filters used on this list
    """
    def get_filters(self)-> list:
        return self.filters + self.temp_filters

    """
        [OVERRIDE]
    get_item:
        gets the nth item in the list
    inputs:
        index: the index in the list of the item to return
    """
    def get_item(self, index: int)-> dict:
        return objectify(self.items)[index]

"""
ListView:
    Contains generic support for lists using Executor functionality.
    Not exclusive to ItemList
"""
class ListView(Executor):

    """
    inputs:
        list_handler: ListHandler object that manages the list itself
        data_handler: ListData object
        filterable: determines if this list is filterable
        discreet: if yes, closes itself automatically once a selection returns
    """
    def __init__(self, list_handler, data_handler,filterable: bool=False, discreet:bool =False):
        super().__init__()
        self.list_handler = list_handler
        self.data_handler = data_handler
        self.discreet = discreet
       
        #add filter command if filterable
        if filterable:
            self.add_command('f', self.add_filter, "filt", "Filters results")

        #add back and select command
        self.add_command('b', self.back, "back", "Returns to menu")
        self.add_command('[0-9]+$', self.select_item, "<num>", "Selects items")

    """
        [OVERRIDE]
    preamble:
        handles the refreshing of data,
        as well as whether the next/previous page commands
        should be present based on the current page
    """
    def preamble(self):
        self.list_handler.refresh()

        #remove both commands to start
        #with a clean slate
        self.remove_command('n')
        self.remove_command('p')

        #if we aren't on the upper bound of pages, add the 'next' command back
        if self.list_handler.page < (self.list_handler.count // self.list_handler.per_page):
            self.add_command('n', self.list_handler.next_page, "next", "Goes to next page of results")

        #if we aren't on the lower bound of pages, add the 'prev' command back
        if self.list_handler.page > 0:
            self.add_command('p', self.list_handler.prev_page, "prev", "Goes to previous page of results")
        self.list_handler.print_list()

    """
        [OVERRIDE]
    select_item:
        handles item selection based on input param
    inputs:
        param: the input value from the command
    """
    def select_item(self, param):
        index = int(param)

        #bounds check
        if index >= 0 and index < self.list_handler.per_page:
            #set selected
            selected = self.list_handler.get_item(index)
            self.data_handler.select(selected)

            #close if discreet
            if self.discreet:
                return True
        else:
            input("selection out of range. hit enter to continue")

    """
    add_filter:
        adds filters to the SELECT statement. User selects a column,
        then inputs a value that column must equate to.
    """
    def add_filter(self, param):
        #create a list handler for the columns
        filter_printer = ListHandler(["columns"],10)
        #format the data for the list
        data = {"columns": ["columns"], "rows": [[x] for x in self.list_handler.columns]}
        filter_printer.items = data
        filter_printer.count = len(self.list_handler.columns)

        #selected item object
        filter_item = ListData()
        #create the filter view and start it
        filter_view = ListView(filter_printer, filter_item, False, True)
        filter_view.start()

        if filter_item.selected is None:
            return

        #get the column to filter by 
        filter_column = self.list_handler.columns[filter_item.selected]
        #get the value to set it to
        value = input("Search for {0} = ".format(filter_column))
        #if the value is not numerical,
        #add quotes around it
        if not value.isdigit():
            value = quote(value)

        #create the clause and add it to the list of filters
        clause = "{0} = {1}".format(filter_column, value)
        self.list_handler.temp_filters.append(clause)
        
        #add the 'clear filter' command
        self.add_command("c", self.clear_filter, "clear", "Clear the current filters")

    """
    clear_filter:
        quick function to remove all filters (and this command with it)
    """
    def clear_filter(self, param):
        self.list_handler.temp_filters = []
        self.remove_command("c")

    """
    back:
        closes the executor loop
    """
    def back(self, param):
        return True

"""
SelectorList:
    List specifically intended for use with selecting items
    from a list OR adding new ones    
"""
class SelectorList(ListView):

    """
    inputs:
        list_handler: ListHandler object that manages the list itself
        item_handler: ItemView object
        custom_data_columns: columns required when creating a new entry
    """
    def __init__(self, list_handler, data_handler, custom_data_columns: list):
        super().__init__(list_handler, data_handler, discreet=True)
        self.cdc = custom_data_columns
        #add command to create a new entry
        self.add_command('a', self.custom, "add", "Creates a new entry instead")

    """
    custom:
        adds a new entry to the database, then selects that one for use
    """
    def custom(self, param):
        data = []
        #loop through each column in the cdc
        for column in self.cdc:
            #get the value for the given column
            value = input("{0}: ".format(column))
            #if the value isnt numeric, wrap it in quotes
            if not value.isdigit():
                value = quote(value)
                
            #add that value to the data
            data.append(value)
            
        #write the entry to the database
        entry = self.list_handler.item.insert_value(self.cdc, data)
        #select the given item
        self.data_handler.select(entry)
        return False

              
