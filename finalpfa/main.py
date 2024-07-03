import os
import io
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import mysql.connector
from mysql.connector import Error
from base64 import b64decode
from PIL import Image, ImageTk
from tkinter import Tk, PhotoImage, Label
from os import system, remove
import base64
from io import BytesIO
from PIL import Image, ImageTk, UnidentifiedImageError  # Ensure you have Pillow installed
import tkinter as tk
from tkinter import messagebox


# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

class DeleteButton(CTkButton):
    def __init__(self, master, row_id, command=None):
        super().__init__(master, text="Delete", fg_color="red", hover_color="darkred", command=command)
        self.row_id = row_id

class manag:
    
    def open_employeeform(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\employee.py')


    def open_recog(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\recognizer.py')


    def open_train(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\train.py')


    def open_dept(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\dept.py')


    def open_contract(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\contract.py')


    def open_post(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\position.py')


    def open_employee(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\main.py')

    def open_attendance(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\attendance.py')

    def open_signin(window):
        window.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\signin.py')
        
    

    def __init__(self, app):
        self.app = app
        app.geometry("1510x760")
        app.resizable(0, 0)
        set_appearance_mode("light")

        self.conn = None
        self.setup_ui()
        self.database_connection()
        if self.conn and self.conn.is_connected():
            self.fetch_and_populate()

        # if self.conn and self.conn.is_connected():
        #     self.populate_table()

    def database_connection(self):
        """Establish a database connection and store it as an instance attribute."""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="",  # Adjust as per your configuration
                database="pfa_db"
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")
            self.conn = None

    def fetch_data(self):
        """Récupérer les données des employés depuis la base de données et les retourner."""
        if self.conn is not None and self.conn.is_connected():
            cursor = self.conn.cursor()
            cursor.execute("SELECT photo, id, name, email, phone, dep, poste FROM pfa_db.employee")
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    
    
    def fetch_and_populate(self):
        data = self.fetch_data()
        if data:
            self.populate_table(data)


   
    # def populate_table(self, data):
    #     """Create and populate the table."""
    #     initial_headers = [["Photo", "ID", "Name", "Email", "DOB", "Address", "Phone", "Department", "Post", "Contract"]]
    #     full_data = initial_headers + data  # Combine headers with data

    #     # Create table frame
    #     table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
    #     table_frame.pack(expand=True, fill="both", padx=27, pady=21)

    #     # Create and pack the table
    #     self.table = CTkTable(master=table_frame, values=full_data, colors=["#E6E6E6", "#EEEEEE"], header_color="#87CEEB", hover_color="#B4B4B4")
    #     self.table.edit_row(0, text_color="#FCEDDA", hover_color="#87CEEB")
    #     self.table.pack(expand=True)

    #     for row_index, row_data in enumerate(data):
    #         photo_data = row_data[0]  # Suppose that the photo is in the first column
    #         if photo_data:  # Check if photo data exists
    #             try:
    #                 while len(photo_data) % 4 != 0:
    #                     photo_data += '='
    #                 photo_bytes = b64decode(photo_data, validate=True)
    #                 if photo_bytes:
    #                     photo_image = Image.open(io.BytesIO(photo_bytes))
    #                     photo_tk = ImageTk.PhotoImage(photo_image)
    #                     photo_label = CTkLabel(master=self.table, image=photo_tk)
    #                     photo_label.image = photo_tk
    #                     # Set the widget in the cell
    #                     self.table.set_cell_widget(row_index, 0, photo_label)
    #             except Exception as e:
    #                 print("Erreur lors du décodage Base64 :", e)

    def add_base64_padding(self,base64_string):
        """Add padding to the base64 string if it's not correctly padded."""
        return base64_string + '==' * ((4 - len(base64_string) % 4) % 4)


    def populate_table(self, data):
        """Create and populate the table."""
        # Create table frame
        table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        # Add headers
        headers = [["Photo","id", "Name", "Email", "Phone", "Department", "Post", "Action"]]
        header_frame = CTkTable(master=table_frame, values=headers ,header_color="#87CEEB")
        header_frame.pack(fill="x")



        # Add rows
        for row in data:
            row_frame = CTkFrame(master=table_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)

            # Display photo from base64
            photo_data = row[0]  # Assuming the first column is the base64 string
            try:
                # Remove potential headers
                if photo_data.startswith('data:image'):
                    photo_data = photo_data.split(',', 1)[1]

                # Add padding if necessary
                photo_data = self.add_base64_padding(photo_data)

                image = Image.open(BytesIO(base64.b64decode(photo_data)))
                image.thumbnail((90, 90), Image.Resampling.LANCZOS)  # Resize image if necessary
                photo = ImageTk.PhotoImage(image)
                photo_label = CTkLabel(master=row_frame, image=photo, text='')
                photo_label.image = photo  # Keep a reference to avoid garbage collection
                photo_label.pack(side="left", expand=True, fill="both", padx=5)
            except (UnidentifiedImageError, ValueError, base64.binascii.Error) as e:
                print(f"Error decoding image: {e}")
                error_label = CTkLabel(master=row_frame, text="Image Error", font=("Arial", 12), text_color="red", justify="center")
                error_label.pack(side="left", expand=True, fill="both", padx=5)

            # Display the rest of the columns
            for col in row[1:]:
                CTkLabel(master=row_frame, text=str(col), font=("Arial", 12), justify="center",width=50).pack(side="left", expand=True, padx=5)

            # Add delete button for each row
            btn_frame = CTkFrame(master=row_frame, fg_color="transparent")
            btn_frame.pack(side="left", padx=5)

            btn = DeleteButton(master=btn_frame, row_id=row[1], command=lambda r=row[1]: self.delete_row(r))
            btn.pack(pady=5)

        # Set uniform column widths
        for i in range(len(headers)):
            table_frame.columnconfigure(i, weight=1)

    def delete_row(self, row_id):
        """Delete a row from the database and refresh the table."""
        if self.conn is not None and self.conn.is_connected():
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM pfa_db.employee WHERE id = %s", (row_id,))
                self.conn.commit()
                cursor.close()
                print(f"Row with ID {row_id} deleted successfully")

                # Clear the existing table frame
                for widget in self.app.winfo_children():
                    widget.destroy()

                # Fetch and populate the table with updated data
                self.setup_ui()
                self.fetch_and_populate()
            except Error as err:
                print(f"Error deleting row: {err}")



    def setup_ui(self):


        sidebar_frame = CTkFrame(master=app, fg_color="#87CEEB", width=245, height=745, corner_radius=0)
        sidebar_frame.pack_propagate(0)
        sidebar_frame.pack(fill="y", anchor="w", side="left")

        # Specify the paths to the image files
        logo_path = os.path.join(current_dir, "logo.png")
        employe_icon_path = os.path.join(current_dir, "C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\employe.png")
        detect_path=os.path.join(current_dir,"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\reconaissance.png")
        attendance_path=os.path.join(current_dir,"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\attandance.png")
        departement_path=os.path.join(current_dir,"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\departemant.png")
        traindata_path=os.path.join(current_dir,"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\traindata.png")
        contrat_path=os.path.join(current_dir,"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\contrat.png")       
        poste_path=os.path.join(current_dir,"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\poste.png") 
              
        package_icon_path = os.path.join(current_dir, "package_icon.png")
        list_icon_path = os.path.join(current_dir, "list_icon.png")
        returns_icon_path = os.path.join(current_dir, "returns_icon.png")
        settings_icon_path = os.path.join(current_dir, "settings_icon.png")
        person_icon_path = os.path.join(current_dir, "person_icon.png")
        logistics_icon_path = os.path.join(current_dir, "smart.png")
        shipping_icon_path = os.path.join(current_dir, "company2.png")
        delivered_icon_path = os.path.join(current_dir, "adresse.png")

        logo_img_data = Image.open(logo_path)
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        employe_img_data = Image.open(employe_icon_path)
        employe_img = CTkImage(dark_image=employe_img_data, light_image=employe_img_data)

        CTkButton(master=sidebar_frame, image=employe_img, text="Employee", fg_color="transparent",
                font=("Arial Bold", 17), hover_color="#0463CA", anchor="w", command=lambda: manag.open_employee(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(46, 0))

        detect_img_data = Image.open(detect_path)
        detect_img = CTkImage(dark_image=detect_img_data, light_image=detect_img_data)



        CTkButton(master=sidebar_frame, image=detect_img, text="Face detector", fg_color="transparent",
                font=("Arial Bold", 17), hover_color="#0463CA", anchor="w", command=lambda: manag.open_recog(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        attandance_img_data = Image.open(attendance_path)
        attandance_img = CTkImage(dark_image=attandance_img_data, light_image=attandance_img_data)


        CTkButton(master=sidebar_frame, image=attandance_img, text="Attendance", fg_color="transparent",
                font=("Arial Bold", 17), hover_color="#0463CA", anchor="w", command=lambda: manag.open_attendance(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))


        traindata_img_data = Image.open(traindata_path)
        traindata_img = CTkImage(dark_image=traindata_img_data, light_image=traindata_img_data)

        CTkButton(master=sidebar_frame, image=traindata_img, text="Training data", fg_color="transparent", font=("Arial Bold", 17)
                , hover_color="#0463CA", anchor="w", command=lambda: manag.open_train(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        departement_img_data = Image.open(departement_path)
        departement_img = CTkImage(dark_image=departement_img_data, light_image=departement_img_data)

        CTkButton(master=sidebar_frame, image=departement_img, text="Departement", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w", command=lambda: manag.open_dept(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        contrat_img_data = Image.open(contrat_path)
        contrat_img = CTkImage(dark_image=contrat_img_data, light_image=contrat_img_data)
        CTkButton(master=sidebar_frame, image=contrat_img, text="Contrat", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        poste_img_data = Image.open(poste_path)
        poste_img = CTkImage(dark_image=poste_img_data, light_image=poste_img_data)
        CTkButton(master=sidebar_frame, image=poste_img, text="Post", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w", command=lambda: manag.open_post(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        person_img_data = Image.open(person_icon_path)
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=sidebar_frame, image=person_img, text="Logout", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w", command=lambda: manag.open_signin(app)).pack(anchor="center", ipady=10, ipadx=15, pady=(100, 0))

        self.main_view = CTkFrame(master=self.app, fg_color="#FCEDDA", width=1490 - 176, height=745, corner_radius=0)
        self.main_view.pack_propagate(0)
        self.main_view.pack(side="left")





        metrics_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        metrics_frame.pack(anchor="n", fill="x", padx=27, pady=(36, 0))

        orders_metric = CTkFrame(master=metrics_frame, fg_color="#87CEEB", width=200, height=60)
        orders_metric.grid_propagate(0)
        orders_metric.pack(side="left")

        logistics_img_data = Image.open(logistics_icon_path)
        logistics_img = CTkImage(light_image=logistics_img_data, dark_image=logistics_img_data, size=(43, 43))

        CTkLabel(master=orders_metric, image=logistics_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        CTkLabel(master=orders_metric, text="Face_Smart", text_color="#FCEDDA", font=("Arial Black", 15)).grid(row=0, column=1,
                                                                                                        sticky="sw")
        CTkLabel(master=orders_metric, text="AI app", text_color="#FCEDDA", font=("Arial Black", 15), justify="left").grid(row=1,
                                                                                                                        column=1,
                                                                                                                        sticky="nw",
                                                                                                                        pady=(0, 10))

        shipped_metric = CTkFrame(master=metrics_frame, fg_color="#87CEEB", width=200, height=60)
        shipped_metric.grid_propagate(0)
        shipped_metric.pack(side="left", expand=True, anchor="center")

        shipping_img_data = Image.open(shipping_icon_path)
        shipping_img = CTkImage(light_image=shipping_img_data, dark_image=shipping_img_data, size=(43, 43))

        CTkLabel(master=shipped_metric, image=shipping_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        CTkLabel(master=shipped_metric, text="Company", text_color="#FCEDDA", font=("Arial Black", 15)).grid(row=0, column=1,
                                                                                                        sticky="sw")
        CTkLabel(master=shipped_metric, text="Innovatix", text_color="#FCEDDA", font=("Arial Black", 15), justify="left").grid(row=1,
                                                                                                                    column=1,
                                                                                                                    sticky="nw",
                                                                                                                    pady=(0, 10))

        delivered_metric = CTkFrame(master=metrics_frame, fg_color="#87CEEB", width=200, height=60)
        delivered_metric.grid_propagate(0)
        delivered_metric.pack(side="right", )

        delivered_img_data = Image.open(delivered_icon_path)
        delivered_img = CTkImage(light_image=delivered_img_data, dark_image=delivered_img_data, size=(43, 43))

        title_frame = CTkFrame(master=self.main_view, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=27, pady=(29, 0))

        CTkLabel(master=title_frame, text="Employee", font=("Arial Black", 25), text_color="#87CEEB").pack(anchor="nw", side="left")

        CTkLabel(master=delivered_metric, image=delivered_img, text="").grid(row=0, column=0, rowspan=2, padx=(12, 5), pady=10)

        CTkLabel(master=delivered_metric, text="Adress", text_color="#FCEDDA", font=("Arial Black", 15)).grid(row=0, column=1,
                                                                                                            sticky="sw")
        CTkLabel(master=delivered_metric, text="Marrakesh", text_color="#FCEDDA", font=("Arial Black", 15), justify="left").grid(row=1,
                                                                                                                        column=1,
                                                                                                                        sticky="nw",
                                                                                                                        pady=(0, 10))

        search_container = CTkFrame(master=self.main_view, height=50, fg_color="#F0F0F0")
        search_container.pack(fill="x", pady=(45, 0), padx=27)

        CTkButton(master=search_container, text="ADD", font=("Arial Black", 15), text_color="#FCEDDA", fg_color="#87CEEB",
                hover_color="#0463CA" , command=lambda: manag.open_employeeform(app)).pack(anchor="ne", side="left", padx=(13, 0), pady=15)

        CTkButton(master=search_container, text="Delete", font=("Arial Black", 15), text_color="#FCEDDA", fg_color="#87CEEB",
                hover_color="#0463CA").pack(anchor="ne", side="right", padx=(13, 13), pady=15)

        CTkButton(master=search_container, text="Update", font=("Arial Black", 15), text_color="#FCEDDA", fg_color="#87CEEB",
                hover_color="#0463CA").pack(anchor="ne", side="right", padx=(13, 0), pady=15)



if __name__ == "__main__":
        app=CTk()
        obj=manag(app)
        app.mainloop()

