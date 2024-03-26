import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3
from algorithm import predict_diagnosis

class MainPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Main Page")
        self.geometry("800x600")
        self.conn = sqlite3.connect('users.db')  # Creates a disk-based database named users.db
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                               (username text primary key, password text)''')  # Creates a table to store user information if it doesn't exist
        tk.Button(self, text="Register", command=self.open_register).pack()
        tk.Button(self, text="Sign In", command=self.open_signin).pack()

    def open_register(self):
        self.withdraw()  # This will hide the main window
        RegisterPage(self)

    def open_signin(self):
        self.withdraw()  # This will hide the main window
        SignInPage(self)

class RegisterPage(tk.Toplevel):
    def __init__(self, main_page):
        tk.Toplevel.__init__(self)
        self.title("Register Page")
        self.geometry("800x600")
        self.main_page = main_page
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        tk.Button(self, text="Register", command=self.register).pack()
        tk.Button(self, text="Go back to Main Page", command=self.go_back).pack()

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.main_page.cursor.execute("INSERT INTO users VALUES (?, ?)", (username, password))  # Stores the user information in the database
            self.main_page.conn.commit()  # Commits the changes to the database
            messagebox.showinfo("Success", "Registration successful!")
            self.go_back()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def go_back(self):
        self.destroy()  # This will destroy the current window
        self.main_page.deiconify()  # This will show the hidden main window

class SignInPage(tk.Toplevel):
    def __init__(self, main_page):
        tk.Toplevel.__init__(self)
        self.title("Sign In Page")
        self.geometry("800x600")
        self.main_page = main_page
        tk.Label(self, text="Username:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()
        tk.Label(self, text="Password:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        tk.Button(self, text="Sign In", command=self.signin).pack()
        tk.Button(self, text="Go back to Main Page", command=self.go_back).pack()

    def signin(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.main_page.cursor.execute("SELECT password FROM users WHERE username=?", (username,))
            result = self.main_page.cursor.fetchone()
            if result is not None and result[0] == password:
                messagebox.showinfo("Success", "Sign in successful!")
                self.destroy()  # This will destroy the current window
                HomePage(self.main_page, username)  # Open the home page
            else:
                messagebox.showerror("Error", "Invalid username or password!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def go_back(self):
        self.destroy()  # This will destroy the current window
        self.main_page.deiconify()  # This will show the hidden main window

class HomePage(tk.Toplevel):
    def __init__(self, main_page, username):
        tk.Toplevel.__init__(self)
        self.main_page = main_page
        self.username = username
        self.title("Home Page")
        self.geometry("800x600")

        # Create a sidebar
        self.sidebar = tk.Frame(self)
        self.sidebar.pack(side="left", fill="y")

        # Add sidebar elements (links to different pages)
        self.home_button = tk.Button(self.sidebar, text="Home", command=self.show_home_page)
        self.page1_button = tk.Button(self.sidebar, text="Patient Details", command=self.show_page1)
        self.page2_button = tk.Button(self.sidebar, text="Appointments", command=self.show_page2)
        self.page3_button = tk.Button(self.sidebar, text="Diagnosis", command=self.show_page3)

        # Pack sidebar elements
        self.home_button.pack(fill="x")
        self.page1_button.pack(fill="x")
        self.page2_button.pack(fill="x")
        self.page3_button.pack(fill="x")

        # Create a container for page content
        self.page_container = tk.Frame(self)
        self.page_container.pack(side="right", fill="both", expand=True)

        # Initialize the home page
        self.show_home_page()

        # Add signout button
        self.signout_button = tk.Button(self, text="Sign Out", command=self.sign_out)
        self.signout_button.pack(side="top", anchor="ne")  # Top right corner

    def show_home_page(self):
        # Display home page content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = tk.Frame(self)
        tk.Label(self.page_container, text=f"Welcome Doctor {self.username}!").pack()

        fields = ["Appointment_ID", "Patient_ID"]
        self.entries = {}
        for field in fields:
            row = tk.Frame(self.page_container)
            row.pack(side="top", fill="x", padx=5, pady=5)
            label = tk.Label(row, text=field, anchor="w")
            entry = tk.Entry(row)
            label.pack(side="left")
            entry.pack(side="right", expand=True, fill="x")
            self.entries[field] = entry

        # Add submit button
        tk.Button(self.page_container, text="Submit", command=self.submit_home).pack()

        self.page_container.pack(fill="both", expand=True)

    def submit_home(self):
        # Get form values
        values = {field: entry.get() for field, entry in self.entries.items()}

        # Check if any field is empty
        for field, value in values.items():
            if not value:
                messagebox.showerror("Error", f"{field.replace('_', ' ')} field cannot be empty.")
                return

        # Connect to the appointments database
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()

        # Query the appointments table for the entered fields
        try:
            cursor.execute(f"SELECT symptoms FROM appointments WHERE appointment_id = :Appointment_ID AND patient_id = :Patient_ID", values)
            result = cursor.fetchone()
            if result is not None:
                symptoms = result[0]
                diagnosis = predict_diagnosis(symptoms)
                self.create_info_page(symptoms, diagnosis)
            else:
                messagebox.showerror("Error", "No matching record found.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def create_info_page(self, symptoms, diagnosis):
        # Create a new Toplevel widget (this will be a new window)
        info_page = tk.Toplevel(self)
        info_page.title("Appointment Information")

        # Add labels to display the symptoms and diagnosis
        symptoms_label = tk.Label(info_page, text=f"Symptoms: {symptoms}")
        symptoms_label.pack()

        diagnosis_label = tk.Label(info_page, text=f"Predicted Diagnosis: {diagnosis}")
        diagnosis_label.pack()

    def show_page1(self):
        # Display Page 1 content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = tk.Frame(self)
        tk.Label(self.page_container, text="Patient Details").pack()

        # Create form fields
        fields = ["Patient_ID", "Patient_Name", "Patient_Date_of_Birth", "Patient_Gender", "Patient_Height(cm)", "Patient_Weight(kg)", "Patient_Blood_Type"]
        self.entries = {}
        for field in fields:
            row = tk.Frame(self.page_container)
            row.pack(side="top", fill="x", padx=5, pady=5)
            label = tk.Label(row, text=field, anchor="w")
            entry = tk.Entry(row)
            label.pack(side="left")
            entry.pack(side="right", expand=True, fill="x")
            self.entries[field] = entry

        # Add submit button
        tk.Button(self.page_container, text="Submit", command=self.submit_details).pack()

        self.page_container.pack(fill="both", expand=True)

    def submit_details(self):
        # Get form values
        values = {field: entry.get() for field, entry in self.entries.items()}

        # Check if any field is empty
        for field, value in values.items():
            if not value:
                messagebox.showerror("Error", f"{field.replace('_', ' ')} field cannot be empty.")
                return

        # Connect to the patients database
        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()

        # Create the patients table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                name TEXT,
                dob TEXT,
                gender TEXT,
                height REAL,
                weight REAL,
                blood_type TEXT
            )
        ''')

        # Insert the form values into the patients table
        try:
            cursor.execute('''
                INSERT INTO patients (patient_id, name, dob, gender, height, weight, blood_type)
                VALUES (:Patient_ID, :Patient_Name, :Patient_Date_of_Birth, :Patient_Gender, :Patient_Height(cm), :Patient_Weight(kg), :Patient_Blood_Type)
            ''', values)

            # Commit the changes and close the connection
            conn.commit()
            messagebox.showinfo("Success", "Patient details have been saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def show_page2(self):
        # Display Page 2 content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = tk.Frame(self)
        tk.Label(self.page_container, text="Apointments").pack()
        self.page_container.pack(fill="both", expand=True)

        # Create form fields
        fields = ["Appointment_ID", "Patient_ID", "Diagnosis_Date", "Known_Symptoms", "Suspected_Disease", "Temperature(C)", "BPM"]
        self.entries = {}
        for field in fields:
            row = tk.Frame(self.page_container)
            row.pack(side="top", fill="x", padx=5, pady=5)
            label = tk.Label(row, text=field, anchor="w")
            entry = tk.Entry(row)
            label.pack(side="left")
            entry.pack(side="right", expand=True, fill="x")
            self.entries[field] = entry

        # Add submit button
        tk.Button(self.page_container, text="Submit", command=self.submit_appointment).pack()

        self.page_container.pack(fill="both", expand=True)

    def submit_appointment(self):
        # Get form values
        values = {field: entry.get() for field, entry in self.entries.items()}

        for field, value in values.items():
            if not value:
                messagebox.showerror("Error", f"{field.replace('_', ' ')} field cannot be empty.")
                return

        # Connect to the patients database
        conn = sqlite3.connect('appointments.db')
        cursor = conn.cursor()

        # Create the patients table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                patient_id INTEGER PRIMARY KEY,
                appointment_id TEXT,
                date TEXT,
                symptoms TEXT,
                disease TEXT,
                temp REAL,
                bpm REAL
            )
        ''')

        # Insert the form values into the patients table
        try:
            cursor.execute('''
                INSERT INTO appointments (patient_id, appointment_id, date, symptoms, disease, temp, bpm)
                VALUES (:Patient_ID, :Appointment_ID, :Diagnosis_Date, :Known_Symptoms, :Suspected_Disease, :Temperature(C), :BPM)
            ''', values)

            # Commit the changes and close the connection
            conn.commit()
            messagebox.showinfo("Success", "Appointment has been saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def show_page3(self):
        # Display Page 3 content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = tk.Frame(self)
        tk.Label(self.page_container, text="Welcome to the Diagnosis Page!").pack()
        self.page_container.pack(fill="both", expand=True)

        fields = ["Diagnosis", "Symptoms"]
        self.entries = {}
        for field in fields:
            row = tk.Frame(self.page_container)
            row.pack(side="top", fill="x", padx=5, pady=5)
            label = tk.Label(row, text=field, anchor="w")
            entry = tk.Entry(row)
            label.pack(side="left")
            entry.pack(side="right", expand=True, fill="x")
            self.entries[field] = entry

        # Add submit button
        tk.Button(self.page_container, text="Submit", command=self.submit_diagnosis).pack()

        self.page_container.pack(fill="both", expand=True)

    def submit_diagnosis(self):
        # Get form values
        values = {field: entry.get() for field, entry in self.entries.items()}

        for field, value in values.items():
            if not value:
                messagebox.showerror("Error", f"{field.replace('_', ' ')} field cannot be empty.")
                return

        # Connect to the patients database
        conn = sqlite3.connect('diagnosis.db')
        cursor = conn.cursor()

        # Create the patients table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS diagnosis (
                diagnoses TEXT,
                symptoms BLOB
            )
        ''')

        # Insert the form values into the patients table
        try:
            cursor.execute('''
                INSERT INTO diagnosis (diagnoses, symptoms)
                VALUES (:Diagnosis, :Symptoms)
            ''', values)

            # Commit the changes and close the connection
            conn.commit()
            messagebox.showinfo("Success", "Diagnosis has been saved successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def show_details(self):
        # Get the Patient ID from the entry field
        patient_id = self.patient_id_entry.get()

        # Retrieve patient details based on the provided Patient_ID
        patient_data = self.get_patient_details(patient_id)

        if patient_data:
            # Display patient details (customize as needed)
            messagebox.showinfo("Patient Details", f"Name: {patient_data['name']}\nDOB: {patient_data['dob']}\nGender: {patient_data['gender']}")
        else:
            messagebox.showerror("Error", f"No patient found with ID {patient_id}")

    def get_patient_details(self, patient_id):
        # Connect to the patients database
        conn = sqlite3.connect('patients.db')
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
            patient_data = cursor.fetchone()
            return patient_data
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()

    def sign_out(self):
        self.destroy()  # This will destroy the current window
        self.main_page.deiconify()  # This will show the hidden main window

if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
    app.conn.close()  # Closes the database connection when the program exits
