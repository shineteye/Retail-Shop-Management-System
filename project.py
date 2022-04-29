from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os,shutil
import zipfile
import sqlite3
import sys
import time
import datetime
import re
import random
from PIL import Image, ImageTk
import pyqrcode
from pyzbar.pyzbar import decode
# the general file directory for the location of the Project
Gen_File_Dir = r'C:\Users\RAMON\Desktop\Complete Assignment'
# the absolute file directory 
absolute_Dir = r"C:\\Users\RAMON"
# the sub directory which the database zip creates when zipping the file
# in my C: directory my sub dir is Users\Ramon\ and the project is stored on my desktop
Sub_Dir = r'\\Users\RAMON\Desktop'
# Some parts of the code in the in the Back up and restore section can be partly modified
# when errors are found
# ============================================================================================ #
# =======================START OF CODE======================================================== #
# connecting project to the store database
conn = sqlite3.connect(Gen_File_Dir+ r"\database\store.db")
c = conn.cursor()
# selecting the maximum ID
result = c.execute("SELECT Max(id) from inventory")
for r in result:
    id = r[0]


def AddToDatabase():
    global AddtoBDScreen

    AddtoBDScreen = Toplevel()
    AddtoBDScreen.geometry("1100x500")
    AddtoBDScreen.title("Add to the database")
    AddtoBDScreen.iconbitmap(Gen_File_Dir+ r"\store_2.ico")
    AddtoBDScreen.lift()
    AddtoBDScreen.focus()

    # main_screen.withdraw()

    class Database:
        def __init__(self, master):
            self.master = master
            self.heading = Label(master, width=700, text="Add to the Database", font=('candara', 40, 'bold'),
                                 fg="white", bg='green')
            self.heading.pack()
            # =========================================================================================
            self.mymenu = Menu(master)
            self.master.config(menu=self.mymenu)

            # function for going back to the home page
            def HomePage():
                try:
                    AddtoBDScreen.destroy()
                except AttributeError:
                    print("minor error")
                finally:
                    AddtoBDScreen.destroy()

            def helpF(self):
                root = Toplevel()
                root.geometry('400x400')
                root.title('Help')
                root.focus()
                root.lift()

                txtBox = Text(root, width=400, height=400, bd=4, relief='flat', font='calibri 15 bold')
                txtBox.place(x=0, y=0)
                txtBox.insert(END, 'This is a little documentation to help you with \nthe use of this program')
                root.mainloop()

            self.OPTMenu = Menu(self.mymenu)
            self.mymenu.add_cascade(label="OPTIONS", menu=self.OPTMenu)
            self.OPTMenu.add_separator()
            self.OPTMenu.add_command(label="Home", command=HomePage)

            # Label Frames for Labels and entries
            self.lblFrame = LabelFrame(master, text="Input Entries", height=340, width=600, bd=4,
                                       font="candara 12 bold")
            self.lblFrame.pack(side="left")
            self.lblFrame.place(x=10, y=70)

            # labels for entry window
            self.namelbl = Label(self.lblFrame, text="Enter Product Name", font=('candara', 15, 'bold'))
            self.namelbl.place(x=0, y=10)

            self.stocklbl = Label(self.lblFrame, text="Enter Stock Quantity", font=('candara', 15, 'bold'))
            self.stocklbl.place(x=0, y=50)

            self.Cplbl = Label(self.lblFrame, text="Enter Cost Price", font=('candara', 15, 'bold'))
            self.Cplbl.place(x=0, y=90)

            self.Splbl = Label(self.lblFrame, text="Enter Selling Price", font=('candara', 15, 'bold'))
            self.Splbl.place(x=0, y=130)

            self.Vendorlbl = Label(self.lblFrame, text="Enter Vendor's Name", font=('candara', 15, 'bold'))
            self.Vendorlbl.place(x=0, y=170)

            self.VendorPhonelbl = Label(self.lblFrame, text="Enter Vendor's Phone Num.", font=('candara', 15, 'bold'))
            self.VendorPhonelbl.place(x=0, y=210)

            # Entry for the labels
            self.name_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.name_ent.place(x=300, y=10)
            self.name_ent.focus()

            self.stock_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.stock_ent.place(x=300, y=50)

            self.Cp_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Cp_ent.place(x=300, y=90)

            self.Sp_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Sp_ent.place(x=300, y=130)

            self.Vendor_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Vendor_ent.place(x=300, y=170)

            self.Vendor_Phone_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Vendor_Phone_ent.place(x=300, y=210)

            # button for giving command to add stuff to the database
            self.btn_add = Button(self.lblFrame, width=25, height=2, text="Add to the Database", bg="green", fg="white",
                                  command=self.get_items)
            self.btn_add.place(x=395, y=260)
            # button for clearing all entries from the entry section
            self.btn_clear = Button(self.lblFrame, width=15, height=2, text="Clear All Entries", bg="red", fg="white",
                                    command=self.clear_All)
            self.btn_clear.place(x=300, y=260)
            print(self.btn_add)

            # creating a text box for the logs 
            self.txtBox = Text(master, width=50, height=20, wrap="word")
            self.txtBox.place(x=650, y=79)
            self.txtBox.insert(END, "Total number of id's in database at start of program: " + str(id))
            self.master.bind("<F1>", helpF)

        def get_items(self):
            # get free entries
            self.name = self.name_ent.get()
            self.stock = self.stock_ent.get()
            self.Cp = self.Cp_ent.get()
            self.Sp = self.Sp_ent.get()
            self.Vendor = self.Vendor_ent.get()
            self.Vendor_Phone = self.Vendor_Phone_ent.get()
            # dynamic entries
            # setting float values of 0 for Cp and stock if nothing is entered
            """if self.Cp == "" and self.stock =="":
                self.Cp == 0 and self.stock == 0
            else:"""
            if self.name == "" or self.stock == "" or self.Cp == "" or self.Sp == "":
                messagebox.showinfo("Error", "Please fill all the entries")
                AddtoBDScreen.focus()
            elif len(self.Vendor_Phone_ent.get()) != 10:
                messagebox.showerror("Error", "Not a valid Phone Number")
                AddtoBDScreen.focus()
            else:
                try:
                    self.totalCp = float(self.Cp) * float(self.stock)
                    self.totalSp = float(self.Sp) * float(self.stock)
                    self.assumedProfit = float(self.totalSp) - float(self.totalCp)
                except ValueError:
                    print("Empty fields")


                # regex for checking whether number is a Ghana number

                self.pattern = (r"^(024)?(054)?(055)?(059)?(020)?(050)?(027)?(057)?(026)?(023)?")
                self.match = re.match(self.pattern,self.Vendor_Phone)
                print(self.match)
                print(self.Vendor_Phone)

                if len(self.Vendor_Phone) != 10:
                    messagebox.showinfo("Error", "Vendor's Phone Number isn't Valid")
                elif not self.Vendor_Phone.startswith("0"):
                    messagebox.showinfo("Error", "Invalid Phone Number")
                elif self.name.isdecimal():
                    messagebox.showinfo("Prod. Name Error", "Invalid Name")
                elif not self.stock.isdecimal():
                    messagebox.showinfo("Error", "Invalid Stock Quantity\nEnter a number")
                elif not self.Cp.isdecimal():
                    messagebox.showinfo("Error", " Cost Price Input isn't a number")
                elif not self.Sp.isdecimal():
                    messagebox.showinfo("Error", " Selling Price Input isn't a number")
                elif self.Vendor.isdecimal():
                    messagebox.showinfo("Error", "Please enter a valid Vendor's name")
                elif not self.Vendor_Phone.isdecimal():
                    messagebox.showinfo("Error", "Please enter a valid Phone Num")
                elif self.match == None:
                    messagebox.showinfo("Error","Not a valid number")
                elif self.match.group() == '':
                    messagebox.showinfo("Error","Not a valid number")

                # if self.name == "" or self.stock == "" or self.Cp == "" or self.Sp == "":
                #    messagebox.showinfo("Error", "Please fill all the entries")
                else:
                    sql = "INSERT INTO inventory( name,stock,cp,sp,totalcp, totalsp, assumedProfit, vendor, vendorPhone) VALUES(?,?,?,?,?,?,?,?,?)"
                    c.execute(sql, (
                        self.name, self.stock, self.Cp, self.Sp, self.totalCp, self.totalSp, self.assumedProfit,
                        self.Vendor,
                        self.Vendor_Phone))
                    conn.commit()
                    global result
                    result = c.execute("SELECT Max(id) from inventory")
                    for r in result:
                        id = r[0]
                    # txtBox Insert
                    self.txtBox.insert(END, "\n\nInserted " + str(self.name) + " into the database with ID: " + str(id))
                    messagebox.showinfo("Success", "Succesfully added to the database")

                    if self.btn_add == 1:
                        id += 1
                        self.txtBox.insert(END,
                                           "\n\nInserted " + str(self.name) + " into the database with ID: " + str(id))
                        messagebox.showinfo("Success", "Succesfully added to the database")
                AddtoBDScreen.focus()
                AddtoBDScreen.lift()

        def clear_All(self):
            # num = id +1
            self.name_ent.delete(0, END)
            self.stock_ent.delete(0, END)
            self.Cp_ent.delete(0, END)
            self.Sp_ent.delete(0, END)
            self.Vendor_ent.delete(0, END)
            self.Vendor_Phone_ent.delete(0, END)
            messagebox.showinfo("Clear", "Entries cleared")
            AddtoBDScreen.focus()
            AddtoBDScreen.lift()

    d = Database(AddtoBDScreen)

    AddtoBDScreen.mainloop()


