import mysql.connector
from datetime import datetime
from tkinter import messagebox

def connect_to_db():
    return mysql.connector.connect(host="localhost", username="root", password="", database="pfa_db")

def record_attendance(emp_id, action):
    db = connect_to_db()
    cursor = db.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if action == "check_in":
            cursor.execute("INSERT INTO attendance (employee_id, check_in) VALUES (%s, %s)", (emp_id, timestamp))
        elif action == "check_out":
            cursor.execute("UPDATE attendance SET check_out = %s WHERE employee_id = %s AND DATE(check_in) = DATE(%s)", (timestamp, emp_id, timestamp))
        db.commit()
        messagebox.showinfo("Success", f"Recorded {action} time for employee ID {emp_id}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to record {action}: {str(e)}")
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    # Example usage
    record_attendance(1, "check_in")
    record_attendance(1, "check_out")
