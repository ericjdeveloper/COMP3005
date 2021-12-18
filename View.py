import sqlite3
from math import *
from CommandFramework import Executor
from DBHelper import objectify, Item, quote

class ListItem:

    def select(self, selected):
        self.selected = selected
        return True


class ItemView(Executor, ListItem):

    def __init__(self, item, viewerFunc=print, instance=None):
        super().__init__()
        self.item = item
        self.instance = instance
        self.viewerFunc = viewerFunc
        self.add_command("b", self.back, "back", "Returns to the item list")

    def preamble(self):
        self.viewerFunc(self.instance)

    def select(self, selected):
        self.setInstance(selected)
        self.start()

    def setInstance(self, instance):
        self.instance = instance

    def back(self, param):
        return True

class ListPrinter:
    def __init__(self,cols,per_page=5):
        self.columns = cols
        self.per_page = per_page
        self.page = 0
        self.count = 0

    def printList(self):
        columns = []
        column_ids = []
        
        print("{0} results found | page {1} of {2}".format(self.count, self.page + 1, (self.count // self.per_page) + 1))
        for i in range(len(self.items["columns"])):
            col = self.items["columns"][i]
            if self.columns is None or col in self.columns:
                column_ids.append(i)
                columns.append(col.upper().center(20))

            
        print('   ' + '|'.join(columns))
        print('-' * (21 * len(columns) - 1))
        for i in range(min(self.per_page, len(self.items["values"]))):
              row = self.items["values"][i]
              formatted  = []
              for j in range(len(row)):
                  val = row[j]
                  if j not in column_ids:
                      continue
                  formatted.append(str(val).ljust(20))

              print("{0}: ".format(i) + '|'.join(formatted))
        print('-' * (21 * len(columns) - 1))

    def refresh(self):
        pass            
    
    def getItem(self, index):
        return index

    def nextPg(self, param):
        self.page = min(self.page + 1, ceil(self.count / self.per_page))
        self.refresh()
        
    def prevPg(self, param):
        self.page = max(0, self.page - 1)
        self.refresh()

    def getMin(self):
        return self.page * self.per_page

    def getMax(self):
        return min((self.page + 1) * self.per_page, self.per_page)

class ItemPrinter(ListPrinter):

    def __init__(self, item, cols=None,per_page=5):
        super().__init__(cols, per_page)
        self.item = item
        self.filters = []

    def refresh(self):
        self.items = self.item.get(self.filters, (self.per_page,self.page * self.per_page))
        self.count = self.item.getCount(self.filters)

    def getItem(self, index):
        return objectify(self.item.get(self.filters, (self.per_page, self.page)))[index]

class ListView(Executor):

    def __init__(self, listPrinter, itemView,filterable=False, discreet=False):
        super().__init__()
        self.listPrinter = listPrinter
        self.itemViewer = itemView
        self.discreet = discreet
        if filterable:
            self.add_command('f', self.add_filter, "filt", "Filters results")
        self.add_command('b', self.back, "back", "Returns to menu")
        self.add_command('[0-9]+$', self.select, "<num>", "Selects items")

    def preamble(self):
        self.listPrinter.refresh()
        self.remove_command('n')
        self.remove_command('p')
        if self.listPrinter.page < (self.listPrinter.count // self.listPrinter.per_page):
            self.add_command('n', self.listPrinter.nextPg, "next", "Goes to next page of results")
            
        if self.listPrinter.page > 0:
            self.add_command('p', self.listPrinter.prevPg, "prev", "Goes to previous page of results")
        self.listPrinter.printList()

    def select(self, param):
        index = int(param)
        if index >= self.listPrinter.getMin() and index < self.listPrinter.getMax():
            selected = self.listPrinter.getItem(index)

            closed = self.itemViewer.select(selected)
            if self.discreet:
                return True
        else:
            input("selection out of range. hit enter to continue")

    def add_filter(self, param):

        filterPrinter = ListPrinter(["columns"],10)
        data = {"columns": ["columns"], "values": [[x] for x in self.listPrinter.columns]}
        filterPrinter.items = data
        filterPrinter.count = len(self.listPrinter.columns)
        filter_item = ListItem()
        filterView = ListView(filterPrinter, filter_item, False, True)
        filterView.start()
        filter_column = self.listPrinter.columns[filter_item.selected]
        value = input("Search for {0} = ".format(filter_column))
        if not value.isdigit():
            value = quote(value)
        clause = "{0} = {1}".format(filter_column, value)
        self.listPrinter.filters.append(clause)

        self.remove_command("c")
        self.add_command("c", self.clear_filter, "clear", "Clear the current filters")

    def clear_filter(self, param):
        self.listPrinter.filters = []
        self.remove_command("c")

    def back(self, param):
        return True

class SelectorList(ListView):
    def __init__(self, listPrinter, itemView, customDataColumns):
        super().__init__(listPrinter, itemView, discreet=True)
        self.CDC = customDataColumns
        self.add_command('a', self.custom, "add", "Creates a new entry instead")

    def custom(self, param):
        data = []
        for column in self.CDC:
            value = input("{0}: ".format(column))
            if not value.isdigit():
                value = quote(value)
            data.append(value)
        entry = self.listPrinter.item.insertValue(self.CDC, data)
        self.itemViewer.select(entry)
        return True

              
