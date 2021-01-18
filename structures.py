import tkinter
import sqlite3


# creates a listbox with a scroll bar
class ScrollBox(tkinter.Listbox):

    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs)

        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    def grid(self, row, column, sticky='nsw', rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs)
        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan)
        self['yscrollcommand'] = self.scrollbar.set


# makes list boxes that update and can be controlled by other list boxes
class DataListBox(ScrollBox):

    def __init__(self, window, connection, table, field, sort_order=(), **kwargs):
        super().__init__(window, **kwargs)

        self.linked_box = None
        self.link_field = None
        self.link_value = None
        self.link_car = None

        self.cursor = connection.cursor()
        self.table = table
        self.field = field

        self.bind("<<ListboxSelect>>", self.get_select)

        self.sql_select = "SELECT " + self.field + ", _id FROM " + self.table
        if sort_order:
            self.sql_sort = " ORDER BY " + ",".join(sort_order)
        else:
            self.sql_sort = " ORDER BY " + self.field

    def clear(self):
        # clears the listbox
        self.delete(0, tkinter.END)

    def link(self, widget, link_field):
        # links box to the output(link_field) of another listbox(widget)
        self.linked_box = widget
        widget.link_field = link_field

    def car_link(self, car):
        # links box to a car object
        self.link_car = car

    def re_query(self, link_value=None):
        self.link_value = link_value

        # selects all values in the sql table that match link_value in the link-field attribute and sorts them
        if link_value and self.link_field:
            sql = self.sql_select + " WHERE " + self.link_field + " = ?" + self.sql_sort
            self.cursor.execute(sql, (link_value,))
        else:
            self.cursor.execute(self.sql_select + self.sql_sort)

        # clears the box of previous contents
        self.clear()

        # populates the box with items
        for value in self.cursor:
            self.insert(tkinter.END, value[0])

        # clears the box that is linked to this box, if one exists
        if self.linked_box:
            self.linked_box.clear()

    def get_select(self, event):

        if self.curselection() != ():
            # gets index of selected item
            index = self.curselection()[0]  # throws index error for some reason, doesnt affect functionality
            # gets value of selected item
            value = self.get(index),
            print(index)

            if self.linked_box:
                # if there is a value selected from the controlling box
                if self.link_value:
                    value = value[0], self.link_value
                    sql_where = " WHERE " + self.field + " = ? AND " + self.link_field + " = ?"
                else:
                    sql_where = " WHERE " + self.field + " = ?"

                link_id = self.cursor.execute(self.sql_select + sql_where, value).fetchone()[1]
                self.linked_box.re_query(link_id)
            else:
                print("no linked box")

            if self.link_car:
                # if the box has a linked car update it
                self.link_car.update_car(index, value)


# class to hold information for current car
class Car(object):

    def __init__(self, ma='beans', mo='beans', no='beans', st=1, en=2, inf='beans'):
        # actual variables
        self.make = ma
        self.model = mo
        self.notes = no
        self.start = st
        self.end = en
        self.info = inf

        # for use with links
        self.cursor = None
        self.make_box = None
        self.model_box = None
        self.notes_box = None
        self.start_box = None
        self.end_box = None
        self.info_box = None

    def link_boxes(self, make, model, notes, start, end, info):
        # link car object to Entry objects to show data
        self.make_box = make
        self.model_box = model
        self.notes_box = notes
        self.start_box = start
        self.end_box = end
        self.info_box = info

    def update_car(self, index, value=None):
        # function that updates fields with info on current car
        conn = sqlite3.connect("carInfo.sqlite")
        self.cursor = conn.cursor()

        if value:
            # get all that good stuff from the sql library
            make_id = "SELECT make FROM modelList where model = " + value[0]
            self.cursor.execute(make_id)
            make_id = self.cursor.fetchall()[0][0]

            self.make = "SELECT make FROM makeList WHERE _id = " + make_id
            self.cursor.execute(self.make)
            self.make = self.cursor.fetchall()[0][0]

            self.model = "SELECT model FROM modelList WHERE model = " + value[0]
            self.cursor.execute(self.model)
            self.model = self.cursor.fetchall()

            self.notes = "SELECT notes FROM modelList WHERE model = " + value[0]
            self.cursor.execute(self.notes)
            self.notes = self.cursor.fetchall()[0][0]

            self.start = "SELECT start FROM modelList WHERE model = " + value[0]
            self.cursor.execute(self.start)
            self.start = self.cursor.fetchall()[0][0]

            self.end = "SELECT end FROM modelList WHERE model = " + value[0]
            self.cursor.execute(self.end)
            self.end = self.cursor.fetchall()[0][0]

            self.info = "SELECT info FROM modelList WHERE model = " + value[0]
            self.cursor.execute(self.info)
            self.info = self.cursor.fetchall()[0][0]

        else:
            print("nothing selected")

        if self.make_box:
            # update boxes with newly-gotten info
            self.make_box.delete(0, 15)
            self.make_box.insert(0, self.make)

            self.model_box.delete(0, 15)
            self.model_box.insert(0, self.model)

            self.notes_box.delete(0, 20)
            self.notes_box.insert(0, self.notes)

            self.info_box.delete(0, 30)
            self.info_box.insert(0, self.info)

# doohickey that opens a new window to add a car
