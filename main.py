from tkinter import *
from tkinter import messagebox, ttk
from PIL import ImageTk # pip install pillow
import mysql.connector as connector # pip install mysql-connector-python
import sys
import datetime # pip install DateTime
import csv # pip install csv
import os

def connect_to_database():
    try:
        connection = connector.connect(
            host="localhost",
            user="root",
            password="mysql"
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS stockease")
            connection.database = "stockease"    
        return connection

    except connector.Error as e:  # Fixed: Imported connector.Error instead of Error#+
        print(f"Error connecting to the database: {e}")
        sys.exit()
        return None
    
    
def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Users (id INT AUTO_INCREMENT, username VARCHAR(255), password VARCHAR(255),email VARCHAR(255), age INT, PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Products (id INT AUTO_INCREMENT, name VARCHAR(255), SKU VARCHAR(255), price FLOAT, quantity INT, supplier VARCHAR(255), PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Sales (id INT AUTO_INCREMENT, product_id INT, quantity_sold INT, sale_date DATE, total_amount FLOAT, customer_name Varchar(50), PRIMARY KEY (id), FOREIGN KEY (product_id) REFERENCES Products(id))")
    cursor.execute("CREATE TABLE IF NOT EXISTS Orders (id INT AUTO_INCREMENT, product_id INT, quantity_ordered INT, order_date DATE, status VARCHAR(255), PRIMARY KEY (id), FOREIGN KEY (product_id) REFERENCES Products(id))")
    connection.commit()

class Register:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("StockEase - Register")
        self.root.geometry('1350x700')
        self.root.resizable(False, False)

        # Widgets
        self.bg_register = ImageTk.PhotoImage(file = 'images/bg.png')
        Label(root, image = self.bg_register).place(x=0,y=0,relheight=1,relwidth=1)

        self.register_front_img = ImageTk.PhotoImage(file = 'images/front.png')
        Label(root, image = self.register_front_img).place(x=250, y=150)

        # Register Frame
        frame = Frame(root, bg = 'white')
        frame.place(x = 550, y = 150, width = 550, height = 404)

        Label(frame, text='REGISTER HERE', font = ("times new roman", 20, "bold"), bg = 'white', fg = 'Red').place(x = 45,y = 25)

        self.usr_var = StringVar()
        Label(frame, text='Username', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 65)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.usr_var).place(x = 45, y = 95, width=250)

        self.age_var = IntVar()
        Label(frame, text='Age', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 325, y = 65)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.age_var).place(x = 325, y = 95, width=170)

        self.email_var = StringVar()
        Label(frame, text='Email Address', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 120)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.email_var).place(x = 45, y = 150, width=250)

        self.pass_var = StringVar()
        Label(frame, text='Password', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 175)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.pass_var).place(x = 45, y = 205, width=250)

        self.con_pass_var = StringVar()
        Label(frame, text='Confirm Password', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 230)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray',  textvariable=self.con_pass_var).place(x = 45, y = 260, width=250)

        self.chk_var = IntVar()
        Checkbutton(frame, text = 'I Agree to the Terms & Conditions', bg = 'white', font = ('times new roman', 12), onvalue = 1, offvalue = 0, variable= self.chk_var).place(x = 45, y = 300)

        Button(frame, text = 'Register Now ->', justify='center', font = ('times new roman', 15, 'bold'), bg = 'green', fg = 'white', command = self.register_data).place(x = 45, y = 340, width = 200)

        Button(root, text = 'Sign In', justify='center', font = ('times new roman', 15, 'bold'), bg = 'white', command = self.sign_in).place(x = 300, y = 460, width = 200)

    def clear(self):
        self.usr_var.set('')
        self.age_var.set(0)
        self.email_var.set('')
        self.pass_var.set('')
        self.con_pass_var.set('')
        self.chk_var.set(0)

    def register_data(self):
        cursor = self.connection.cursor()
        if self.usr_var.get() == '' or self.age_var.get() == 0 or self.con_pass_var.get() == '' or self.email_var.get() == '' or self.pass_var.get() == '':
            messagebox.showerror("Error", "All Fields are Required", parent = self.root)
        elif self.pass_var.get() != self.con_pass_var.get():
            messagebox.showerror("Error", "Password and Confirm Password do not match.", parent = self.root)
        elif self.age_var.get() < 18:
            messagebox.showerror("Error", "You must be at least 18 years old.", parent = self.root)
        elif self.chk_var.get() == 0:
            messagebox.showerror("Error", "Please agree to the Terms & Conditions", parent = self.root)
        else:
            username = self.usr_var.get()
            age = self.age_var.get()
            email = self.email_var.get()
            password = self.pass_var.get()
            try:
                cursor.execute("SELECT * FROM Users WHERE email = %s", (self.email_var.get(),))
                row = cursor.fetchone()
                if row != None:
                    messagebox.showerror("Error", "Email already exists. Please try with another email.", parent = self.root)
                else:
                    cursor.execute("INSERT INTO Users (username, password, email, age) VALUES (%s, %s, %s, %s)", (username, password, email, age))
                    connection.commit()
                    cursor.close()
                    messagebox.showinfo("Success", "Registered Successfully", parent = self.root)
                    self.clear()
            except Exception as e:
                messagebox.showerror("Error", f"Error registering user: {e}", parent = self.root)

    def sign_in(self):
        self.root.destroy()
        new_root = Tk()
        obj = SignIn(new_root, self.connection)
        new_root.mainloop()

