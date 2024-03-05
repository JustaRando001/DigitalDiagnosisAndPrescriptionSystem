import tkinter as tk
import tkinter.messagebox as messagebox
import sqlite3

class MainPage(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Main Page")
        self.geometry("1080x720")
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
        self.title("Home Page")
        self.main_page = main_page
        tk.Label(self, text=f"Welcome, {username}!").pack()
        tk.Button(self, text="Sign Out", command=self.signout).pack()

    def signout(self):
        self.destroy()  # This will destroy the current window
        self.main_page.deiconify()  # This will show the hidden main window

if __name__ == "__main__":
    app = MainPage()
    app.mainloop()
    app.conn.close()  # Closes the database connection when the program exits
