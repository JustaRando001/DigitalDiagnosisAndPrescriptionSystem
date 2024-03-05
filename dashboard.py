import tkinter as tk
from tkinter import ttk

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard App")
        self.root.geometry("800x600")

        # Create a sidebar
        self.sidebar = ttk.Frame(root)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.configure(style="Sidebar.TFrame")  # Set the style

        # Add sidebar elements (links to different pages)
        self.home_button = ttk.Button(self.sidebar, text="Home", command=self.show_home_page)
        self.page1_button = ttk.Button(self.sidebar, text="Page 1", command=self.show_page1)
        self.page2_button = ttk.Button(self.sidebar, text="Page 2", command=self.show_page2)
        self.page3_button = ttk.Button(self.sidebar, text="Page 3", command=self.show_page3)

        # Pack sidebar elements
        self.home_button.pack(fill="x")
        self.page1_button.pack(fill="x")
        self.page2_button.pack(fill="x")
        self.page3_button.pack(fill="x")

        # Create a container for page content
        self.page_container = ttk.Frame(root)
        self.page_container.pack(side="right", fill="both", expand=True)

        # Initialize the home page
        self.show_home_page()

        # Configure the style
        self.style = ttk.Style()
        self.style.configure("Sidebar.TFrame", background="gray")

    def show_home_page(self):
        # Display home page content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = ttk.Frame(self.root)
        ttk.Label(self.page_container, text="Welcome to the Home Page!").pack()
        self.page_container.pack(fill="both", expand=True)

    def show_page1(self):
        # Display Page 1 content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = ttk.Frame(self.root)
        ttk.Label(self.page_container, text="This is Page 1").pack()
        self.page_container.pack(fill="both", expand=True)

    def show_page2(self):
        # Display Page 2 content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = ttk.Frame(self.root)
        ttk.Label(self.page_container, text="Welcome to Page 2").pack()
        self.page_container.pack(fill="both", expand=True)

    def show_page3(self):
        # Display Page 3 content
        self.page_container.pack_forget()  # Hide previous page
        self.page_container = ttk.Frame(self.root)
        ttk.Label(self.page_container, text="Page 3 content goes here").pack()
        self.page_container.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = DashboardApp(root)
    root.mainloop()