def UpdateDatabase():
    global uptDatabase
    uptDatabase = Toplevel()

    uptDatabase.geometry("1100x550")
    uptDatabase.title("Update the database")
    uptDatabase.iconbitmap(Gen_File_Dir+r"\store_2.ico")
    uptDatabase.lift()
    uptDatabase.focus()
    # main_screen.withdraw()

    result = c.execute("SELECT Max(id) from inventory")
    for r in result:
        id = r[0]

    print(id)

    class DatabaseUpdate:

        def __init__(self, master):

            self.master = master
            self.heading = Label(master, width=600, text="Update the Database", font='candara 40 bold', fg="white",
                                 bg='green')
            self.heading.pack()
            # =========================================================================================
            self.mymenu = Menu(master)
            self.master.config(menu=self.mymenu)

            # function for going back to the home page
            def HomePage():
                try:
                    uptDatabase.destroy()
                except AttributeError:
                    print("minor error")
                finally:
                    uptDatabase.destroy()

            def helpF(self):
                root = Toplevel()
                root.geometry('400x400')
                root.title('Help')
                root.focus()
                root.lift()

                txtBox = Text(root, width=400, height=400, bd=4, relief='flat', font='calibri 15 bold')
                txtBox.place(x=0, y=0)
                txtBox.insert(END, 'This is a little documentation to help you with \nthe use of this program')
                root.mainloop()

            def Exit(self):
                uptDatabase.destroy()

            self.OPTMenu = Menu(self.mymenu)
            self.mymenu.add_cascade(label="OPTIONS", menu=self.OPTMenu)
            self.OPTMenu.add_command(label="Home ", command=HomePage)
            self.OPTMenu.add_separator()
            self.OPTMenu.add_command(label="Exit       Esc", command=Exit)

            # Label frame for labels  and entries
            self.lblFrame = LabelFrame(master, text="Input Entries", height=450, width=555, bd=4,
                                       font="candara 12 bold")
            self.lblFrame.pack(side="left")
            self.lblFrame.place(x=10, y=70)

            # Labels for id and entry
            self.idl = Label(self.lblFrame, text="Enter ID of product", font='candara 15 bold')
            self.idl.place(x=10, y=10)

            self.ide = Entry(self.lblFrame, width=13, font=("candara", 15, "bold"))
            self.ide.place(x=260, y=10)
            self.ide.focus()

            # Search button
            self.btn_search = Button(self.lblFrame, width=12, text="Search", font="candara 10 bold", bg="steelblue",
                                     bd=2, command=self.search)
            self.btn_search.place(x=445, y=10)

            # labels for entry window
            self.namelbl = Label(self.lblFrame, text=" Product Name", font='candara 15 bold')
            self.namelbl.place(x=10, y=50)

            self.stocklbl = Label(self.lblFrame, text=" Stock Quantity", font='candara 15 bold')
            self.stocklbl.place(x=10, y=90)

            self.Cplbl = Label(self.lblFrame, text=" Cost Price", font='candara 15 bold')
            self.Cplbl.place(x=10, y=130)

            self.Splbl = Label(self.lblFrame, text=" Selling Price", font='candara 15 bold')
            self.Splbl.place(x=10, y=170)

            self.TotalCp = Label(self.lblFrame, text=" Total Selling Price", font='candara 15 bold')
            self.TotalCp.place(x=10, y=210)

            self.TotalSp = Label(self.lblFrame, text=" Total Cost Price", font='candara 15 bold')
            self.TotalSp.place(x=10, y=250)

            self.Vendorlbl = Label(self.lblFrame, text=" Vendor's Name", font='candara 15 bold')
            self.Vendorlbl.place(x=10, y=290)

            self.VendorPhonelbl = Label(self.lblFrame, text=" Vendor's Phone Num.", font='candara 15 bold')
            self.VendorPhonelbl.place(x=10, y=330)

            # Entry for the labels
            self.name_ent = Entry(self.lblFrame, width=25, font='candara 15 bold')
            self.name_ent.place(x=260, y=50)

            self.stock_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.stock_ent.place(x=260, y=90)

            self.Cp_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Cp_ent.place(x=260, y=130)

            self.Sp_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Sp_ent.place(x=260, y=170)

            self.TotalCp_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.TotalCp_ent.place(x=260, y=210)

            self.TotalSp_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.TotalSp_ent.place(x=260, y=250)

            self.Vendor_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Vendor_ent.place(x=260, y=290)

            self.Vendor_Phone_ent = Entry(self.lblFrame, width=25, font=('candara', 15, 'bold'))
            self.Vendor_Phone_ent.place(x=260, y=330)

            # button for giving command to update to the database
            self.btn_add = Button(self.lblFrame, width=38, height=2, text="Update Database", bg="green", fg="white",
                                  bd=3,
                                  command=self.update_database)
            self.btn_add.place(x=260, y=370)

            # creating a text box for the logs
            self.txtBox = Text(master, width=50, height=27, bd=2, relief="sunken", wrap="word")
            self.txtBox.place(x=650, y=75)
            self.txtBox.insert(END, "Total number of id's in database: " + str(id))
            self.master.bind("<F1>", helpF)
            self.master.bind("<Escape>", Exit)

        def search(self):
            sql = "SELECT * FROM inventory WHERE id=?"
            result = c.execute(sql, (self.ide.get(),))
            for r in result:
                self.inf1 = r[1]  # name of product
                self.inf2 = r[2]  # Stock Quantity
                self.inf3 = r[3]  # Cost Price
                self.inf4 = r[4]  # Selling price
                self.inf5 = r[5]  # total cost price
                self.inf6 = r[6]  # total selling price
                self.inf7 = r[7]  # assumed profit
                self.inf8 = r[8]  # name of vendor
                self.inf9 = r[9]  # phone num of vendor
            conn.commit()
            try:
                if self.ide.get().isalpha():
                    messagebox.showinfo("Error", "Not a valid Id")
                elif self.ide.get() > str(id):
                    messagebox.showerror("Error", "Id entered is out of range")
                # insert update into entries
                else:
                    self.name_ent.delete(0, END)
                    self.name_ent.insert(0, str(self.inf1))

                    self.stock_ent.delete(0, END)
                    self.stock_ent.insert(0, str(self.inf2))

                    self.Cp_ent.delete(0, END)
                    self.Cp_ent.insert(0, str(self.inf3))

                    self.Sp_ent.delete(0, END)
                    self.Sp_ent.insert(0, str(self.inf4))

                    self.TotalCp_ent.delete(0, END)
                    self.TotalCp_ent.insert(0, str(self.inf5))

                    self.TotalSp_ent.delete(0, END)
                    self.TotalSp_ent.insert(0, str(self.inf6))

                    self.Vendor_ent.delete(0, END)
                    self.Vendor_ent.insert(0, str(self.inf8))

                    self.Vendor_Phone_ent.delete(0, END)
                    self.Vendor_Phone_ent.insert(0, "0" + str(self.inf9))
            except AttributeError:
                messagebox.showerror("Error", "Enter an id to search for")

        def update_database(self):
            # getting all updated values
            self.u1 = self.name_ent.get()
            self.u2 = self.stock_ent.get()
            self.u3 = self.Cp_ent.get()
            self.u4 = self.Sp_ent.get()
            self.u5 = self.TotalCp_ent.get()
            self.u6 = self.TotalSp_ent.get()
            # self.u7 = self.name_ent.get() # assumed profit entry value for update
            self.u8 = self.Vendor_ent.get()
            self.u9 = self.Vendor_Phone_ent.get()

            # regex for checking whether number is a Ghana number
            #if self.btn_search == 1:
            self.pattern = (r"^(024)?(054)?(055)?(059)?(020)?(050)?(027)?(057)?(026)?(023)?")
            self.match = re.match(self.pattern,self.u9)
            print(self.match)
            print(self.u9)

            # parameters to check for the validity of the inputs
            if self.u1.isdecimal():
                messagebox.showinfo("Prod. Name Error", "Invalid Name")
            elif not self.u2.isdecimal():
                messagebox.showinfo("Error", "Invalid Stock Quantity\nEnter a number")
            elif not self.u3.isdecimal():
                messagebox.showinfo("Error", " Cost Price Input isn't a number")
            elif not self.u4.isdecimal():
                messagebox.showinfo("Error", " Selling Price Input isn't a number")
            elif not self.u5.isdecimal():
                messagebox.showinfo("Error", "Input isn't a number")
            elif not self.u6.isdecimal():
                messagebox.showinfo("Error", "Input isn't a number")
            elif self.u8.isdecimal():
                messagebox.showinfo("Error", "Please enter a Valid name")
            elif not self.u9.isdecimal():
                messagebox.showinfo("Error", "Please enter a valid Phone Num")
            elif len(self.u9) != 10:
                messagebox.showinfo("Error", "Vendor's Phone Number isn't Valid")
            elif self.match == None:
                messagebox.showinfo("Error","Not a valid number")
            elif self.match.group() == '':
                messagebox.showinfo("Error","Not a valid number")
            else:
                self.u9 = str(self.u9)
                query = "UPDATE inventory SET name=?,stock=?,cp=?,sp=?,totalcp=?,totalsp=?,vendor=?,vendorPhone=? WHERE id=?"
                c.execute(query,
                          (self.u1, self.u2, self.u3, self.u4, self.u5, self.u6, self.u8, self.u9, self.ide.get()))
                conn.commit()
                messagebox.showinfo("Success", "Database Updated")
            uptDatabase.lift()
            uptDatabase.focus()

    d = DatabaseUpdate(uptDatabase)

    uptDatabase.mainloop()