class SignIn:
    def __init__(self, root, connection):
        self.root = root
        self.connection = connection
        self.root.title("StockEase - Sign In")
        self.root.geometry('1350x700')
        self.root.resizable(False, False)
        self.bg_login_img = ImageTk.PhotoImage(file = 'images/bg_login.png')
        Label(root, image = self.bg_login_img).place(x = 0, y = 0, relheight=1,relwidth=1)
        self.front_img = ImageTk.PhotoImage(file = 'images/login_front.png')
        Label(root, image=self.front_img).place(x = 250,  y = 150)
        frame = Frame(root, bg = 'white')
        frame.place(x = 550, y = 150 ,width = 550, height=403)
        Label(frame, text='LOGIN HERE', font = ("times new roman", 20, "bold"), bg = 'white', fg = 'Red').place(x = 45,y = 25)
        self.email_login_var = StringVar()
        Label(frame, text='Email Address', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 85)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.email_login_var).place(x = 45, y = 115, width=250)
        self.usr_login_var = StringVar()
        Label(frame, text='Username', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 145)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.usr_login_var).place(x = 45, y = 180, width=250)
        self.pass_login_var = StringVar()
        Label(frame, text='Password', font=('times new roman', 15, 'bold'), bg = 'white', fg = 'gray').place(x = 45, y = 210)
        Entry(frame, font=('times new roman', 15), bg = 'lightgray', textvariable= self.pass_login_var).place(x = 45, y = 240, width=250)
        Button(frame, text = 'Not a member? Sign Up', bg = 'white', fg = 'Green', font = ('times new roman', 15, 'bold'), bd = 0, command = self.register).place(x = 43, y = 270)
        Button(frame, text = 'Login', justify='center', font = ('times new roman', 15, 'bold'), bg = 'green', fg = 'white', command = self.login).place(x = 45, y = 320, width = 200)

    def login(self):
        cursor = self.connection.cursor()
        if self.usr_login_var.get() == '' or self.email_login_var.get() == '' or self.pass_login_var.get() == '':
            messagebox.showerror("Error", "All Fields are Required", parent = self.root)
        else:
            email = self.email_login_var.get()
            username = self.usr_login_var.get()
            password = self.pass_login_var.get()
            try:
                cursor.execute("SELECT * FROM Users WHERE email = %s AND username = %s AND password = %s", (email, username, password))
                row = cursor.fetchone()
                if row == None:
                    messagebox.showerror("Error", "Invalid Email, Username or Password", parent = self.root)
                else:
                    messagebox.showinfo("Success", "Logged In Successfully", parent = self.root)
                    self.root.destroy()
                    new_root = Tk()
                    obj = Home(new_root, self.connection, username)
                    new_root.mainloop()
            except Exception as e:
                messagebox.showerror("Error", f"Error logging in: {e}", parent = self.root)

    def register(self):
        self.root.destroy()
        new_root = Tk()
        obj = Register(new_root, self.connection)
        new_root.mainloop()

