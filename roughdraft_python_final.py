import tkinter as tk

class App:
    def __init__(self, master):
        self.master = master
        self.entries = []
        self.create_widgets()

    def create_widgets(self):
        
        tk.Label(self.master, text="Product Name").grid(row=0, column=0)
        tk.Label(self.master, text="Serial Number").grid(row=0, column=1)
        tk.Label(self.master, text="Quantity").grid(row=0, column=2)

        
        self.product_entry = tk.Entry(self.master)
        self.product_entry.grid(row=1, column=0)

        self.serial_entry = tk.Entry(self.master)
        self.serial_entry.grid(row=1, column=1)

        self.quantity_entry = tk.Entry(self.master)
        self.quantity_entry.grid(row=1, column=2)

        
        tk.Button(self.master, text="Add", command=self.add_entry).grid(row=2, column=0)
        tk.Button(self.master, text="Delete", command=self.delete_entry).grid(row=2, column=1)
        tk.Button(self.master, text="Edit", command=self.edit_entry).grid(row=2, column=2)

        
        self.table = tk.Listbox(self.master)
        self.table.grid(row=3, column=0, columnspan=3)

    def add_entry(self):
        
        product_name = self.product_entry.get()
        serial_number = self.serial_entry.get()
        quantity = self.quantity_entry.get()

        if product_name and serial_number and quantity:
            self.entries.append((product_name, "-", serial_number, "-", quantity))
            self.product_entry.delete(0, tk.END)
            self.serial_entry.delete(0, tk.END)
            self.quantity_entry.delete(0, tk.END)

            self.show_entries()

    def delete_entry(self):
        
        selected = self.table.curselection()

        if selected:
            self.entries.pop(selected[0])
            self.show_entries()

    def edit_entry(self):
        
        selected = self.table.curselection()

        if selected:
           
            entry = self.entries[selected[0]]
            self.product_entry.insert(0, entry[0])
            self.serial_entry.insert(0, entry[1])
            self.quantity_entry.insert(0, entry[2])

            
            self.entries.pop(selected[0])

            self.show_entries()

    def show_entries(self):
        
        self.table.delete(0, tk.END)

        for i, entry in enumerate(self.entries):
            self.table.insert(i, entry)

root = tk.Tk()
app = App(root)
root.mainloop()