def MainWorkFrame():
    global mainScreen
    global time
    mainScreen = Toplevel()

    mainScreen.geometry("1360x700+0+0")
    mainScreen.title("Sales Work Main Frame")
    mainScreen.iconbitmap(Gen_File_Dir+r"\store_2.ico")
    mainScreen.focus()
    mainScreen.lift()

    # date
    date = datetime.datetime.now().date()
    # time
    # time = time.time()
    # database structure
    conn = sqlite3.connect(Gen_File_Dir+r"\database\store.db")
    c = conn.cursor()

    # List like for stuff
    productsList = []
    productsPrice = []
    productsQuantity = []
    productsId = []
    productsDiscount =[]

    # list for labels
    LabelsList = []

    class Application:
        def __init__(self, master):
            self.master = master
            # =========================================================================================
            self.mymenu = Menu(master)
            self.master.config(menu=self.mymenu)

            # function for going back to the home page
            def HomePage():
                try:
                    mainScreen.destroy()
                except AttributeError:
                    print("minor error")
                finally:
                    mainScreen.destroy()

            def helpF(self):
                root = Toplevel()
                root.geometry('400x400')
                root.title('Help')
                root.focus()
                root.lift()

                txtBox = Text(root, width=400, height=400, bd=4, relief='flat', font='calibri 15 bold')
                txtBox.place(x=0, y=0)
                txtBox.insert(END, 'This is a little documentation to help you with \nthe use of this program')
                root.mainloop()

            def Exit():
                uptDatabase.destroy()

            self.OPTMenu = Menu(self.mymenu)
            self.mymenu.add_cascade(label="OPTIONS", menu=self.OPTMenu)
            self.OPTMenu.add_separator()
            self.OPTMenu.add_command(label="Home", command=HomePage)
            self.OPTMenu.add_separator()
            self.OPTMenu.add_command(label="Exit", command=Exit)

            # frames
            self.left = Frame(self.master, width=800, height=700, bg="white")
            self.left.pack(side="left")

            self.right = Frame(self.master, width=555, height=700, bg="green", bd=5, relief="raise")
            self.right.pack(side="right")

            self.heading = Label(self.left, text="                       SIROCCO'S MINI STORE                    ",
                                 bg="green", fg="white", font="candara 28 bold", bd=3, relief="raise")
            self.heading.place(x=0, y=0)

            self.dateL = Label(self.right, text="Today's Date is: " + str(date),
                               font="Candara 16 bold", fg="green", justify="center")
            self.dateL.place(x=120, y=0)

            # Table for invoice
            self.tProduct = Label(self.right, text="Products               ",
                                  font="candara 16 bold", fg="white", bg="green")
            self.tProduct.place(x=0, y=60)

            self.tQuantity = Label(self.right, text="Quantity", font="candara 16 bold", fg="white", bg="green")
            self.tQuantity.place(x=200, y=60)

            self.tAmount = Label(self.right, text="Amount", font="candara 16 bold", fg="white", bg="green")
            self.tAmount.place(x=350, y=60)

            self.totalLabel = Label(self.right, text="Total: ", font="candara 16 bold", fg="white", bg="green")
            self.totalLabel.place(x=0, y=600)
            self.totalVat = Label(self.right, text="VAT:Ghc 0.20 ", font="candara 16 bold", fg="white", bg="green")
            self.totalVat.place(x=0, y=630)

            # Entry for stuff
            self.Label_E_Id = Label(self.left, text="Enter Id of Product", font="candara 24 bold",
                                    bg="white", fg="green")
            self.Label_E_Id.place(x=20, y=60)

            self.EntryofID = Entry(self.left, width=13, font="candara 24 bold", bd=3, relief="sunken")
            self.EntryofID.place(x=310, y=60)
            self.EntryofID.focus()
            # Search Button
            self.SearchId = Button(self.left, width=10, height=2, text="Search", bd=5, relief="raise",
                                   fg="white", bg="green", activebackground="lightgreen", activeforeground="black",
                                   command=self.fill)
            self.SearchId.place(x=560, y=60)

            # fill in with the function (fill)
            self.ProductName = Label(self.left, text="Product's Name", font="candara 20 bold", fg="green", bg="white")
            self.ProductName.place(x=20, y=200)
            self.ProdNameInfo = Label(self.left, text="          ", font="candara 20 bold",
                                      fg="green", bd=3, relief="sunken")
            self.ProdNameInfo.place(x=270, y=200)

            self.ProdPrice = Label(self.left, text="Price", font="candara 20 bold", fg="green", bg="white")
            self.ProdPrice.place(x=20, y=250)
            self.ProdPriceInfo = Label(self.left, text="          ", font="candara 20 bold",
                                       fg="green", bd=3, relief="sunken")
            self.ProdPriceInfo.place(x=270, y=250)
            self.master.bind("<Return>", self.fill)
            self.master.bind("<Up>", self.addToCart)
            self.master.bind("<space>", self.generateBill)
            self.master.bind("<F1>", helpF)
            # self.master.bind("<Return>",self.addToCart)

        def fill(self):
            try:

                # get the product id's and fill it in with the Labels above
                self.get_ID = self.EntryofID.get()
                float(self.get_ID)

                query = "SELECT * FROM inventory WHERE id=?"
                result = c.execute(query, (self.get_ID,))
                for self.r in result:
                    self.get_ID = self.r[0]
                    self.getName = self.r[1]
                    self.getPrice = self.r[4]
                    self.getStock = self.r[2]
                    self.ProdNameInfo.configure(text=str(self.getName))
                    self.ProdPriceInfo.configure(text="Ghc " + str(self.getPrice) + ".00")
                # Creating the Quantity and Discount Label
                self.Quantity = Label(self.left, text="Enter Quantity", font="candara 16 bold",
                                      fg="green", bg="white")
                self.Quantity.place(x=20, y=350)
                self.QuantityEnt = Entry(self.left, width=20, font="candara 16 bold", bd=3, relief="sunken")
                self.QuantityEnt.place(x=260, y=350)
                #
                self.QuantityEnt.focus()

                self.DiscountL = Label(self.left, text="Enter Discount", font="candara 16 bold",
                                       fg="green", bg="white")
                self.DiscountL.place(x=20, y=390)
                self.DiscountEnt = Entry(self.left, width=20, font="candara 16 bold", bd=3, relief="sunken")
                self.DiscountEnt.place(x=260, y=390)
                self.DiscountEnt.insert(END, 0)

                # button for adding items to cart
                self.addToCartBtn = Button(self.left, text="Add To Cart", font="candara 16 bold",
                                           fg="white", bg="green", bd=3, relief="raised", command=self.addToCart)
                self.addToCartBtn.place(x=360, y=430)

                # creating the given amount label and entry section
                self.GivenAmnt = Label(self.left, text="Enter the Given Amount", font="candara 16 bold", fg="green",
                                       bg="white")
                self.GivenAmnt.place(x=20, y=490)

                self.GivenAmntEnt = Entry(self.left, width=20, font="candara 16 bold", fg="green",
                                          bg="white", bd=3, relief="sunken")
                self.GivenAmntEnt.place(x=260, y=490)
                # button for change calculation
                self.ChangeCalcBtn = Button(self.left, text="Calculate Change", font="candara 16 bold",
                                            fg="white", bg="green", command=self.ChangeCalculator)
                self.ChangeCalcBtn.place(x=315, y=530)

            except ValueError:
                messagebox.showinfo("Error", "Enter ID number")
                mainScreen.focus()

        def addToCart(self):
            # getting quantity value from the database
            self.QuantityValue = (self.QuantityEnt.get())
            self.DiscountValue = (float(self.DiscountEnt.get()))
            if self.QuantityValue == "":
                messagebox.showinfo("Error", "Empty input for Quantity")
            elif int(self.QuantityValue) > int(self.getStock):
                messagebox.showinfo("Error", "Not enough " + self.getName + " in stock")
            else:
                self.finalPrice = (float(self.QuantityValue) * float(self.getPrice)) - (float(self.DiscountEnt.get()))
                productsList.append(self.getName)
                productsPrice.append(self.finalPrice)
                productsQuantity.append(self.QuantityValue)
                productsId.append(self.get_ID)
                productsDiscount.append(self.DiscountValue)

                self.xValue = 0
                self.yValue = 100
                self.counter = 0
                self.DisList = []
                for self.p in productsList:
                    self.tempName = Label(self.right, text=str(productsList[self.counter]), font="candara 16 bold",
                                          bg="green", fg="white")
                    self.tempName.place(x=0, y=self.yValue)
                    LabelsList.append(self.tempName)

                    self.tempQuant = Label(self.right, text=str(productsQuantity[self.counter]), font="candara 16 bold",
                                           bg="green", fg="white")
                    self.tempQuant.place(x=200, y=self.yValue)
                    LabelsList.append(self.tempQuant)

                    self.tempPrice = Label(self.right, text="Ghc " + str(productsPrice[self.counter]) + "0",
                                           font="candara 16 bold", bg="green", fg="white")
                    self.tempPrice.place(x=350, y=self.yValue)
                    LabelsList.append(self.tempPrice)

                    self.yValue += 40
                    self.counter += 1

                    # Vat Value
                    self.Vat = float(0.20)                      

                    # reconfiguring the total price
                    #print(float(sum(productsPrice)-self.DiscountVal))
                    self.totalLabel.configure(text="Total: Ghc" + str(float(sum(productsPrice)))+ "0")

                    # erasing everything below the display for the name of the product and the price
                    self.Quantity.place_forget()
                    self.QuantityEnt.place_forget()
                    self.DiscountL.place_forget()
                    self.DiscountEnt.place_forget()
                    # self.ChangeCalcBtn.place_forget()
                    self.addToCartBtn.place_forget()
                    # self.GivenAmnt.place_forget()
                    # self.GivenAmntEnt.place_forget()
                    self.ProdNameInfo.configure(text="           ")
                    self.ProdPriceInfo.configure(text="           ")
                    self.EntryofID.delete(0, END)
                    self.EntryofID.focus()

        def ChangeCalculator(self):
            try:
                if float(self.GivenAmntEnt.get()) < self.finalPrice:
                    messagebox.showerror("Error", "Amount not enough")
                elif float(self.GivenAmntEnt.get()) == "":
                    messagebox.showinfo("Error", "Please enter an amount")
                elif self.GivenAmntEnt.get().isalpha():
                    messagebox.showinfo("Error", "Not a valid Amount")
                else:
                    self.amntGiven = float(self.GivenAmntEnt.get())
                    self.ourTotal = float(sum(productsPrice))

                    self.GivenAmntToGive = self.amntGiven - self.ourTotal

                    # label for the change to be given
                    self.changeVal = Label(self.left, text="Change: Ghc" + str(self.GivenAmntToGive),
                                           font="candara 16 bold", fg="white", bg="green")
                    self.changeVal.place(x=530, y=490)

                    # bill Generator button
                    self.GenerateBill = Button(self.left, text="GENERATE BILL", font="georgia", width=89, height=2
                                               , fg="black", bg="steelblue", command=self.generateBill)
                    self.GenerateBill.place(x=0, y=600)
            except ValueError:
                messagebox.showinfo("Error", "You forgot to check the balance")

        def generateBill(self):
            
            try:
                # create the bill before you update the database
                fileDirectory = Gen_File_Dir+"\INVOICE\Invoice " + str(date) + "\ "
                if not os.path.exists(fileDirectory):
                    os.makedirs(fileDirectory)
                else:
                    # creating the template of the bill
                    company = "\t\t\t\t  SIROCCOS GROCERY STORE\n"
                    address = "\t\t\t\tAmrahia off the Dodowa Rd.\n"
                    phone = "\t\t\t\t\t0557793777\n"
                    sample = "\t\t\t\t\t INVOICE\n"
                    dt = "\t\t\t\t\t" + str(date)

                    table_header = '\n\n\t\t\t...................................\n\t\t\tSN.\tProducts\tTQuantity\tAmount\n\t' \
                                    '\t\t................................... '
                    fileContent = company + address + phone + sample + dt + "\n" + table_header
                    # open a file to write the invoice to
                    # creating the file name
                    fileName = str(fileDirectory) + str(random.randrange(1000, 10000)) + ".rtf"
                    f = open(fileName, "w")
                    f.write(fileContent)
                    # fill dynamics
                    r = 0
                    for t in productsList:
                        f.write("\n\t\t\t" + str(r + 1) + "\t" + str(productsList[r] + "       ")[:7] + "\t " + str(
                            productsQuantity[r]).rjust(4,' ') + "\t\t" + str(productsPrice[r]).rjust(4,' '))
                        r += 1
                    f.write("\n\n\n\t\t\tVat:" + str(self.Vat))
                    if str(sum(productsDiscount)) == 0.0:
                        f.write("\n\t\t\tTotal:Ghc" + str(sum(productsPrice) + self.Vat ) + "0")
                        f.write("\n\t\t\tThanks for Shopping with us. ):'")
                        os.startfile(fileName, "print")
                        f.close()
                    else:
                        f.write('\n\t\t\tTotal Discount:Ghc'+ str(sum(productsDiscount)) + "0" )
                        f.write("\n\t\t\tTotal:Ghc" + str(sum(productsPrice) + self.Vat ) + "0")
                        f.write("\n\t\t\tThanks for Shopping with us. ):'")
                        os.startfile(fileName, "print")
                        f.close()

                # decreasing the stock
                self.x = 0

                initial = "SELECT * FROM inventory WHERE id=?"
                result= c.execute(initial, (productsId[self.x],))

                for i in productsList:
                    for self.r in result:
                        self.oldStock = self.r[2]
                    self.newStock = int(self.oldStock) - int(productsQuantity[self.x])

                    # updating the stock
                    sql = "UPDATE inventory SET stock=? WHERE id=?"
                    c.execute(sql, (self.newStock, productsId[self.x]))
                    conn.commit()

                    # insert transaction into the  transaction database
                    sql2 = "INSERT INTO transactions (productName, quantity, amount, date) VALUES (?,?,?,?)"
                    c.execute(sql2, (productsList[self.x], productsQuantity[self.x], productsPrice[self.x], date))
                    conn.commit()

                    self.x += 1

                for i in LabelsList:
                    i.destroy()
                del (productsList[:])
                del (productsId[:])
                del (productsPrice[:])
                del (productsQuantity[:])
                self.GivenAmntEnt.delete(0, END)
                self.EntryofID.focus()
                self.changeVal.place_forget()
                self.totalLabel.configure(text="")
                messagebox.showinfo("Success", "Bill has been Generated")
                mainScreen.focus()
                mainScreen.lift()
            except AttributeError:
                messagebox.showinfo("Error", "Forgot to calculate your change")
            finally:
                return
            
            
        

    app = Application(mainScreen)

    mainScreen.mainloop()