class Home:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.root.title("StockEase")
        self.root.geometry('1350x700')
        self.root.resizable(False, False)
        self.username = username
        strip_frame = Frame(self.root, bg='#020328', height=70)  # You can change the color and height
        strip_frame.pack(side=TOP, fill=X)
        Label(strip_frame, text = self.username, fg = 'white', bg = '#020328', font = ('times new roman', 25)).place(x = 25,y =  13)
        Button(strip_frame, text = 'Sign Out', font = ('times new roman',25), fg = 'white', bg = '#020328', bd = 0, activebackground='#40404b', activeforeground='white', command= self.signout).place(x = 1190, y = 5)

        # product
        product_frame = Frame(root,bg = 'white', bd = 10, relief=RIDGE).place(x = 30, y = 90, width = 1290, height = 200)
        Label(product_frame,  text = 'Product :', font = ('times new roman', 30, 'bold'), fg = '#020328', bg = 'white').place(x = 73, y = 110)
        Button(product_frame,command = self.add_products, text = 'Add Product', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place( x = 81, y = 187)
        Button(product_frame,command = self.update_products, text = 'Update Product', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place( x = 371, y = 187)
        Button(product_frame,command = self.delete_products, text = 'Delete Product', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place( x = 700, y = 187)
        Button(product_frame,command = self.view_products, text= 'View Products', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place(x = 1020, y = 187)

        # Sales
        sales_frame = Frame(root, bg = 'white', bd = 10, relief= RIDGE).place(x = 30, y = 310, width = 350, height = 330)
        Label(sales_frame, text= 'Sales', font = ('times new roman', 30, 'bold'), bg = 'white', fg = '#020328').place(x = 157, y = 330)
        Button(sales_frame,command = self.record_sales, text = 'Record Sale', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place( x = 105, y = 495)
        Button(sales_frame,command = self.view_sales, text = 'View Sales', font = ('times new roman', 25, 'bold'), fg = 'white', bg = 'green', bd = 5).place(x = 115, y = 395)

        # Orders
        orders_frame = Frame(root, bg = 'white', bd = 10, relief=RIDGE).place(x = 500, y = 310, width = 350, height = 330)
        Label(orders_frame, text= 'Orders', font = ('times new roman', 30, 'bold'), bg = 'white', fg = '#020328').place(x = 605, y = 330)
        Button(orders_frame,command = self.record_orders, text = 'Record Order', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place( x = 553, y = 495)
        Button(orders_frame,command = self.view_orders, text = 'View Orders', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place( x = 563, y = 395)

        # Reports
        reports_frame = Frame(root, bg = 'white', bd = 10, relief=RIDGE).place(x = 970, y = 310, width = 350, height = 330)
        Label(reports_frame, text= 'Reports', font = ('times new roman', 30, 'bold'), bg = 'white', fg = '#020328').place(x = 1082, y = 330)
        Button(reports_frame,command = self.inventory_report, text = 'Inventory Report', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place(x = 1008, y = 495)
        Button(reports_frame,command = self.sales_report, text = 'Sales Report', font = ('times new roman',25, 'bold'), fg = 'white', bg = 'green', bd = 5).place(x = 1037, y = 395)

    def signout(self):
        self.root.destroy()
        new_root = Tk()
        obj = SignIn(new_root, self.connection)
        new_root.mainloop()

    # Product Functions

    def add_products(self):
        self.root.destroy()
        new_root = Tk()
        obj = AddProd(new_root, self.connection, self.username)
        new_root.mainloop()

    def delete_products(self):
        self.root.destroy()
        new_root = Tk()
        obj = DelProd(new_root, self.connection, self.username)
        new_root.mainloop()

    def update_products(self):
        self.root.destroy()
        new_root = Tk()
        obj = UpdateProduct(new_root, self.connection, self.username)
        new_root.mainloop()

    def view_products(self):
        self.root.destroy()
        new_root = Tk()
        obj = ViewProd(new_root, self.connection, self.username)
        new_root.mainloop()

    # Sales Functions

    def record_sales(self):
        self.root.destroy()
        new_root = Tk()
        obj = RecSale(new_root, self.connection, self.username)
        new_root.mainloop()

    def view_sales(self):
        self.root.destroy()
        new_root = Tk()
        obj = ViewSales(new_root, self.connection, self.username)
        new_root.mainloop()
    
    # Orders Functions

    def record_orders(self):
        self.root.destroy()
        new_root = Tk()
        obj = RecOrder(new_root, self.connection, self.username)
        new_root.mainloop()

    def view_orders(self):
        self.root.destroy()
        new_root = Tk()
        obj = ViewOrders(new_root, self.connection, self.username)
        new_root.mainloop()
    
    # Reports Functions

    def inventory_report(self):
        cursor = self.connection.cursor()   
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        if rows != []:
            filename = "Inventory Report" + str(datetime.date.today())
            with open(f'Inventory/{filename}.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Name', 'SKU', 'Price', 'Quantity', 'Supplier'])
                for row in rows:
                    writer.writerow(list(row))
            messagebox.showinfo('Success', f'Inventory report has been created. Name : {filename}')
        else:
            messagebox.showerror('Error', 'No products found in the database.')


    def sales_report(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM sales")
        rows = cursor.fetchall()
        if rows != []:
            filename = "Sales Report" + str(datetime.date.today())
            with open(f'Sales/{filename}.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Product ID', 'Quantity Sold', 'Date', 'Total Amount', 'Customer Name'])
                for row in rows:
                    writer.writerow(list(row))
            messagebox.showinfo('Success', f'Sales report has been created. Name : {filename}')
        else:
            messagebox.showerror('Error', 'No sales found in the database.')

    

class AddProd:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("800x600")
        self.root.title('Add Product')

        # Widgets
        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='ADD PRODUCT', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=295, y=15)

        self.name_var = StringVar()
        Label(self.root, text='Name: ', font=('Roboto', 20, 'bold')).place(x=200, y=90)
        Entry(self.root, bg='lightyellow', bd=5, font=('Roboto', 15, 'bold'), textvariable=self.name_var).place(x=300, y=90, width=275, height=40)

        self.sku_var = StringVar()
        Label(self.root, text='SKU : ', font=('Roboto', 20, 'bold')).place(x=200, y=140)
        Entry(self.root, bg='lightyellow', bd=5, font=('Roboto', 15, 'bold'), textvariable=self.sku_var).place(x=300, y=140, width=275, height=40)

        self.price_var = DoubleVar()
        self.qnt_var = IntVar()

        # Create and place labels and entries
        Label(self.root, text='Price: ', font=('Roboto', 20, 'bold')).place(x=200, y=190)
        Entry(self.root, bg='lightyellow', bd=5, font=('Roboto', 15, 'bold'), textvariable=self.price_var).place(x=300, y=190, width=275, height=40)

        Label(self.root, text='Quantity: ', font=('Roboto', 20, 'bold')).place(x=200, y=240)
        Entry(self.root, bg='lightyellow', bd=5, font=('Roboto', 15, 'bold'), textvariable=self.qnt_var).place(x=340, y=240, width=235, height=40)


        self.sup_var = StringVar()
        Label(self.root, text='Supplier: ', font=('Roboto', 20, 'bold')).place(x=140, y=290)
        Entry(self.root, bg='lightyellow', bd=5, font=('Roboto', 15, 'bold'), textvariable=self.sup_var).place(x=300, y=290, width=315, height=40)

        Button(self.root, text='Add Product ->', font=('Roboto', 25, 'bold'), fg='white', bg='green', bd=5, command=self.add_prod_to_database).place(x=270, y=457)

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def add_prod_to_database(self):
        # Check if fields are empty or invalid
        if not self.name_var.get() or not self.sku_var.get() or self.price_var.get() <= 0 or self.qnt_var.get() <= 0 or not self.sup_var.get():
            messagebox.showerror('Error', 'All fields are required and must be valid.')
        else:
            name = self.name_var.get()
            sku = self.sku_var.get()
            supplier = self.sup_var.get()
            price = self.price_var.get()
            quantity = self.qnt_var.get()

            cursor = self.connection.cursor()
            try:
                cursor.execute("INSERT INTO Products (name, SKU, supplier, price, quantity) VALUES (%s, %s, %s, %s, %s)", (name, sku, supplier, price, quantity))
                self.connection.commit()
                cursor.execute("SELECT id FROM Products where name = %s", name)
                id = cursor.fetchone()[0]
                messagebox.showinfo('Success', f'Product added successfully. Product id: {id}', parent=self.root)

                
            except Exception as e:
                messagebox.showerror('Error', f'Error adding product: {e}', parent=self.root)
            finally:
                cursor.close()

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()

class DelProd:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("250x290")
        self.root.title('Delete Product')

        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='DELETE PRODUCT', font=("Roboto", 15, 'bold'), bg='#020328', fg='white').place(x=40, y=20)

        self.id_var = IntVar()
        Label(self.root, text = 'ID: ', font=('Roboto', 15, 'bold')).place(x = 25,  y = 90)
        Entry(self.root, bg = 'lightyellow', bd = 5, font=('Roboto', 15, 'bold'), textvariable=self.id_var).place(x = 70, y = 90, width = 140, height = 30)

        self.sku_var = StringVar()
        Label(self.root, text = 'SKU: ', font = ('Robot', 15, 'bold')).place(x = 25, y = 130)
        Entry(self.root, bg = 'lightyellow', bd = 5, font=('Roboto', 15, 'bold'), textvariable=self.sku_var).place(x = 80, y = 130, width = 130, height = 30)

        Button(self.root, text='Delete Product ->', font=('Roboto', 15, 'bold'), fg='white', bg='red', bd=5, command=self.delete_product_from_database).place(x=30, y=200)


        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()

    def delete_product_from_database(self):
        cursor = self.connection.cursor()
        if self.id_var.get() <= 0 or self.sku_var.get() == '':
            messagebox.showerror('Error', 'All details shooould be valid.')
        else:
            id = self.id_var.get()
            sku = self.sku_var.get()
            cursor.execute('SELECT * FROM ProductS WHERE id = %s AND SKU = %s', (id, sku))
            row = cursor.fetchone()
            if row == None:
                messagebox.showerror('Error', 'Product not found.')
            else:
                messagebox.askokcancel('Confirmations', 'Are you sure you want to delete this product?')
                if messagebox.OK:
                    cursor.execute('DELETE FROM Products WHERE id = %s AND SKU = %s', (id, sku))
                    self.connection.commit()
                    messagebox.showinfo('Success', 'Product deleted successfully.')
        cursor.close()
        
class UpdateProduct:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("800x600")
        self.root.title('Update Product')

        # Widgets
        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='UPDATE PRODUCT', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=275, y=15)

        self.id_var  =IntVar()
        Label(self.root, text = "ID: ", font= ("Roboto", 20, 'bold')).place(x = 200, y = 90)
        Entry(self.root, bg = 'lightyellow', bd = 5, font= ("Roboto", 20, 'bold'), textvariable=self.id_var).place(x =270, y = 90, width=300, height = 40)

        Label(self.root, text = '* Enter the new values, leave blank if no new values', font = ('Roboto', 20, 'bold')).place(x = 70, y = 140)

        self.name_var = StringVar()
        Label(self.root, text = 'Name: ', font = ('Roboto', 20, 'bold')).place(x = 180, y = 190)
        Entry(self.root, bg = 'lightyellow', bd = 5, font= ("Roboto", 20, 'bold'), textvariable=self.name_var).place(x = 290, y = 190, width=300, height = 40)

        self.sku_var = StringVar()
        Label(self.root, text = 'SKU: ', font = ('Roboto', 20, 'bold')).place(x = 200, y = 240)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable= self.sku_var).place(x = 290, y = 240, width = 280, height = 40)

        self.price_var = DoubleVar()
        Label(self.root, text = 'Price: ', font = ('Roboto', 20, 'bold')).place(x = 190, y = 290)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable=self.price_var).place(x = 290, y = 290, width = 280, height = 40)

        self.qnt_var = IntVar()
        Label(self.root, text = "Quantity: ", font = ('Roboto', 20, 'bold')).place(x = 145, y = 340)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.qnt_var).place(x = 290, y = 340, width =320, height = 40)

        self.sup_var = StringVar()
        Label(self.root,  text = 'Supplier: ', font = ('Roboto', 20, 'bold')).place(x = 145, y = 390)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.sup_var).place(x = 290, y = 390, width =320, height = 40)

        Button(self.root, text='Update Product ->', font=('Roboto', 25, 'bold'), fg='white', bg='green', bd=5, command=self.update_prod_in_database).place(x=240, y=457)


        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def update_prod_in_database(self):
        id = self.id_var.get()
        if id <= 0:
            messagebox.showerror('Error', 'ID should be a positive integer.')
        else:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM Products WHERE id = %s", id)
            row = cursor.fetchone()
            if row is None:
                messagebox.showerror('Error', 'Product not found.')
            else:
                name = self.name_var.get()
                sku = self.sku_var.get()
                price = self.price_var.get()
                quant = self.qnt_var.get()
                supplier = self.sup_var.get()

                if name != '':
                    cursor.execute("UPDATE Products SET name = %s WHERE id = %s", (name, id))
                    self.connection.commit()
                if sku !='':
                    cursor.execute("UPDATE Products SET SKU = %s WHERE id = %s", (sku, id))
                    self.connection.commit()
                if price != 0:
                    cursor.execute("UPDATE Products SET price = %s WHERE id = %s", (price, id))
                    self.connection.commit()
                if quant != 0:
                    cursor.execute("UPDATE Products SET quantity = %s WHERE id = %s", (quant, id))
                    self.connection.commit()
                if supplier != '':
                    cursor.execute("UPDATE Products SET supplier = %s WHERE id = %s", (supplier, id))
                    self.connection.commit()
                cursor.close()

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()

