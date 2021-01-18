# This is the central file for carData and creates the UI for the program.

import sqlite3
import tkinter
import structures

chosen_car = structures.Car()


if __name__ == '__main__':

    # basic setup shizwoz
    conn = sqlite3.connect("carInfo.sqlite")

    main_window = tkinter.Tk()
    main_window.title("Car Database")
    main_window.geometry("640x480")

    # row and column setup
    main_window.columnconfigure(0, weight=1)
    main_window.columnconfigure(1, weight=1)
    main_window.columnconfigure(2, weight=5)
    main_window.columnconfigure(3, weight=5)

    main_window.rowconfigure(0, weight=1)
    main_window.rowconfigure(1, weight=5)
    main_window.rowconfigure(2, weight=5)
    main_window.rowconfigure(3, weight=5)
    main_window.rowconfigure(4, weight=3)
    main_window.rowconfigure(5, weight=1)
    main_window.rowconfigure(6, weight=3)

    # labels
    tkinter.Label(main_window, text="make").grid(row=0, column=0)
    tkinter.Label(main_window, text="model").grid(row=0, column=1)

    # makes listbox
    make_list = structures.DataListBox(main_window, conn, "makeList", "make")
    make_list.re_query()
    make_list.grid(row=1, column=0, sticky="nsew", rowspan=5, padx=(20, 20))
    make_list.config(border=2, relief="sunken")

    # models listbox
    model_list = structures.DataListBox(main_window, conn, "modelList", "model")
    model_list.re_query()
    model_list.grid(row=1, column=1, sticky="nsew", rowspan=3, padx=(20, 20))
    model_list.config(border=2, relief="sunken")

    make_list.link(model_list, "make")
    model_list.car_link(chosen_car)

    # selected car information frame
    car_frame = tkinter.LabelFrame(main_window, text="Model Details", labelanchor="n")
    car_frame.grid(row=1, column=2, rowspan=4, columnspan=2, sticky="nsew", padx=(20, 20))

    # selected car info boxes
    makeBox = tkinter.Entry(car_frame, width=15)
    makeBox.grid(row=2, column=2, sticky='s', padx=(20, 0), pady=(10, 0))

    modelBox = tkinter.Entry(car_frame, width=15)
    modelBox.grid(row=2, column=3, sticky='s', padx=(30, 0))

    notesBox = tkinter.Entry(car_frame, width=20)
    notesBox.grid(row=3, column=2, columnspan=2, sticky='s', padx=(25, 0), pady=(20, 0))

    infoBox = tkinter.Entry(car_frame, width=30)
    infoBox.grid(row=4, column=2, columnspan=2, rowspan=3, sticky='nsew', padx=(25, 10), pady=(20, 20))

    chosen_car.link_boxes(makeBox, modelBox, notesBox, None, None, infoBox)

    # buttons
    newButton = tkinter.Button(main_window, text="Add new", width=10)
    newButton.grid(row=4, column=1, sticky="n", pady=(20, 0))
    editButton = tkinter.Button(main_window, text="Edit current", width=10)
    editButton.grid(row=5, column=1, sticky="n")

    # main loop
    main_window.mainloop()
    conn.close()