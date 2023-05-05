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

# main tkinter class
class App():
    # setting things to initialize upon app startup
    def __init__(self, window):
        self.window = window
        self.main_font = ('Arial', 12)
        self.create_widgets()
        # declaring lists for each class type
        self.tools_list = []
        self.hardware_list = []
        self.lumber_list = []
        # setting the size, title and icon of the window
        window.geometry('1000x500')
        window.minsize(500, 400)
        window.title('Hardware Inventory')
        icon = PhotoImage(file='logo.png')
        window.iconphoto(True, icon)
        # grid settings to help with rescaling when changing the window size
        # NOTE: it's still not great but it kind of works
        Grid.columnconfigure(window, 0, weight=1)
        Grid.columnconfigure(window, 1, weight=1)
        # a trace to watch for what the option menu item is, updates labels when lumber is the current option
        # this trace uses the update_labels_for_lumber function
        self.selected_catagory.trace('w', self.update_labels_for_lumber)
        # binds the enter key to window so when it is pressed it will call the on_enter function, which then calls the add function
        self.window.bind('<Return>', self.on_enter)

    # function to create the widgets themselves
    def create_widgets(self):
        # creating label for the catagory field, assigning it a spot in the grid
        self.catagory_label = Label(self.window, text='Catagory:', font=self.main_font)
        self.catagory_label.grid(row=0, column=0, sticky=E)

        # creating label for the item field, assigning it a spot in the grid
        self.item_label = Label(self.window, text='Item:', font=self.main_font)
        self.item_label.grid(row=1, column=0, sticky=E)

        # creating label for the brand field, assigning it a spot in the grid
        self.brand_label = Label(self.window, text='Brand:', font=self.main_font)
        self.brand_label.grid(row=2, column=0, sticky=E)

        # creating label for the quantity field, assigning it a spot in the grid
        self.qty_label = Label(self.window, text='Quantity:', font=self.main_font)
        self.qty_label.grid(row=3, column=0, sticky=E)

        # display label is a label that starts with no text but is then updated to let the user know what contents were added
        # when the add button is pressed
        # this label is modified by the submit function
        self.display_label = Label(window, text='', font=self.main_font)
        self.display_label.grid(row=4, column=0, sticky="NESW", padx=20, columnspan=2)

        # creating catagory dropdown and assigning its contents to the category_options list
        catagory_options = ['Tools', 'Hardware', 'Lumber']
        # setting the default value
        self.selected_catagory = StringVar(self.window)
        self.selected_catagory.set(catagory_options[0])
        catagory_drop = OptionMenu(self.window, self.selected_catagory, *catagory_options)
        # configures option menu and places in the grid
        catagory_drop.configure(width=20, font=self.main_font)
        catagory_drop.grid(row=0, column=1, sticky=W, pady=2)
        # entry box for item, then grid placement
        self.item_entry = Entry(self.window, font=self.main_font)
        self.item_entry.grid(row=1, column=1, sticky=W)

        # entry box for brand, then grid placement
        self.brand_entry = Entry(self.window, font=self.main_font)
        self.brand_entry.grid(row=2, column=1, sticky=W)

        # entry box for quantity, then grid placement
        self.qty_entry = Entry(self.window, font=self.main_font)
        self.qty_entry.grid(row=3, column=1, sticky=W)

        # add button to add the current entry field text to the appropriate list (tools, hardware or lumber), then grid placement
        # this button calls the update_list function
        self.add_button = Button(self.window, command=self.add, text='Add', font=self.main_font, width=20)
        self.add_button.grid(row=5, column=1, sticky=W, pady=2)


        # creating clear button to remove user input from entry boxes, then grid placement
        # this button calls the clear_form function
        Button(self.window, command=self.clear_form, text='Clear', font=self.main_font, width=20).grid(row=6, column=1, sticky=W, pady=2)

        # write excel button should write the content of each class list to an excel file, however it won't work while the
        # tkinter loop is running
        # this button calls the write_excel function
        Button(self.window, command=self.write_excel, text='Write Excel', font=self.main_font, width=20).grid(row=7, column=1, sticky=W, pady=2)

        # open excel button should open the already written to excel sheet, however it only opens a blank one at the moment
        Button(self.window, command=self.open_excel, text='Open Excel', font=self.main_font, width=20).grid(row=8, column=1, sticky=W, pady=2)

    # function to determine which class to create, and return a list of that class' attributes
    def submit(self):
    # local variables to be used within the function
        item_catagory = self.selected_catagory.get()
        item = self.item_entry.get()
        item_brand = self.brand_entry.get()
        item_qty = self.qty_entry.get()

        # if statement to decide which class to create: Tools, Hardware or Lumber
        # this one will create an object from the Tools class
        if item_catagory == 'Tools':
            t1 = Tools(item_brand, item_qty)
            # if statement to make sure no entry fields are empty, if not it displays an added message and returns
            if any(i == '' for i in [item, item_brand, item_qty]):
                self.display_label.config(text=f'All fields required')
            else:
                self.display_label.config(text=f'{t1.qty} {t1.brand} {item} added')
                # returning a list of the user entered values
                return list([item, item_brand, item_qty])

        # this one will create an object from the Hardware class
        elif item_catagory == 'Hardware':
            t1 = Hardware(item_brand, item_qty)
            if any(i == '' for i in [item, item_brand, item_qty]):
                self.display_label.config(text=f'All fields required')
            else:
                self.display_label.config(text=f'{t1.qty} {t1.brand} {item} added')
                return list([item, item_brand, item_qty])

        # this one will create an object from the Lumber class
        elif item_catagory == 'Lumber':
            t1 = Lumber(item_brand, item_qty)
            if any(i == '' for i in [item, item_brand, item_qty]):
                self.display_label.config(text=f'All fields required')
            else:
                self.display_label.config(text=f'{t1.qty} {t1.cut} {item} added')
                return list([item, item_brand, item_qty])
            
    # add_list function updates the list of whichever type of item is created (tool, hardware or lumber)
    def add(self):
        # checking to make sure the submit function is not returning None
        if self.submit() is None:
            pass
        # appending the list with the new value pulled from the entry boxes
        else:
            # logic to select which list to update based on the option menu choice
            if self.selected_catagory.get() == 'Tools':
                self.tools_list.append(self.submit())
                print(self.tools_list)  # DEBUG, delete this line before turned in
            elif self.selected_catagory.get() == 'Hardware':
                self.hardware_list.append(self.submit())
                print(self.hardware_list)  # DEBUG, delete this line before turned in
            elif self.selected_catagory.get() == 'Lumber':
                self.lumber_list.append(self.submit())
                print(self.lumber_list)  # DEBUG, delete this line before turned in

    # event function to call the add function and the clear form function, this is used to bind enter to the window, 
    # so that enter also adds to the list and clears the existing user entries and sets the cursor back to the item entry box
    def on_enter(self, event):
        self.add()
        self.clear_form()
        self.item_entry.focus_set()

    # clear_form function removes all user entered data on the form
    def clear_form(self):
        self.item_entry.delete(0, END)
        self.brand_entry.delete(0, END)
        self.qty_entry.delete(0, END)

    # update_labels_for_lumber dynamically changes the brand and item labels as the lumber class does not use them.
    # it instead uses cut and wood type, the labels are changed to reflect that
    def update_labels_for_lumber(self, *args):
        if self.selected_catagory.get() == 'Lumber':
            self.item_label.config(text='Wood:')
            self.brand_label.config(text='Cut:')
        else:
            self.item_label.config(text='Item:')
            self.brand_label.config(text='Brand:')


    # write_excel function uses a pandas dataframe to write the contents of the above lists to an excel spreadsheet
    def write_excel(self):
        # creating dataframes for each class
        tools_df = pd.DataFrame(self.tools_list, columns=['Item', 'Brand', 'Qty'])
        hardware_df = pd.DataFrame(self.hardware_list, columns=['Item', 'Brand', 'Qty'])
        lumber_df = pd.DataFrame(self.lumber_list, columns=['Wood', 'Cut', 'Qty'])
        self.display_label.config(text=f' ')
        # opening inventory.xlsx file and writing contents to it, each class gets its own sheet for organization
        with pd.ExcelWriter('inventory.xlsx') as writer:
            tools_df.to_excel(writer, sheet_name='Tools')
            hardware_df.to_excel(writer, sheet_name='Hardware')
            lumber_df.to_excel(writer, sheet_name='Lumber')

    # open_excel opens the specified excel file, inventory.xlsx
    def open_excel(self):
        inventory = openpyxl.load_workbook('inventory.xlsx')
        inventory.save('inventory.xlsx')
        os.system('start EXCEL.EXE inventory.xlsx')

# defines window as tkinter instance, creates instance of the App class called app ans passes in window then begins mainloop
window = Tk()
app = App(window)
window.mainloop()