class ViewProd:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("1350x700")
        self.root.title('View Products')

        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='VIEW PRODUCTS', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=555, y=15)

        style = ttk.Style()
        style.configure("Treeview", font  = ('Roboto', 15, 'bold'))
        style.configure("Treeview.Heading", font = ('Roboto', 20, 'bold'))

        table = ttk.Treeview(columns=('id', 'name', 'sku', 'price', 'quantity', 'supplier'), show = 'headings')
        table.heading('id', text='ID')
        table.heading('name', text='Name')
        table.heading('sku', text='SKU')
        table.heading('price', text='Price')
        table.heading('quantity', text='Quantity')
        table.heading('supplier', text='Supplier')
        table.pack(side=TOP, fill = BOTH, expand = True)

        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM Products ORDER BY id ASC')

        rows = cursor.fetchall()

        if rows != []:
            for row in rows:
                table.insert('', index = END, values = row)
        else:
            messagebox.showinfo(parent = self.root, message = 'No Product Found', title = 'Info')

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()


class RecSale:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("800x600")
        self.root.title('Record Sales')

        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='RECORD SALE', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=295, y=15)

        # Product id
        self.prod_id = IntVar()
        Label(self.root, text = "Product ID: ", font = ('Roboto', 20, 'bold')).place(x = 190, y = 90)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.prod_id).place(x = 350, y = 90, width = 250, height = 40)

        # Customer Name
        self.cust_name = StringVar()
        Label(self.root, text = "Customer Name: ", font = ('Roboto', 20, 'bold')).place(x = 140, y = 140)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.cust_name).place(x = 370, y = 140, width = 280, height = 40)

        # Quantity
        self.qnt_sold = IntVar()
        Label(self.root, text = "Quantity: ", font = ('Roboto', 20, 'bold')).place(x = 190, y = 190)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.qnt_sold).place(x = 330, y = 190, width = 270, height = 40)

        # Date
        self.date_var = StringVar()
        Label(self.root, text = "Date (YYYY-MM-DD): ", font = ('Roboto', 20, 'bold')).place(x = 100, y = 240)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.date_var).place(x = 380, y = 240, width = 290, height = 40)

        # Amount
        self.amnt_var = DoubleVar()
        Label(self.root, text = "Total Amount: ", font = ('Roboto', 20, 'bold')).place(x = 150, y = 290)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable = self.amnt_var).place(x = 360, y = 290, width = 290, height = 40)

        Button(self.root, text='Record Sale ->', font=('Roboto', 25, 'bold'), fg='white', bg='green', bd=5, command = self.record_sale).place(x=260, y=457)

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def record_sale(self):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM Products WHERE id = %s', (self.prod_id.get(),))
        if cursor.fetchone() == None:
            messagebox.showerror('Error', 'Product not found.')
        else:
            cursor.execute('SELECT quantity FROM Products WHERE id = %s', (self.prod_id.get(),))
            quantity = cursor.fetchone()[0]
            if quantity < self.qnt_sold.get():
                messagebox.showerror('Error', 'Not enough stock.')
            else:
                prod_id = self.prod_id.get()
                customer_name = self.cust_name.get()
                quantity_sold = self.qnt_sold.get()
                total_amount = self.amnt_var.get()
                date = self.date_var.get()
                cursor.execute("INSERT INTO Sales (product_id, quantity_sold, sale_date, total_amount, customer_name) VALUES (%s, %s, %s, %s, %s)", (prod_id, quantity_sold, date, total_amount, customer_name))
                self.connection.commit()
                cursor.execute("UPDATE Products SET quantity = quantity - %s WHERE id = %s", (quantity_sold, prod_id))
                self.connection.commit()
                messagebox.showinfo('Success', 'Sale recorded successfully.')
                


    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()

