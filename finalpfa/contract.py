import os
from customtkinter import *
from CTkTable import CTkTable
from PIL import Image
import mysql.connector
from mysql.connector import Error


# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

class DeleteButton(CTkButton):
    def __init__(self, master, row_id, command=None):
        super().__init__(master, text="Delete", fg_color="red", hover_color="darkred", command=command)
        self.row_id = row_id

class manag:
    
    def open_contractform(app):
        # This function will destroy the current CTk window and open a new script.
        app.destroy()
        os.system('python C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\contract_form.py')
    

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
        """Fetch employee data from the database and return it."""
        if self.conn is not None and self.conn.is_connected():
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT contract_id, Contract_type FROM pfa_db.contracts")
                result = cursor.fetchall()
                cursor.close()
                return result
            except Error as err:
                print(f"Error fetching data: {err}")
        return []
    
    
    def fetch_and_populate(self):
        data = self.fetch_data()
        if data:
            self.populate_table(data)



    def populate_table(self, data):
        """Create and populate the table."""
        # Create table frame
        table_frame = CTkScrollableFrame(master=self.main_view, fg_color="transparent")
        table_frame.pack(expand=True, fill="both", padx=27, pady=21)

        # Add headers
        headers = [["Contract ID", "Contract Type", "Action"]]
        header_frame = CTkTable(master=table_frame, values=headers ,header_color="#87CEEB")
        header_frame.pack(fill="x")

        # Add rows
        for row in data:
            row_frame = CTkFrame(master=table_frame, fg_color="transparent")
            row_frame.pack(fill="x", pady=5)

            for col in row:
                CTkLabel(master=row_frame, text=str(col), font=("Arial", 12) , justify = "center").pack(side="left", padx=(190,190))


            # Add delete button for each row
            btn_frame = CTkFrame(master=row_frame, fg_color="transparent")
            btn_frame.pack(side="left", padx=(130,130))

            btn = DeleteButton(master=btn_frame, row_id=row[0], command=lambda r=row[0]: self.delete_row(r))
            btn.pack(pady=5)

        # Set uniform column widths
        for _ in range(len(headers)):
            table_frame.columnconfigure(_, weight=1)


    def delete_row(self, row_id):
        """Delete a row from the database and refresh the table."""
        if self.conn is not None and self.conn.is_connected():
            try:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM pfa_db.contracts WHERE contract_id = %s", (row_id,))
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
        person_icon_path = os.path.join(current_dir, "person_icon.png")
        logistics_icon_path = os.path.join(current_dir, "smart.png")
        shipping_icon_path = os.path.join(current_dir, "company2.png")
        delivered_icon_path = os.path.join(current_dir, "adresse.png")

        logo_img_data = Image.open(logo_path)
        logo_img = CTkImage(dark_image=logo_img_data, light_image=logo_img_data, size=(77.68, 85.42))

        CTkLabel(master=sidebar_frame, text="", image=logo_img).pack(pady=(38, 0), anchor="center")

        employe_img_data = Image.open(employe_icon_path)
        employe_img = CTkImage(dark_image=employe_img_data, light_image=employe_img_data)

        CTkButton(master=sidebar_frame, image=employe_img, text="Employees", fg_color="transparent",
                font=("Arial Bold", 17), hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(46, 0))

        detect_img_data = Image.open(detect_path)
        detect_img = CTkImage(dark_image=detect_img_data, light_image=detect_img_data)



        CTkButton(master=sidebar_frame, image=detect_img, text="Face detector", fg_color="transparent",
                font=("Arial Bold", 17), hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        attandance_img_data = Image.open(attendance_path)
        attandance_img = CTkImage(dark_image=attandance_img_data, light_image=attandance_img_data)



        CTkButton(master=sidebar_frame, image=attandance_img, text="Attendance", fg_color="transparent",
                font=("Arial Bold", 17), hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))


        traindata_img_data = Image.open(traindata_path)
        traindata_img = CTkImage(dark_image=traindata_img_data, light_image=traindata_img_data)

        CTkButton(master=sidebar_frame, image=traindata_img, text="Training data", fg_color="transparent", font=("Arial Bold", 17)
                , hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        departement_img_data = Image.open(departement_path)
        departement_img = CTkImage(dark_image=departement_img_data, light_image=departement_img_data)

        CTkButton(master=sidebar_frame, image=departement_img, text="Departement", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        contrat_img_data = Image.open(contrat_path)
        contrat_img = CTkImage(dark_image=contrat_img_data, light_image=contrat_img_data)
        CTkButton(master=sidebar_frame, image=contrat_img, text="Contrat", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        poste_img_data = Image.open(poste_path)
        poste_img = CTkImage(dark_image=poste_img_data, light_image=poste_img_data)
        CTkButton(master=sidebar_frame, image=poste_img, text="Post", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(16, 0))

        person_img_data = Image.open(person_icon_path)
        person_img = CTkImage(dark_image=person_img_data, light_image=person_img_data)
        CTkButton(master=sidebar_frame, image=person_img, text="Logout", fg_color="transparent", font=("Arial Bold", 17),
                hover_color="#0463CA", anchor="w").pack(anchor="center", ipady=10, ipadx=15, pady=(100, 0))

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

        CTkLabel(master=title_frame, text="Contracts", font=("Arial Black", 25), text_color="#87CEEB").pack(anchor="nw", side="left")

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
                hover_color="#0463CA" , command=lambda: manag.open_contractform(app)).pack(anchor="ne", side="left", padx=(13, 0), pady=15)

        CTkLabel(master=search_container, text="ONLY ADMIN", font=("Arial Black", 15), 
                 text_color="#87CEEB").pack(anchor="ne", side="right", padx=(13, 13), pady=15)



if __name__ == "__main__":
        app=CTk()
        obj=manag(app)
        app.mainloop()

