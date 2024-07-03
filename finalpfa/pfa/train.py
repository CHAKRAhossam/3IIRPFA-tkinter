from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import cv2
import os
import numpy as np

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("525x400")
        self.root.title("Face Recognition System")

        # Title label
        title_lbl = Label(self.root, text="Training Data Set", font=("Arial Bold", 20, "bold"), fg="#FCEDDA", bg="#87CEEB")
        title_lbl.place(x=0, y=0, width=540, height=60)

        # Main frame
        main_frame = Frame(self.root, bd=2, bg="#FCEDDA")
        main_frame.place(x=30, y=70, width=460, height=300)

        # Left frame inside the main frame
        left_frame = LabelFrame(main_frame, bd=2, bg="#FCEDDA", relief=RIDGE, text="Train Data", font=("Arial Bold", 12, "bold"))
        left_frame.place(x=10, y=10, width=430, height=280)

        # Training button
        train_btn = Button(self.root, text="Start Training", command=self.train_classifier, cursor="hand2", font=("Arial Bold", 12, "bold"), bg="#87CEEB", fg="black")
        train_btn.place(x=150, y=200, width=223, height=35)

    def train_classifier(self):
        # Directory containing the training data
        data_dir = "C:\\Users\\Dell\\OneDrive\\Desktop\\finalpfa\\finalpfa\\pfa\\data"
        # List of all files in the directory
        path = [os.path.join(data_dir, file) for file in os.listdir(data_dir)]

        faces = []
        ids = []

        for image_path in path:
            # Convert the image to grayscale
            img = Image.open(image_path).convert("L")
            image_np = np.array(img, 'uint8')
            # Extract the ID from the image filename
            id = int(os.path.split(image_path)[1].split('.')[1])
            faces.append(image_np)
            ids.append(id)
            # Display the image during training
            cv2.imshow("Training", image_np)
            cv2.waitKey(1)

        ids = np.array(ids)

        # Train the LBPH recognizer and save the trained model
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.train(faces, ids)
        clf.write("classifier.xml")
        cv2.destroyAllWindows()

        # Show a message box indicating that training is complete
        self.root.after(1000, self.show_message)

    def show_message(self):
        messagebox.showinfo("Result", "Training completed")

if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()
