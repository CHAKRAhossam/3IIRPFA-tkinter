from tkinter import * 
from tkinter import messagebox
import mysql.connector
import os
import hashlib


def open_signup(window):
    window.destroy()
    os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\signup.py')

def signin(window):
    username = user.get()
    password = code.get()

    # Check if username or password is empty
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    try:
        # Connect to MySQL database using XAMPP
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="",  
            database="pfa_db"  
        )

        cursor = db_connection.cursor()

        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username and password match in the database
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hashed_password))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Success", "Login Successful!")
            window.destroy()
            os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\main.py')
            # Perform further actions after login
        else:
            messagebox.showerror("Invalid", "Invalid username or password")

        

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", "Could not connect to the database.")



window=Tk()
window.title('login')
window.geometry('925x500+300+200')
window.configure(bg="#fff")
window.resizable(False,False)

img = PhotoImage(file=r"C:\Users\Dell\OneDrive\Desktop\finalpfa\finalpfa\pfa\interface_img\login.png")
Label(window,image=img,bg='white').place(x=50,y=50)

frame=Frame(window,width=350,height=350,bg="white")
frame.place(x=480,y=70)

heading=Label(frame,text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

# Username Entry and Label
def on_enter(e):
    user.delete(0, 'end')

def on_leave(e):
    name=user.get()
    if name=='':
        user.insert(0,'Username')

user = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=107)

# Password Entry and Label
def on_enter(e):
    code.delete(0, 'end')

def on_leave(e):
    name=code.get()
    if name=='':
        code.insert(0,'Password')

code = Entry(frame,width=25,fg='black',border=0,bg="white",font=('Microsoft YaHei UI Light',11))
code.place(x=30,y=150)
code.insert(0,'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)
Frame(frame,width=295,height=2,bg='black').place(x=25,y=177)

# Sign in Button
Button(frame,width=39,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0,command=lambda: signin(window)).place(x=35,y=204)

# Sign up Label and Button
label=Label(frame,text="Don't have an account?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9))
label.place(x=75,y=270)

sign_up = Button(frame,width=6,text='Sign up',border=0,bg='white',cursor='hand2',fg='#57a1f8', command=lambda: open_signup(window))
sign_up.place(x=215,y=270)

window.mainloop()
