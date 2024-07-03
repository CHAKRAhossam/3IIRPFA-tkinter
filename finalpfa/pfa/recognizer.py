import os
import cv2
import numpy as np
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import tkinter.simpledialog as tsd
import cv2, os
import csv
import numpy as np
import pandas as pd
import datetime
import time

class Recognizer:
    def __init__(self, root):
        self.root = root
        self.root.geometry("925x500")
        self.root.title("Face Recognition System")

        title_lbl = Label(self.root, text="Face Detector", font=("Arial Bold", 20, "bold"), fg="#FCEDDA", bg="#87CEEB")
        title_lbl.place(x=0, y=0, width=925, height=60)

        # Frame for the Table
        table_frame = Frame(self.root, bd=2, bg="#FCEDDA")
        table_frame.place(x=10, y=70, width=550, height=500)

        # Left Frame for Table
        left_frame = LabelFrame(table_frame, bd=2, bg="#FCEDDA", relief=RIDGE, text="ATTENDANCE TABLE", font=("Arial Bold", 12, "bold"))
        left_frame.place(x=10, y=10, width=490, height=300)

        # Table (Treeview) with Scrollbar
        self.tv = ttk.Treeview(left_frame, height=13, columns=('name', 'date', 'time'))
        self.tv.column('#0', width=82)
        self.tv.column('name', width=130)
        self.tv.column('date', width=133)
        self.tv.column('time', width=133)
        self.tv.heading('#0', text='ID')
        self.tv.heading('name', text='NAME')
        self.tv.heading('date', text='DATE')
        self.tv.heading('time', text='TIME')
        self.tv.place(x=10, y=10, width=450, height=250)

        scroll = ttk.Scrollbar(left_frame, orient='vertical', command=self.tv.yview)
        scroll.place(x=460, y=10, height=250)
        self.tv.configure(yscrollcommand=scroll.set)

        # Frame for the Buttons
        button_frame = Frame(self.root, bd=2, bg="#FCEDDA")
        button_frame.place(x=560, y=70, width=360, height=500)

        right_frame = LabelFrame(button_frame, bd=2, bg="#FCEDDA", relief=RIDGE, text="CHECK IN / CHECK OUT", font=("Arial Bold", 12, "bold"))
        right_frame.place(x=10, y=10, width=320, height=300)

        # Buttons
        b1 = Button(button_frame, text="Check In", cursor="hand2", command=self.track_images, font=("Arial Bold", 12, "bold"), bg="#87CEEB", fg="black")
        b1.place(x=80, y=120, width=200, height=35)

    def check_haarcascadefile(self):
        exists = os.path.isfile("C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\haarcascade_frontalface_default.xml")
        if exists:
            return True
        else:
            messagebox.showerror(title='File Missing', message='The file haarcascade_frontalface_default.xml is missing.')
            return False


    def assure_path_exists(self, path):
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def track_images(self):
        self.check_haarcascadefile()
        self.assure_path_exists("Attendance/")
        self.assure_path_exists("EmployeeDetails/")
        for k in self.tv.get_children():
            self.tv.delete(k)
        msg = ''
        i = 0
        j = 0
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        exists3 = os.path.isfile("C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\TrainingImageLabel\\Trainner.yml")
        if exists3:
            recognizer.read("C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\TrainingImageLabel\\Trainner.yml")
        else:
            messagebox.showerror(title='Data Missing', message='Please click on Save Profile to reset data!!')
            return
        harcascadePath = "C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath);
        cam = cv2.VideoCapture(0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Id', '', 'Name', '', 'Date', '', 'Time']
        exists1 = os.path.isfile("C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\EmployeeDetails\\EmployeeDetails.csv")
        if exists1:
            df = pd.read_csv("C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\EmployeeDetails\\EmployeeDetails.csv")
        else:
            messagebox.showerror(title='Details Missing', message='Employee details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            return
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
                serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf < 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['ID'] == serial]['NAME'].values
                    ID = df.loc[df['ID'] == serial]['ID'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance = [str(ID), '', bb, '', str(date), '', str(timeStamp)]
                else:
                    Id = 'Unknown'
                    bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
            cv2.imshow('Taking Attendance', im)
            if cv2.waitKey(1) == ord('q'):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        exists = os.path.isfile(f"Attendance\\Attendance_{date}.csv")
        if exists:
            with open(f"Attendance\\Attendance_{date}.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)

        with open(f"Attendance\\Attendance_{date}.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if i > 1:
                    if i % 2 != 0:
                        iidd = str(lines[0]) + '   '
                        self.tv.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))

        csvFile1.close()
        cam.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = Tk()
    obj = Recognizer(root)
    root.mainloop()