def QrCodeScreen():
    global QrScreen
    global ScanBtn
    QrScreen = Toplevel()
    QrScreen.geometry("600x600+100+50")
    QrScreen.title("QrCode Screen")
    QrScreen.iconbitmap(Gen_File_Dir+"\store_2.ico")
    QrScreen.focus()
    QrScreen.lift()
    # instance for creating menus in QrScreen
    mymenu = Menu(QrScreen)
    QrScreen.config(menu=mymenu)
    
    class QR:
        def __init__(self,master,*args,**kwargs):
            self.master = master
            
            # function for going back to the home page
            def HomePage():
                try:
                    QrScreen.destroy()
                except AttributeError:
                    print("minor error")
                finally:
                    QrScreen.destroy()

            def helpF(self):
                root = Toplevel()
                root.geometry('400x400')
                root.title('Help')
                root.focus()
                root.lift()

                txtBox = Text(root, width=400, height=400, bd=4, relief='flat', font='calibri 15 bold')
                txtBox.place(x=0, y=0)
                txtBox.insert(END, 'This is a little documentation to help you with \nthe use of this program')
                root.mainloop()

            def Exit(self):
                QrScreen.destroy()
            QrScreen.bind("<F1>", helpF)

            OPTMenu = Menu(mymenu)
            mymenu.add_cascade(label="OPTIONS", menu=OPTMenu)
            OPTMenu.add_command(label="Home", command=HomePage)
            OPTMenu.add_separator()
            OPTMenu.add_command(label="Exit", command=Exit)
            
            self.ScanBtn = Button(QrScreen, text="Click to open scanned image", font="candara", width=25, height=2, fg='white',
                        bg='green', relief='raised', command=self.PopUpDiagBox)
            self.ScanBtn.pack()
                        
        def PopUpDiagBox(self):
            global selectedImg
            global filename
            global ScanBtn
                    
            self.filename = filedialog.askopenfilename(
                initialdir=Gen_File_Dir+"\scanned Qr Images/",
                title="Select the QrCode Image", filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))

            self.selectedImg = ImageTk.PhotoImage(Image.open(self.filename))
            Label(QrScreen, text="").pack()
            self.selectedImgLabel = Label(QrScreen, image=self.selectedImg, width=170, height=170)
            self.selectedImgLabel.pack()
            Label(QrScreen, text="").pack()
            self.InfoText = Label(QrScreen, text="Text from QrCode", font='candara 16 bold')
            self.InfoText.pack()
            # to find the image name =========three lines below
            # imageList=[str(filename)]
            # image=','.join(imageList)
            # imageName = image[96:]

            self.d = decode(Image.open(self.filename))
            self.textfromcode = self.d[0].data.decode('ascii')
            self.resultText = Label(QrScreen, text=self.textfromcode, font='candara 16 bold')
            self.resultText.pack()
            QrScreen.focus()
            QrScreen.lift()

            # print(image)
            # print(len(image))
            # print(image[96:])
            print(self.ScanBtn)
            #Label(QrScreen,text=filename).pack()
            
            self.ClrBtn = Button(QrScreen,text='Clear',command=self.clear)
            Label(QrScreen).pack()
            self.ClrBtn.pack()
            
        def clear(self):
            self.selectedImgLabel.configure(image='')
            self.InfoText.configure(text='')
            self.resultText.configure(text='')
            
        
            

        

        HeaderLbl = Label(QrScreen, text="QR CODE READER", font="candara 25 bold", width=300, bg="Green",
                        bd=5, relief='groove', fg="white")
        HeaderLbl.pack()
        # HeaderLbl.place(x=100,y=10)
        Label(QrScreen, text="").pack()
        

        # qr = pyqrcode.create("shine")
        # qr.png("shine.png", scale=8)
        # d = decode(Image.open(selectedImg))

        # print(d)
        #QrScreen.bind("<F1>", self.helpF)
    Q = QR(QrScreen)
    QrScreen.mainloop()


