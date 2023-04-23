# imports; Tkinter: for GUI
#          Pandas: for dataframes and excel
#          os: to launch excel file
#          openpyxl: attempting to open the excel file
from tkinter import *
import pandas as pd
import os
import openpyxl  

# Tools class with attributes brand and quantity
class Tools:
    def __init__(self, brand, qty):
        self.brand = brand
        self.qty = qty

# Hardware class with attributes brand and quantity
class Hardware:
    def __init__(self, brand, qty):
        self.brand = brand
        self.qty = qty

# Lumber class with attributes cut and quantity
class Lumber:
    def __init__(self, cut, qty):
        self.cut = cut
        self.qty = qty

# function to determine which class to create, and return a list of that classes attributes
def submit():
    # local variables to be used within the function
    item_catagory = selected_catagory.get()
    item = item_entry.get()
    item_brand = brand_entry.get()
    item_qty = qty_entry.get()

    # if statement to decide which class to create: Tools, Hardware or Lumber
    # this one will create an object from the Tools class
    if item_catagory == 'Tools':
        t1 = Tools(item_brand, item_qty)
        # if statement to make sure no entry fields are empty, if not it displays an added message and returns
        if any(i == '' for i in [item, item_brand, item_qty]):
            display_label.config(text=f'all fields required')
        else:
            display_label.config(text=f'{t1.qty} {t1.brand} {item} added')
            # returning a list of the user entered values
            return list([item, item_brand, item_qty])

    # this one will create an object from the Hardware class
    elif item_catagory == 'Hardware':
        t1 = Hardware(item_brand, item_qty)
        if any(i == '' for i in [item, item_brand, item_qty]):
            display_label.config(text=f'all fields required')
        else:
            display_label.config(text=f'{t1.qty} {t1.brand} {item} added')
            return list([item, item_brand, item_qty])

    # this one will create an object from the Lumber class
    elif item_catagory == 'Lumber':
        t1 = Lumber(item_brand, item_qty)
        if any(i == '' for i in [item, item_brand, item_qty]):
            display_label.config(text=f'all fields required')
        else:
            display_label.config(text=f'{t1.qty} {t1.cut} {item} added')
            return list([item, item_brand, item_qty])

# update_list function updates the list of whichever type of item is created (tool, hardware or lumber)
def update_list():
    # checking to make sure the submit function is not returning None
    if submit() is None:
        pass
    # appending the list with the new value pulled from the entry boxes
    else:
        # logic to select which list to update based on the option menu choice
        if selected_catagory.get() == 'Tools':
            tools_list.append(submit())
            print(tools_list)
        elif selected_catagory.get() == 'Hardware':
            hardware_list.append(submit())
            print(hardware_list)
        elif selected_catagory.get() == 'Lumber':
            lumber_list.append(submit())
            print(lumber_list)

# clear_form function removes all user entered data on the form
def clear_form():
    item_entry.delete(0, END)
    brand_entry.delete(0, END)
    qty_entry.delete(0, END)

# update_labels_for_lumber dynamically changes the brand and item labels as the lumber class does not use them.
# it instead uses cut and wood type, the labels are changed to reflect that
def update_labels_for_lumber(*args):
    if selected_catagory.get() == 'Lumber':
        item_label.config(text='Wood:')
        brand_label.config(text='Cut:')
    else:
        item_label.config(text='Item:')
        brand_label.config(text='Brand:')

# declaring lists for each class type
tools_list = []
hardware_list = []
lumber_list = []

# write_excel function uses a pandas dataframe to write the contents of the above lists to an excel spreadsheet
# NOTE: for some reason this will only work after the main tkinter loop ends, I assigned it to a button but it wont write
# to the excel file before the tkinter loop is closed
def write_excel():
    # creating dataframes for each class
    tools_df = pd.DataFrame(tools_list, columns=['Item', 'Brand', 'Qty'])
    hardware_df = pd.DataFrame(hardware_list, columns=['Item', 'Brand', 'Qty'])
    lumber_df = pd.DataFrame(lumber_list, columns=['Wood', 'Cut', 'Qty'])
    # opening inventory.xlsx file and writing contents to it, each class gets its own sheet for organization
    with pd.ExcelWriter('inventory.xlsx') as writer:
        tools_df.to_excel(writer, sheet_name='Tools')
        hardware_df.to_excel(writer, sheet_name='Hardware')
        lumber_df.to_excel(writer, sheet_name='Lumber')

