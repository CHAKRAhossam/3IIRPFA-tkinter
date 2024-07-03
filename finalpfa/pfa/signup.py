from tkinter import *
from tkinter import messagebox
import mysql.connector
import re
import os
import hashlib


def open_signin(window):
    window.destroy()
    os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\signin.py')
    

def signup(window):
    # Get user inputs
    username = user.get()
    password = code.get()
    conf_pass = conf_code.get()
    email = email_entry.get()


    # Check if any field is empty
    if not all([username, password, conf_pass, email]):
        messagebox.showerror("Error", "All fields are required.")
        return

    # Check if passwords match
    if password != conf_pass:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    # Email validation pattern
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    # Check if email matches the pattern
    if not re.match(email_pattern, email):
        messagebox.showerror("Error", "Invalid email format.")
        return
    

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="pfa_db"
        )

        cursor = db_connection.cursor()

        # Create users table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        """)

        # Insert user data into the database
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        val = (username, hashed_password, email)
        cursor.execute(sql, val)
        db_connection.commit()

        messagebox.showinfo("Success", "Account created successfully.")

        # Clear the entry fields
        user.delete(0, END)
        code.delete(0, END)
        conf_code.delete(0, END)
        email_entry.delete(0, END)

        window.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\signin.py')

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", "Could not create account.")


window=Tk()
window. title("SignUp")
window. geometry ('925x500+300+200')
window.configure(bg='#fff')
window. resizable(False,False)


img = PhotoImage(file=r"C:\Users\Dell\OneDrive\Desktop\finalpfa\finalpfa\pfa\interface_img\signup.png")
Label(window, image=img, border=0,bg= 'white').place(x=50,y=90)
frame=Frame(window,width=350,height=450,bg= '#fff' )
frame.place(x=480,y=50)


heading=Label(frame, text='Sign up' ,fg="#57a1f8", bg= 'white',font=('Microsoft Yahei UI Light',23, 'bold'))
heading.place(x=100,y=5)

#######################################################################

def on_enter (e):
    user.delete(0, 'end')
def on_leave(e) :
    if user.get()=='' :
        user.insert(0, 'Username' )

user = Entry(frame, width=25,fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light' ,11))
user.place(x=30,y=60)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame (frame,width=295, height=2, bg= 'black' ).place(x=25,y=87)

########################################################################

def on_enter(e):
    email_entry.delete(0, 'end')
def on_leave(e) :
    if email_entry.get()=='' :
        email_entry.insert(0, 'Email' )

email_entry = Entry(frame, width=25,fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light' ,11))
email_entry.place(x=30,y=130)
email_entry.insert(0, 'Email')
email_entry.bind('<FocusIn>', on_enter)
email_entry.bind('<FocusOut>', on_leave)

Frame (frame,width=295, height=2, bg= 'black' ).place(x=25,y=157)

########################################################################

def on_enter (e):
    code.delete(0, 'end')
def on_leave(e) :
    if code.get()=='' :
        code.insert(0, 'Password' )

code = Entry(frame, width=25,fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light' ,11))
code.place(x=30,y=200)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame (frame,width=295, height=2, bg= 'black' ).place(x=25,y=227)


########################################################################

def on_enter (e):
    conf_code.delete(0, 'end')
def on_leave(e) :
    if conf_code.get()=='' :
        conf_code.insert(0, 'Confirm Password' )

conf_code = Entry(frame, width=25,fg='black', border=0, bg='white', font=('Microsoft Yahei UI Light' ,11))
conf_code.place(x=30,y=270)
conf_code.insert(0, 'Confirm Password')
conf_code.bind('<FocusIn>', on_enter)
conf_code.bind('<FocusOut>', on_leave)

Frame (frame,width=295, height=2, bg= 'black' ).place(x=25,y=297)

#########################################################################


Button (frame, width=39, pady=7, text= 'Sign up',bg='#57a1f8',fg='white', border=0,command=lambda: signup(window)).place (x=35,y=340)
label=Label(frame, text='I have an account' ,fg='black',bg='white',font=('Microsoft YaHei UI Light' ,9))
label.place(x=90,y=390)

sign_in=Button(frame, width=6, text= 'Sign in' ,border=0,bg= 'white',cursor='hand2',fg='#57a1f8',command=lambda: open_signin(window))
sign_in.place (x=200,y=390)


window.mainloop()