class ViewSales:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("1350x700")
        self.root.title('View Sales')   

        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='VIEW SALES', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=555, y=15)

        style = ttk.Style()
        style.configure("Treeview", font  = ('Roboto', 15, 'bold'))
        style.configure("Treeview.Heading", font = ('Roboto', 20, 'bold'))

        table = ttk.Treeview(columns=('id', 'prod_id', 'qnt_sold', 'saledate', 'totalamount', 'cust_name'), show = 'headings')
        table.heading('id', text='ID')
        table.heading('prod_id', text='Product ID')
        table.heading('qnt_sold', text='Quantity Sold')
        table.heading('saledate', text='Sale Date')
        table.heading('totalamount', text='Total Amount')
        table.heading('cust_name', text = 'Customer Name')
        table.pack(side=TOP, fill = BOTH, expand = True)

        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM Sales ORDER BY id ASC')

        rows = cursor.fetchall()

        if rows != []:
            for row in rows:
                table.insert('', index = END, values = row)
        else:
            messagebox.showinfo(parent = self.root, message = 'No Sale Found', title = 'Info')

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()

class ViewOrders:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("1350x700")
        self.root.title('View Orders')

        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='VIEW ORDERS', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=555, y=15)

        style = ttk.Style()
        style.configure("Treeview", font  = ('Roboto', 15, 'bold'))
        style.configure("Treeview.Heading", font = ('Roboto', 20, 'bold'))

        table = ttk.Treeview(columns = ('id', 'prod_id', 'qnt_ordered', 'order_date', 'status'), show = 'headings')
        table.heading('id', text='ID')
        table.heading('prod_id', text='Product ID')
        table.heading('qnt_ordered', text='Quantity Ordered')
        table.heading('order_date', text='Order Date')
        table.heading('status', text='Status')
        table.pack(side=TOP, fill = BOTH, expand = True)

        cursor = self.connection.cursor()
        
        cursor.execute('SELECT * FROM Orders ORDER BY id ASC')
        rows = cursor.fetchall()
        
        if rows != []:
            for row in rows:
                table.insert('', index = END, values = row)
        else:
            messagebox.showinfo(parent = self.root, message = 'No Order Found', title = 'Info')


        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()

