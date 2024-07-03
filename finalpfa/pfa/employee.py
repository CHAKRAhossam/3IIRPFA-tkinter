from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import threading
import base64
from io import BytesIO
import re
from tkcalendar import DateEntry
import datetime
import csv



class employee:
    
    def __init__(self,root):
        self.root=root
        self.root.geometry("1500x790+0+0")
        self.root.title("face recognition system")
        self.setup_components()
        self.start_video_thread()
        self.dep_combo = None 
        self.poste_combo = None
        self.cntr_combo = None


    def fetch_contracts(self):
        """ Fetch contract types from the database and update the contract combobox. """
        try:
            # Assuming the database and a table with contract data are correctly set up
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="pfa_db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT contract_type FROM contracts")  # Adjust the query to match your table and column names
            contracts = cursor.fetchall()
            # Flatten the list of tuples and add 'Select Type' at the start
            contract_list = ['Select Type'] + [contract[0] for contract in contracts]
            self.cntr_combo['values'] = contract_list
            self.cntr_combo.current(0)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    def fetch_positions(self):
        """ Fetch position names from the database and update the position combobox. """
        try:
            # Assuming the database and a table with position data are correctly set up
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="pfa_db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT position_title FROM positions")  # Adjust the query to match your table and column names
            positions = cursor.fetchall()
            # Flatten the list of tuples and add 'Select Position' at the start
            position_list = ['Select Position'] + [pos[0] for pos in positions]
            self.poste_combo['values'] = position_list
            self.poste_combo.current(0)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    def fetch_departments(self):
        """ Fetch department names from the database and update the department combobox. """
        try:
            # Assuming the database 'face' is already created and has a table for departments
            conn = mysql.connector.connect(host="localhost", username="root", password="", database="pfa_db")
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT dept_name FROM departments")  # Adjust the column and table names based on your schema
            departments = cursor.fetchall()
            # Flatten the list of tuples and add 'Select Department' at the start
            department_list = ['Select Department'] + [dept[0] for dept in departments]
            self.dep_combo['values'] = department_list
            self.dep_combo.current(0)
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    def on_department_change(self, event=None):
        if self.dep_combo is None:
            print("dep_combo is not initialized.")
            return
        department = self.dep_combo.get()
        print("Department selected:", department)  # Check what department is selected
        if department != 'Select Department':
            self.fetch_positions(department)
        else:
            self.poste_combo['values'] = ['Select Position']
            self.poste_combo.current(0)

  
    def setup_components(self):
        #liste des variables

        self.var_dep=StringVar()
        self.var_poste=StringVar()
        self.var_date=StringVar()
        self.var_cntr=StringVar()
        self.va_std_id=IntVar()
        self.var_std_name=StringVar()
        self.var_email=StringVar()
        self.var_dob=StringVar()
        self.var_address=StringVar()
        self.var_phone=StringVar()
        self.var_gender=StringVar()
        self.var_status=StringVar()
        self.base64_string=""



        img0=Image.open(r"C:\Users\Dell\OneDrive\Desktop\finalpfa\finalpfa\pfa\interface_img\skybleu.png")
        img0=img0.resize((6000,6000))
        self.photoimg0=ImageTk.PhotoImage(img0)

        f_lbl=Label(self.root,image=self.photoimg0)
        f_lbl.place(x=0,y=0,width=1500,height=1300)
 
        title_lbl=Label(self.root,text="Employees management system " ,font=("Arial Bold",35,"bold"),fg="#FCEDDA",bg="#87CEEB")
        title_lbl.place(x=0,y=0,width=1550,height=60)

        main_frame=Frame(self.root,bd=2,bg="#FCEDDA")
        main_frame.place(x=20,y=110,width=1460,height=600)

        left_frame=LabelFrame(main_frame,bd=2,bg="#FCEDDA",relief=RIDGE,text="employees details",font=("Arial Bold",12,"bold"))
        left_frame.place(x=10,y=10,width=730,height=580)


        #departement
        dep_label=Label(left_frame,text="Departement",font=("Arial Bold",12,"bold"),bg="#FCEDDA")
        dep_label.grid(row=0,column=0,padx=10,pady=25,sticky=W)


        # Initialize self.dep_combo with proper configuration
        self.dep_combo = ttk.Combobox(left_frame, textvariable=self.var_dep, font=("Arial Bold", 12, "bold"), state="readonly")
        self.dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)
        self.fetch_departments()

    
        #poste occupe
        poste_label=Label(left_frame,text="poste occuppe",font=("Arial Bold",12,"bold"),bg="#FCEDDA")
        poste_label.grid(row=0,column=2,padx=10,pady=25,sticky=W)


        # Initialize self.poste_combo
        self.poste_combo = ttk.Combobox(left_frame, textvariable=self.var_poste, font=("Arial Bold", 12, "bold"), state="readonly")
        self.poste_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)
        self.fetch_positions()
        
        #date d'embauche

        date_label=Label(left_frame,text="Date d'embauche",font=("Arial Bold",12,"bold"),bg="#FCEDDA")
        date_label.grid(row=1,column=0,padx=10,pady=25,sticky=W)

        
        date_combo=ttk.Combobox(left_frame,textvariable=self.var_date,font=("Arial Bold",12,"bold"),state="readonly")
        date_combo["values"]=("select Year","2019-20","2020-21","2021-22","2022-23","2023-24")
        date_combo.current(0)
        date_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)


        
        
        #type de contrat

        cntr_label=Label(left_frame,text="Type de contrat",font=("Arial Bold",12,"bold"),bg="#FCEDDA")
        cntr_label.grid(row=1,column=2,padx=10,pady=25,sticky=W)    


        self.cntr_combo = ttk.Combobox(left_frame, textvariable=self.var_cntr, font=("Arial Bold", 12, "bold"), state="readonly")
        self.cntr_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)
        self.fetch_contracts()  # Call to populate the contracts combobox   


        #id
        id_label=Label(left_frame,text="Id : ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        id_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)
        id_label_entry=ttk.Entry(left_frame,width=20,textvariable=self.va_std_id,font=("Arial Bold",13,"bold"))
        id_label_entry.grid(row=2,column=1,padx=10,pady=25,sticky=W)
        
        #name
        Name_label=Label(left_frame,text=" Name : ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        Name_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)
        Name_label_entry=ttk.Entry(left_frame,width=20,textvariable=self.var_std_name,font=("Arial Bold",13,"bold"))
        Name_label_entry.grid(row=2,column=3,padx=10,pady=25,sticky=W)
        #email
        
        email_label=Label(left_frame,text="Email : ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)
        email_label_entry=ttk.Entry(left_frame,width=20,textvariable=self.var_email,font=("Arial Bold",13,"bold"))
        email_label_entry.grid(row=3,column=1,padx=10,pady=25,sticky=W)


        # Date of Birth
        birth_label = Label(left_frame, text="Date Of Birth :", font=("Arial Bold", 13, "bold"), bg="#FCEDDA")
        birth_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)
        birth_label_entry = DateEntry(left_frame, width=20, date_pattern='yyyy-mm-dd', textvariable=self.var_dob, font=("Arial Bold", 13))
        birth_label_entry.grid(row=3, column=3, padx=10, pady=25, sticky=W)

        #adresse

        adress_label=Label(left_frame,text="Address : ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        adress_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)
        adress_label_entry=ttk.Entry(left_frame,width=20,textvariable=self.var_address,font=("Arial Bold",13,"bold"))
        adress_label_entry.grid(row=4,column=1,padx=10,pady=25,sticky=W)
        #phone number
        phone_label=Label(left_frame,text="phone number : ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        phone_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)
        phone_label_entry=ttk.Entry(left_frame,width=20,textvariable=self.var_phone,font=("Arial Bold",13,"bold"))
        phone_label_entry.grid(row=4,column=3,padx=10,pady=25,sticky=W)
        #Gender


        gender_label=Label(left_frame,text="Gender : ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        gender_label.grid(row=5,column=0,padx=10,pady=25,sticky=W)
        
        gender_combo=ttk.Combobox(left_frame,textvariable=self.var_gender,font=("Arial Bold",13,"bold"),state="readonly")
        gender_combo["values"]=("select gender","male","female")
        gender_combo.current(0)
        gender_combo.grid(row=5,column=1,padx=2,pady=10,sticky=W) 

        #etat civil
        etat_label=Label(left_frame,text="Marital status: ",font=("Arial Bold",13,"bold"),bg="#FCEDDA")
        etat_label.grid(row=5,column=2,padx=10,pady=25,sticky=W)

        etat_combo=ttk.Combobox(left_frame,textvariable=self.var_status,font=("Arial Bold",13,"bold"),state="readonly")
        etat_combo["values"]=("select status","single","married","divorced")
        etat_combo.current(0)
        etat_combo.grid(row=5,column=3,padx=2,pady=10,sticky=W)

        #right frame 
        self.current_right_frame=LabelFrame(self.root,bd=2,bg="#FCEDDA",relief=RIDGE,text="live ",font=("Arial Bold",12,"bold"))
        self.current_right_frame.place(x=770,y=130,width=700,height=450)


        live_btn_frame=LabelFrame(self.root,bg="white",relief=RIDGE,font=("Arial Bold",12,"bold"))
        live_btn_frame.place(x=825,y=600,width=621,height=36)


        capture_btn = Button(live_btn_frame, text="Capture Image", command=self.capture_image,width=30,font=("Arial Bold",13,"bold"),bg="#87CEEB",fg="#FCEDDA")
        capture_btn.grid(row=0,column=0)

        takephoto_btn=Button(live_btn_frame,command=self.take_photo,text="batch and save",width=30,font=("Arial Bold",13,"bold"),bg="#87CEEB",fg="#FCEDDA")
        takephoto_btn.grid(row=0,column=1)

        #btns frame

        btn_frame=Frame(left_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=180,y=500,width=312,height=35)  

        reset_btn=Button(btn_frame,text="reset",command=self.reset_data,width=30,font=("Arial Bold",13,"bold"),bg="#87CEEB",fg="#FCEDDA")
        reset_btn.grid(row=0,column=3)


    def start_video_thread(self):
        thread = threading.Thread(target=self.start_video)
        thread.daemon = True  # Daemonize thread
        thread.start()

    def start_video(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Camera not accessible")
            return

        def video_stream():
            ret, frame = self.cap.read()
            if ret:
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                lbl_img.imgtk = imgtk  # Keep reference, avoid garbage collection
                lbl_img.config(image=imgtk)
                lbl_img.after(10, video_stream)
            else:
                print("Error: Frame capture failed")
                self.cap.release()

        lbl_img = Label(self.current_right_frame,bg="#FCEDDA")
        lbl_img.pack(expand=True, fill=BOTH)
        video_stream()  
    
    def capture_image(self):
        if self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                cv2.imwrite("captured_img.jpg", frame)  # Save the current frame to an image file
                self.open_cropping_tool(frame)
            else:
                messagebox.showerror("Error", "Failed to capture image")
        else:
            messagebox.showerror("Error", "Camera not accessible")
            
    def open_cropping_tool(self, img):
        # Window for cropping
        cv2.namedWindow("Crop Image")
        cv2.imshow("Crop Image", img)

        # Mouse callback function to get the cropping rectangle
        self.crop_rect = None

        def on_mouse(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.crop_rect = [x, y]  # Starting point
            elif event == cv2.EVENT_LBUTTONUP:
                self.crop_rect.extend([x, y])  # Ending point
                # Draw the rectangle to indicate the crop area
                cv2.rectangle(img, (self.crop_rect[0], self.crop_rect[1]), (self.crop_rect[2], self.crop_rect[3]), (0, 255, 0), 2)
                cv2.imshow("Crop Image", img)

        cv2.setMouseCallback("Crop Image", on_mouse)

        # Wait for 'c' to crop or 'q' to quit
        while True:
            k = cv2.waitKey(1) & 0xFF
            if k == ord('c') and self.crop_rect is not None:
                break
            elif k == ord('q'):
                cv2.destroyAllWindows()
                return

        # Crop and show cropped image
        if self.crop_rect:
            cropped_image = img[self.crop_rect[1]:self.crop_rect[3], self.crop_rect[0]:self.crop_rect[2]]
            cv2.imshow("Cropped Image", cropped_image)
            is_success, buffer = cv2.imencode(".png", cropped_image)
            if is_success:
                io_buf = BytesIO(buffer)
                self.base64_string = base64.b64encode(io_buf.getvalue()).decode('utf-8')
                print(self.base64_string)
            cv2.imwrite("cropped_img.jpg", cropped_image)  # Optionally save or further process
            cv2.waitKey(0)

        cv2.destroyAllWindows()
                      

        def on_closing(self):
           if self.video_capture.isOpened():
             self.video_capture.release()
             self.root.destroy()

             self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        return self.base64_string

    
#===============functions=================
    def validate_email(email):

        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, email):
           return True
        else:
            messagebox.showerror("Invalid Email", "Invalid email forme!")
            return False
        
    
    def validate_phone(phone_number):
        # This pattern matches phone numbers starting with +2126 or +2127 followed by 8 digits
        pattern = r'^\+212[67]\d{8}$'
        if re.match(pattern, phone_number):
            return True
        else:
            messagebox.showerror("Invalid Phone Number", "Invalid phone number form! (+2127/+2126 ........).")
            return False
        
    def validate_age(self, dob):
        # Convert the date of birth to a date object
        dob_date = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
        today = datetime.date.today()
        age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
        return age >= 18
        
    def add_data(self):
      
        phone = self.var_phone.get()
        if not employee.validate_phone(phone):
            return
      
        email = self.var_email.get()
        if not employee.validate_email(email):
            return
      
        dob = self.var_dob.get()
        if not self.validate_age(dob):
            messagebox.showerror("Error", "Employee must be at least 18 years old.")
            return

        if self.var_dep.get()=="select departement" or self.var_std_name.get()=="" or self.va_std_id.get()=="":
            messagebox.showerror("error","all fileds must be field",parent=self.root) 
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="",database="pfa_db")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into employee values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                        self.var_dep.get(),
                                                                                        self.var_poste.get(),
                                                                                        self.var_date.get(),
                                                                                        self.var_cntr.get(),
                                                                                        self.va_std_id.get(),
                                                                                        self.var_std_name.get(),
                                                                                        email,
                                                                                        dob,
                                                                                        self.var_address.get(),
                                                                                        phone,
                                                                                        self.var_gender.get(),
                                                                                        self.var_status.get(),
                                                                                        self.base64_string
                                                                                                                ))
                
                conn.commit()
                #self.fetch_data()
                conn.close()

                # Save ID, name, and email to CSV file
                data = [self.va_std_id.get(), self.var_std_name.get(), email]

                with open('employee_data.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(data)


                messagebox.showinfo("success","emmployee info added successfuly",parent=self.root)
            except Exception  as es :
                messagebox.showerror("error",f"Due To :{str(es)}",parent=self.root)


#=============reset button ===========================

    def reset_data(self):
        self.var_dep.set("Select Departement")
        self.var_poste.set("Select poste")
        self.var_date.set("Select date")
        self.va_std_id.set("")
        self.var_std_name.set("")
        self.var_email.set("")
        self.var_dob.set("")
        self.var_address.set("")
        self.var_phone.set("")
        self.var_gender.set("Select gender")
        self.var_status.set("Select status")

#=============take photo===================
    def take_photo(self):
        if self.var_dep.get() == "select departement" or self.var_std_name.get() == "":
            messagebox.showerror("error", "all fields must be filled", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="", database="pfa_db")
                my_cursor = conn.cursor() 
                my_cursor.execute("select * from employee")
                result = my_cursor.fetchall()

                my_cursor.execute(
                    "INSERT INTO employee ( dep, poste, date, contrat, name, email, dob, address, phone, gender, status, photo) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (
                        self.var_dep.get(),
                        self.var_poste.get(),
                        self.var_date.get(),
                        self.var_cntr.get(),
                        self.var_std_name.get(),
                        self.var_email.get(),
                        self.var_dob.get(),
                        self.var_address.get(),
                        self.var_phone.get(),
                        self.var_gender.get(),
                        self.var_status.get(),
                        self.base64_string
                    )
                )

                my_cursor.execute("select id from employee order by id desc limit 1")
                id = my_cursor.fetchone()[0]

            

                # Load pre-defined data from OpenCV
                try:
                    face_classifier = cv2.CascadeClassifier("C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\haarcascade_frontalface_default.xml")
                except cv2.error as e:
                    messagebox.showerror("Error", f"Failed to load face classifier: {e}", parent=self.root)

                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
                    for (x, y, w, h) in faces:
                        face_cropped = img[y:y+h, x:x+w]
                        return face_cropped

                cap = cv2.VideoCapture(0)
                img_id = 0

                while True:
                    ret, my_frame = cap.read()
                    if face_cropped(my_frame) is not None:
                        img_id += 1
                        face = face_cropped(my_frame)
                        face = cv2.resize(face, (450, 450))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                        file_name_path = f"C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\data\\data{id}.{img_id}.jpg"
                        cv2.imwrite(file_name_path, face)
                        cv2.putText(face, str(img_id), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 255, 0), 2)
                        cv2.imshow("cropped Face", face)

                        if cv2.waitKey(1) == 13 or int(img_id) == 20:
                            break

                # Save ID, name, and email to CSV file
                my_cursor.execute("select name from employee order by id desc limit 1")
                name = my_cursor.fetchone()[0]
                my_cursor.execute("select email from employee order by id desc limit 1")
                email = my_cursor.fetchone()[0]

                data = [id,'',name, '', email]  # Ensure that email is not empty

                conn.commit()
                self.reset_data()
                conn.close()

                # Use raw string to avoid invalid escape sequence warning
                with open(r'EmployeeDetails\EmployeeDetails.csv', 'a+', newline='') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(data)
                csvFile.close()

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("result", "generating data sets completed!")

            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

                                                                                                    



if __name__ == "__main__":
        root=Tk()
        obj=employee(root)
        root.mainloop()