# open_excel opens the specified excel file, inventory.xlsx
# NOTE: while the main tkinter loop is running this only opens a blank excel file
def open_excel():
    inventory = openpyxl.load_workbook('inventory.xlsx')
    inventory.save('inventory.xlsx')
    os.system('start EXCEL.EXE inventory.xlsx')

# defining main Tkinter window
window = Tk()

# setting the size, title and icon of the window
window.geometry('1000x500')
window.title('Hardware Inventory')
icon = PhotoImage(file='logo.png')
window.iconphoto(True, icon)

# declaring a main font for later use to keep the form consistent
main_font = ('Arial', 12)

# grid settings to help with rescaling when changing the window size
# NOTE: it's still not great but it kind of works
Grid.columnconfigure(window, 0, weight=1)
Grid.columnconfigure(window, 1, weight=1)

# creating label for the catagory field, assigning it a spot in the grid
catagory_label = Label(window, text='Catagory:', font=main_font)
catagory_label.grid(row=0, column=0, sticky=E)

# creating label for the item field, assigning it a spot in the grid
item_label = Label(window, text='Item:', font=main_font)
item_label.grid(row=1, column=0, sticky=E)

# creating label for the brand field, assigning it a spot in the grid
brand_label = Label(window, text='Brand:', font=main_font)
brand_label.grid(row=2, column=0, sticky=E)

# creating label for the quantity field, assigning it a spot in the grid
qty_label = Label(window, text='Quantity:', font=main_font)
qty_label.grid(row=3, column=0, sticky=E)

# creating catagory dropdown and assigning its contents to the category_options list
catagory_options = ['Tools', 'Hardware', 'Lumber']
# setting the default value
selected_catagory = StringVar(window)
selected_catagory.set(catagory_options[0])
catagory_drop = OptionMenu(window, selected_catagory, *catagory_options)
# configures option menu and places in the grid
catagory_drop.configure(width=20, font=main_font)
catagory_drop.grid(row=0, column=1, sticky=W, pady=2)

# entry box for item, then grid placement
item_entry = Entry(window, font=main_font)
item_entry.grid(row=1, column=1, sticky=W, pady=2)

# entry box for brand, then grid placement
brand_entry = Entry(window, font=main_font)
brand_entry.grid(row=2, column=1, sticky=W, pady=2)

# entry box for quantity, then grid placement
qty_entry = Entry(window, font=main_font)
qty_entry.grid(row=3, column=1, sticky=W, pady=2)

# add button to add the current entry field text to the appropriate list (tools, hardware or lumber), then grid placement
# this button calls the update_list function
add_button = Button(window, command=update_list, text='Add', font=main_font)
add_button.grid(row=4, column=1, pady=2, padx=2)

# creating clear button to remove user input from entry boxes, then grid placement
# this button calls the clear_form function
clear_button = Button(window, command=clear_form, text='Clear', font=main_font)
clear_button.grid(row=5, column=1, pady=2, padx=2)

# submit button was used for a while during development but the add button kind of ate its functionality, leaving here
# just in case, uncomment next to lines to add it back
# submit_button = Button(window, command=submit, text='Submit', font=main_font)
# submit_button.grid(row=6, column=1, pady=2)

# write excel button should write the content of each class list to an excel file, however it won't work while the
# tkinter loop is running
# this button calls the write_excel function
write_excel_button = Button(window, command=write_excel, text='write excel', font=main_font)
write_excel_button.grid(row=6, column=1, pady=2)

# open excel button should open the already written to excel sheet, however it only opens a blank one at the moment
open_excel_button = Button(window, command=open_excel, text='open excel', font=main_font)
open_excel_button.grid(row=7, column=1, pady=2)

# display label is a label that starts with no text but is then updated to let the user know what contents were added
# when the add button is pressed
# this label is modified by the submit function
display_label = Label(window, text='', font=main_font)
display_label.grid(row=8, column=0, columnspan=2, pady=2)

# a trace to watch for what the option menu item is, updates labels when lumber is the current option
# this trace uses the update_labels_for_lumber function
selected_catagory.trace('w', update_labels_for_lumber)

# end of tkinter main loop
window.mainloop()