class RecOrder:
    def __init__(self, root, connection, username):
        self.root = root
        self.connection = connection
        self.username = username

        self.root.geometry("800x500")
        self.root.title('Record Order')

        strip = Frame(self.root, bg='#020328', height=70)
        strip.pack(side=TOP, fill=X)
        Label(strip, text='RECORD ORDER', font=("Roboto", 20, 'bold'), bg='#020328', fg='white').place(x=295, y=15)

        self.prod_id = IntVar()
        Label(self.root, text = 'Product ID: ', font=('Roboto', 20, 'bold')).place(x = 180, y = 90)
        Entry(self.root, textvariable = self.prod_id, font=('Roboto', 20, 'bold'), bg= 'lightyellow', bd = 5).place(x = 330, y = 90, width = 280, height = 40)

        self.qnt_ordered = IntVar()
        Label(self.root, text = 'Quantity Ordered: ', font=('Roboto', 20, 'bold')).place(x = 130, y = 140)
        Entry(self.root, bg = 'lightyellow', bd = 5, font = ('Roboto', 20, 'bold'), textvariable= self.qnt_ordered).place(x = 370, y = 140, width = 280, height = 40)

        self.order_date = StringVar()
        Label(self.root, text= 'Order Date: ', font= ('Roboto', 20, 'bold')).place(x = 175, y = 190)
        Entry(self.root, bg = 'lightyellow', bd = 5,font = ('Roboto', 20, 'bold'), textvariable= self.order_date).place(x =330, y = 190, width = 280, height = 40)

        Button(self.root, text='Record Order ->', font=('Roboto', 25, 'bold'), fg='white', bg='green', bd=5, command = self.record_order).place(x=260, y=357)

        self.root.protocol('WM_DELETE_WINDOW', self.on_closing)

    def record_order(self):
        if self.prod_id.get() == 0 or self.qnt_ordered.get() == 0 or self.order_date.get() == '':
            messagebox.showerror(parent = self.root, message = 'Please fill all the fields', title = 'Error')
        else:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Orders (product_id, quantity_ordered, order_date, status) VALUES (%s, %s, %s, 'Not Delivered')", (self.prod_id.get(), self.qnt_ordered.get(), self.order_date.get()))
            connection.commit()
            messagebox.showinfo(parent = self.root, message = 'Order recorded successfully', title = 'Success')
            self.prod_id.set(0)
            self.qnt_ordered.set(0)
            self.order_date.set('')

    def on_closing(self):
        self.root.destroy()
        new_root = Tk()
        obj = Home(new_root, self.connection, self.username)
        new_root.mainloop()


    
if __name__ == '__main__':

    inv_path = "Inventory"

    if not os.path.exists(inv_path):
        os.mkdir(inv_path)
    else:
        pass

    sale_path = "Sales"

    if not os.path.exists(sale_path):
        os.mkdir(sale_path)
    else:
        pass

    connection = connect_to_database()
    create_tables(connection)
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Orders')
    rows = cursor.fetchall()
    if  rows != []:
        cursor.execute("UPDATE Orders SET status = 'Delivered' WHERE order_date >= %s", (datetime.date.today(),))
        connection.commit()
        cursor.execute("UPDATE Orders SET status = 'Not Delivered' WHERE order_date < %s", (datetime.date.today(),))
        connection.commit()

        cursor.execute("SELECT product_id, quantity_ordered FROM Orders WHERE status = 'Delivered'")
        rows = cursor.fetchall()
        if rows != []:
            for row in rows:
                quantity_ordered = row[1]
                cursor.execute("UPDATE Products SET quantity = quantity + %s WHERE id = %s", (quantity_ordered, row[0]))
            connection.commit()

    root = Tk()
    obj = SignIn(root, connection)
    root.mainloop()