def BacknRestore():
    BackRestore = Toplevel()
    BackRestore.geometry("600x600+100+50")
    BackRestore.title("Backup and Restore")
    BackRestore.iconbitmap(Gen_File_Dir+ "\store_2.ico")
    BackRestore.focus()
    BackRestore.lift()

    hlbl = Label(BackRestore, text="BackUp & Restore", font="candara 16 bold", width=400, height=2, bg='green',
                 fg='white')
    hlbl.pack()
    Label(BackRestore, text='').pack()


    class Backup:
        def __init__(self, master):
            self.master = master

            self.bkpButton = Button(BackRestore, text="Back up", font="candara 20 bold",height=5,width=15, command=self.BackUpToZip)
            self.bkpButton.pack()
            Label(BackRestore, text='').pack()
            Label(BackRestore).pack()
            self.RestoreButton = Button(BackRestore, text="Restore", font="candara 20 bold",height=5, width=15, command=self.restore)
            self.RestoreButton.pack()
            Label(BackRestore).pack()

        zipname =''


        # function for creating a backup of our database files and invoice folder

        def BackUpToZip(self):
            # Backup the entire contents of the "folder" into a zip file
            global zipname
            self.folder = os.path.abspath(Gen_File_Dir + r"\database")
            print(self.folder)
            # figure out the filename this code should use based on what files already exist

            self.num = 1
            while True:
                self.zipfilename = os.path.basename(self.folder) + "_" + str(self.num) + ".zip"
                if not os.path.exists(self.zipfilename):
                    break
                self.num += 1
            zipname = self.zipfilename
            # Create the ZIP file.
            print('Creating %s...' % (self.zipfilename))
            self.backupZip = zipfile.ZipFile(self.zipfilename, 'w')

            # Walk the entire folder tree and compress the files in each folder.
            for foldername, subfolders, filenames in os.walk(self.folder):
                print("Adding files  in %s..." % foldername)
                # Add the current folder to the zip file
                self.backupZip.write(foldername)

                # Add all the files in the folder to the zip file.
                self.backupZip.write(foldername)
                # Add all the files  in this folder to the zip file
                for filename in filenames:
                    newBase = os.path.basename(self.folder) + "_"
                    if filename.startswith(newBase) and filename.endswith('.zip'):
                        continue
                    self.backupZip.write(os.path.join(foldername, filename))
            self.backupZip.close()
            print("done")
            print(zipname)
            # initial back up was made to the C:\\Users\Ramon directory
            # so we move into that particular directory
            os.chdir(absolute_Dir)
            # now we copy the initial zip file to the BackUp directory in our assesment folder
            self.databseZip = absolute_Dir + self.zipfilename
            shutil.copy(self.databseZip,Gen_File_Dir+'\BackUp')
            messagebox.showinfo("Success", "Zip file backup success")

            self.pathLbl = Label(BackRestore, text=r"BackUp can be located in the BackUp folder ", font='candara 14 bold',
                                 bd=4, relief='groove', justify='center')
            self.pathLbl.place(x=120, y=250)
            self.bkpname = Label(BackRestore, text=r"BackUp Name : " + self.zipfilename, font='candara 14 bold', bd=4,
                                 relief='groove', justify='center')
            self.bkpname.place(x=160, y=290)
            if self.bkpButton == 1:
                self.pathLbl.place_forget()
                self.bkpname.place_forget()
            BackRestore.focus()
            BackRestore.lift()



        print(zipname)

        def restore(self):
            global zipname
            os.chdir = Gen_File_Dir+ '\BackUp'
            self.restorezip = zipfile.ZipFile(zipname)
            self.restorezip.extractall(Gen_File_Dir+'\BackUp')
            print(zipname)
            try:
                os.unlink(Gen_File_Dir +'\database\store.db')
                shutil.rmtree(Gen_File_Dir +'\database\INVOICE', ignore_errors=False, onerror=None)
                shutil.move(Gen_File_Dir + r'\BackUp' + Sub_Dir + '\Complete Assignment\database\INVOICE',
                    Gen_File_Dir+r'\database')
                shutil.move(Gen_File_Dir + r'\BackUp' + Sub_Dir + '\Complete Assignment\database\store.db',
                    Gen_File_Dir+r'\database')
                self.restorezip.close()
                os.unlink(Gen_File_Dir + r'\BackUp\Users')
                print('done')
            except PermissionError:
                pass
            finally:
                messagebox.showinfo('Success','Restored Successfully')

    B = Backup(BacknRestore)
    #R = Restore(BacknRestore)

    BackRestore.mainloop()


