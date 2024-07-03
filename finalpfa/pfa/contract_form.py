from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

class Employee:

    def __init__(self, root):
        self.root = root
        self.root.geometry("525x400")
        self.root.title("Face Recognition System")
        self.setup_components()

    def setup_components(self):
        self.var_contract = StringVar()

        # Background Image
        img0 = PhotoImage(file="C:/Users/Dell/OneDrive/Desktop/finalpfa/finalpfa/pfa/interface_img/skybleu.png")
        img0 = img0.subsample(3, 3)  # Adjust the subsample as per your image size
        f_lbl = Label(self.root, image=img0)
        f_lbl.place(x=0, y=0)

        # Title Label
        title_lbl = Label(self.root, text="Contract Management System", font=("Arial Bold", 20, "bold"), fg="#FCEDDA", bg="#87CEEB")
        title_lbl.place(x=0, y=0, width=540, height=60)

        # Main Frame
        main_frame = Frame(self.root, bd=2, bg="#FCEDDA")
        main_frame.place(x=30, y=70, width=460, height=300)

        # Left Frame
        left_frame = LabelFrame(main_frame, bd=2, bg="#FCEDDA", relief=RIDGE, text="Contract", font=("Arial Bold", 12, "bold"))
        left_frame.place(x=10, y=10, width=430, height=280)

        # Contract Type Label and Entry
        contract_label = Label(left_frame, text="Contract Type:", font=("Arial Bold", 13, "bold"), bg="#FCEDDA")
        contract_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)
        contract_entry = ttk.Entry(left_frame, width=20, textvariable=self.var_contract, font=("Arial Bold", 13, "bold"))
        contract_entry.grid(row=2, column=3, padx=10, pady=25, sticky=W)

        # Buttons Frame
        btn_frame = Frame(left_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=100, y=150, width=223, height=35)

        # Save Button
        save_btn = Button(btn_frame, text="Save", command=self.add_contract, width=10, font=("Arial Bold", 13, "bold"), bg="#87CEEB", fg="#FCEDDA")
        save_btn.grid(row=0, column=1)

        # Reset Button
        reset_btn = Button(btn_frame, text="Reset", command=self.reset_data, width=10, font=("Arial Bold", 13, "bold"), bg="#87CEEB", fg="#FCEDDA")
        reset_btn.grid(row=0, column=3)

    def add_contract(self):
        if self.var_contract.get() == "":
            messagebox.showerror("Error", "All fields must be filled", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="pfa_db")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO contracts (contract_type) VALUES (%s)", (self.var_contract.get(),))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Contract added successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def reset_data(self):
        self.var_contract.set("")


if __name__ == "__main__":
    root = Tk()
    obj = Employee(root)
    root.mainloop()