def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.iconbitmap(Gen_File_Dir+r"\store_2.ico")
    mymenu = Menu(main_screen)
    main_screen.config(menu=mymenu)

    ####################################################################
    # ===========section containing menu bars============================
    # creating new command function

    def helpF(self):
        root = Toplevel()
        root.geometry('400x400')
        root.title('Help')
        root.iconbitmap(Gen_File_Dir+"\store_2.ico")

        root.focus()

        txtBox = Text(root, width=400, height=400, bd=4, relief='flat', font='calibri 15 bold')
        txtBox.place(x=0, y=0)
        txtBox.insert(END, 'This is a little documentation to help you with \nthe use of this program')
        root.mainloop()

    # creating a menu item

    fileMenu = Menu(mymenu)
    mymenu.add_cascade(label="MENU", menu=fileMenu)
    fileMenu.add_command(label="For help  F1", command='')
    fileMenu.add_command(label="Exit     Esc", command=exit)
    # my menu is the whole menus on the top
    # mymenu.add_command(label="New...", command=help)
    # mymenu.add_command(label="Exit",command=root.quit)
    #####################################################################
    main_screen.geometry("600x560+400+50")
    main_screen.title(" Main Interface")
    Label(text=r"CLICK ON THE TASK YOU WANT TO PERFORM", bg="green", fg='white', width="300", height="2",
          font=("candara", 15, 'bold')).pack()
    Label(text="").pack()
    Button(text="ADDING GOODS TO THE DATABASE", height=4, width=30, relief='groove', bd=4,
           command=AddToDatabase).pack()
    # command=login
    Label(text="").pack()
    Button(text=r"UPDATE THE DATABASE", height=4, width=30, relief='groove', bd=4, command=UpdateDatabase).pack()
    # command=register
    Label(text="").pack()
    Button(text="RETAIL INTERFACE", height=4, width=30, relief='groove', bd=4, command=MainWorkFrame).pack()

    Label(text="").pack()
    Button(text="QR CODE READER", height=4, width=30, relief='groove', bd=4, command=QrCodeScreen).pack()

    Label(text="").pack()
    Button(text="BACKUP AND RESTORE", height=4, width=30, relief='groove', bd=4, command=BacknRestore).pack()

    main_screen.bind('<F1>', helpF)
    main_screen.bind("<Escape>", exit)

    main_screen.mainloop()


main_account_screen()
