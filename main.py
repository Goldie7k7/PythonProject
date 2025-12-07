import customtkinter as ctk
import sqlite3 as sql
from tkinter import ttk
from tkinter import messagebox
import csv

# Configure app appearance
ctk.set_appearance_mode("System")  # Can be "System", "Dark", or "Light"
ctk.set_default_color_theme("dark-blue")  # More modern theme

# Apply dark styling to Treeview
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
    background="#2b2b2b",
    foreground="white",
    fieldbackground="#2b2b2b",
    rowheight=30,
    font=('Arial', 12))
style.configure("Treeview.Heading",
    background="#1a1a1a",
    foreground="white",
    font=('Arial', 12, 'bold'))
style.map("Treeview", background=[('selected', '#3a7ebf')])

# Database setup
conn = sql.connect('LoginInfo.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password BLOB NOT NULL)''')

# Main application window
main = ctk.CTk()
main.title("Password Manager")
main.geometry("600x400")
main.resizable(False, False)

# Global variable for treeview
tree = None

def center_window(window, width, height):
    """Center the window on the screen"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def create_password_table(user):
    """Create password table for a new user"""
    con = sql.connect('Passwords.db')
    cur = con.cursor()
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS {user}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        website TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )''')
    con.commit()
    con.close()

def SIGNUP():
    """Open Sign Up window"""

    def signupverify():
        user = username_entry.get().strip()
        passkey = password_entry.get().strip()

        if not user or not passkey:
            messagebox.showerror('Error', 'Fields cannot be empty.')
            return

        # Check if username already exists
        c.execute('SELECT 1 FROM users WHERE username = ? LIMIT 1', (user,))
        if c.fetchone() is not None:
            messagebox.showerror('Error', 'Username already exists.')
            return

        # Create user account
        try:
            c.execute('INSERT INTO users(username,password) VALUES(?,?)', (user, passkey))
            conn.commit()
            create_password_table(user)     # REQUIRED FUNCTION
            messagebox.showinfo('Success', 'Account created successfully!')

            window.destroy()
            show_password_manager(user)     # OPEN MANAGER UI
        except Exception as e:
            messagebox.showerror('Error', f'Failed to create account: {str(e)}')

    main.withdraw()
    window = ctk.CTkToplevel(main)
    window.title("Sign Up")
    window.geometry("500x500")
    center_window(window, 500, 500)
    window.resizable(False, False)
    window.grab_set()  # Make window modal

    # Main frame
    frame = ctk.CTkFrame(window)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title
    ctk.CTkLabel(frame, text="Create Account", font=('Arial', 24, 'bold')).pack(pady=(10, 20))

    # Form frame
    form_frame = ctk.CTkFrame(frame, fg_color="transparent")
    form_frame.pack(fill="x", padx=20)

    # Username field
    ctk.CTkLabel(form_frame, text="Username:", font=('Arial', 14)).pack(anchor="w")
    username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter username")
    username_entry.pack(fill="x", pady=(0, 10))

    # Password field
    ctk.CTkLabel(form_frame, text="Password:", font=('Arial', 14)).pack(anchor="w")
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter password", show="*")
    password_entry.pack(fill="x", pady=(0, 20))

    # Sign up button
    ctk.CTkButton(frame, text="Sign Up", command=signupverify, font=('Arial', 16), height=45)\
        .pack(fill="x", padx=20)

    # Back button
    ctk.CTkButton(frame, text="Back",
                  command=lambda: [window.destroy(), main.deiconify()],
                  font=('Arial', 16), fg_color="transparent", border_width=1)\
        .pack(fill="x", padx=20, pady=(10, 0))

def LOGIN():
    """Login existing user"""

    def forgot_password():
        def retrieve():
            uname = uname_entry.get()
            if uname == '':
                messagebox.showwarning("Input Error", "Enter your username")
                return
            c.execute("SELECT password FROM users WHERE username = ?", (uname,))
            result = c.fetchone()
            if result:
                messagebox.showinfo("Password Found", f"Password: {result[0]}")
                top.destroy()
            else:
                messagebox.showerror("Not Found", "Username not found")

        top = ctk.CTkToplevel()
        top.title("Forgot Password")
        top.geometry("300x150")

        label = ctk.CTkLabel(top, text="Enter your username:")
        label.pack(pady=10)

        uname_entry = ctk.CTkEntry(top)
        uname_entry.pack(pady=5)

        retrieve_btn = ctk.CTkButton(top, text="Retrieve Password", command=retrieve)
        retrieve_btn.pack(pady=10)


    def loginverify():
        user = username_entry.get().strip()
        passkey = password_entry.get().strip()

        if not user or not passkey:
            messagebox.showerror("Error", "Fields cannot be empty.")
            return

        c.execute('SELECT 1 FROM users WHERE username = ? AND password = ? LIMIT 1', (user, passkey))
        if c.fetchone() is not None:
            messagebox.showinfo('Success', 'Login successful!')
            window.destroy()
            show_password_manager(user)
        else:
            messagebox.showerror("Error", 'Incorrect username or password')

    main.withdraw()
    window = ctk.CTkToplevel(main)
    window.title("Login")
    window.geometry("500x500")
    center_window(window, 500, 500)
    window.resizable(False, False)
    window.grab_set()  # Make window modal

    # Main frame
    frame = ctk.CTkFrame(window)
    frame.pack(pady=20, padx=20, fill="both", expand=True)

    # Title
    ctk.CTkLabel(frame, text="Login", font=('Arial', 20, 'bold')).pack(pady=(10, 20))

    # Form frame
    form_frame = ctk.CTkFrame(frame, fg_color="transparent")
    form_frame.pack(fill="x", padx=20)

    # Username field
    ctk.CTkLabel(form_frame, text="Username:", font=('Arial', 12)).pack(anchor="w")
    username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter username")
    username_entry.pack(fill="x", pady=(0, 10))

    # Password field
    ctk.CTkLabel(form_frame, text="Password:", font=('Arial', 12)).pack(anchor="w")
    password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter password", show="*")
    password_entry.pack(fill="x", pady=(0, 20))
    
    #forgot button
    forgot_btn = ctk.CTkButton(frame, text="Forgot Password?", command=forgot_password, font=('Arial', 14), height=40).pack(fill="x", padx=20, pady=(20,0))



    # Login button
    ctk.CTkButton(frame, text="Login", command=loginverify, font=('Arial', 14), height=40).pack(fill="x", padx=20 , pady=(10,0))

    # Back button
    ctk.CTkButton(frame, text="Back", command=lambda: [window.destroy(), main.deiconify()], 
                  font=('Arial', 18), fg_color="transparent", border_width=1).pack(fill="x", padx=20, pady=(5, 0))

def show_password_manager(user):
    """Show password manager interface"""

    # Open database for this user
    con = sql.connect("Passwords.db")
    cur = con.cursor()

    # Main window
    table = ctk.CTk()
    table.title(f"{user}'s Password Vault")
    table.geometry("800x600")
    center_window(table, 800, 600)

    # ----- HEADER -----
    header = ctk.CTkLabel(table, text=f"{user}'s Passwords", font=("Arial", 28, "bold"))
    header.pack(pady=20)

    # ----- TREEVIEW -----
    tree_frame = ctk.CTkFrame(table)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    tree = ttk.Treeview(tree_frame, columns=("ID","Website","Username","Password"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Website", text="Website")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")
    tree.pack(fill="both", expand=True)

    # Load initial data
    def refresh_treeview():
        for item in tree.get_children():
            tree.delete(item)
        cur.execute(f"SELECT * FROM {user}")
        rows = cur.fetchall()
        for row in rows:
            tree.insert("", "end", values=row)

    refresh_treeview()

    # ----- NEW ENTRY WINDOW -----
    def new_entry():
        nonlocal tree

        entry_window = ctk.CTkToplevel(table)
        entry_window.title("New Entry")
        entry_window.geometry("400x350")
        center_window(entry_window, 400, 350)
        entry_window.grab_set()

        frame = ctk.CTkFrame(entry_window)
        frame.pack(pady=20, padx=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="New Password Entry", font=('Arial', 18, 'bold')).pack(pady=(0, 20))

        # Form area
        form_frame = ctk.CTkFrame(frame, fg_color="transparent")
        form_frame.pack(fill="x")

        # Website
        ctk.CTkLabel(form_frame, text="Website:", font=('Arial', 12)).pack(anchor="w")
        website_entry = ctk.CTkEntry(form_frame, placeholder_text="e.g. google.com")
        website_entry.pack(fill="x", pady=(0, 10))

        # Username
        ctk.CTkLabel(form_frame, text="Username/Email:", font=('Arial', 12)).pack(anchor="w")
        username_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter username or email")
        username_entry.pack(fill="x", pady=(0, 10))

        # Password
        ctk.CTkLabel(form_frame, text="Password:", font=('Arial', 12)).pack(anchor="w")
        password_entry = ctk.CTkEntry(form_frame, placeholder_text="Enter password", show="*")
        password_entry.pack(fill="x", pady=(0, 20))

        # Submit new entry
        def submit():
            website = website_entry.get().strip()
            username_val = username_entry.get().strip()
            password_val = password_entry.get().strip()

            if not all([website, username_val, password_val]):
                messagebox.showwarning("Missing Info", "Please fill all fields")
                return

            try:
                cur.execute(
                    f"INSERT INTO {user} (website, username, password) VALUES (?, ?, ?)",
                    (website, username_val, password_val)
                )
                con.commit()
                messagebox.showinfo("Success", "Entry added successfully!")
                refresh_treeview()
                entry_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error adding entry: {str(e)}")

        # Submit button
        ctk.CTkButton(frame, text="Save Entry", command=submit, font=('Arial', 14), height=40)\
            .pack(fill="x", pady=(10, 0))
        
    def export_to_csv():
            try:
                filepath = ctk.filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV Files', '*.csv')])
                if not filepath:
                    return
                con = sql.connect('Passwords.db')
                cur = con.cursor()
                cur.execute(f"SELECT * FROM {user}")
                rows = cur.fetchall()
                with open(filepath, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['ID', 'Website', 'Username', 'Password'])
                    writer.writerows(rows)
                messagebox.showinfo('Success', 'Exported successfully!')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to export: {e}')
    def delete_entry():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an entry to delete.")
            return
        item = tree.item(selected[0])
        entry_id = item['values'][0]
        try:
            cur.execute(f"DELETE FROM {user} WHERE id = ?", (entry_id,))
            con.commit()
            tree.delete(selected[0])
            messagebox.showinfo("Deleted", "Entry deleted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete entry: {e}")

    def edit_entry():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an entry to edit.")
            return
        item = tree.item(selected[0])
        entry_id, old_site, old_user, old_pass = item['values']


        edit_win = ctk.CTkToplevel(table)
        edit_win.title("Edit Entry")
        edit_win.geometry("400x350")
        center_window(edit_win, 400, 350)
        edit_win.grab_set()


        frame = ctk.CTkFrame(edit_win)
        frame.pack(pady=20, padx=20, fill="both", expand=True)


        # Website
        ctk.CTkLabel(frame, text="Website:").pack(anchor="w")
        site_entry = ctk.CTkEntry(frame)
        site_entry.insert(0, old_site)
        site_entry.pack(fill="x", pady=(0, 10))


        # Username
        ctk.CTkLabel(frame, text="Username:").pack(anchor="w")
        user_entry = ctk.CTkEntry(frame)
        user_entry.insert(0, old_user)
        user_entry.pack(fill="x", pady=(0, 10))


        # Password
        ctk.CTkLabel(frame, text="Password:").pack(anchor="w")
        pass_entry = ctk.CTkEntry(frame, show="*")
        pass_entry.insert(0, old_pass)
        pass_entry.pack(fill="x", pady=(0, 20))


        def save_edit():
            new_site = site_entry.get().strip()
            new_user = user_entry.get().strip()
            new_pass = pass_entry.get().strip()
            if not all([new_site, new_user, new_pass]):
                messagebox.showwarning("Missing Info", "Please fill all fields.")
                return
            try:
                cur.execute(f"UPDATE {user} SET website = ?, username = ?, password = ? WHERE id = ?", (new_site, new_user, new_pass, entry_id))
                con.commit()
                tree.item(selected[0], values=(entry_id, new_site, new_user, new_pass))
                messagebox.showinfo("Updated", "Entry updated successfully!")
                edit_win.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {e}")


        ctk.CTkButton(frame, text="Save", command=save_edit).pack(fill="x")






    # ----- BUTTONS -----
    button_frame = ctk.CTkFrame(table)
    button_frame.pack(pady=15)

    ctk.CTkButton(button_frame, text="Add New Entry", command=new_entry, width=180).grid(row=0, column=0, padx=10)
    ctk.CTkButton(button_frame, text="Refresh", command=refresh_treeview, width=180).grid(row=0, column=1, padx=10)
    ctk.CTkButton(button_frame, text="Logout", command=lambda: [table.destroy(), main.deiconify()], width=180)\
        .grid(row=0, column=2, padx=10)
    ctk.CTkButton(button_frame,text="Export Data",command=export_to_csv,width=100).grid(row=0, column=3, padx=10)

    DeleteButton = ctk.CTkButton(button_frame, text="Delete Entry", command=delete_entry, width=180)
    DeleteButton.grid(row=0, column=4, padx=10)

    EditButton = ctk.CTkButton(button_frame, text="Edit Entry", command=edit_entry, width=180)
    EditButton.grid(row=0, column=5, padx=10)

    table.mainloop()

    # Connect to passwords database
    con = sql.connect('Passwords.db')
    cur = con.cursor()

    # Create main window
    table = ctk.CTk()
    table.title(f"Password Manager - {user}")
    table.geometry("900x600")
    center_window(table, 900, 600)

    # Main frame
    main_frame = ctk.CTkFrame(table)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Header
    header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    header_frame.pack(fill="x", pady=(0, 20))

    ctk.CTkLabel(header_frame, text="Your Passwords", font=('Arial', 24, 'bold')).pack(side="left")

    # Button frame
    button_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
    button_frame.pack(side="right")

    # New entry button
    ctk.CTkButton(button_frame, text="+ New Entry", command=new_entry, width=120).pack(side="left", padx=5)

    # Refresh button
    ctk.CTkButton(button_frame, text="Refresh", command=refresh_treeview, width=80).pack(side="left", padx=5)

    # Treeview frame
    tree_frame = ctk.CTkFrame(main_frame)
    tree_frame.pack(fill="both", expand=True)

    # Create treeview
    tree = ttk.Treeview(tree_frame, columns=('ID', 'Website', 'Username', 'Password'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Website', text='Website')
    tree.heading('Username', text='Username')
    tree.heading('Password', text='Password')
    
    # Set column widths
    tree.column('ID', width=50, anchor='center')
    tree.column('Website', width=200)
    tree.column('Username', width=200)
    tree.column('Password', width=200)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True)

    # Load initial data
    refresh_treeview()

    # Handle window close
    def on_close():
        con.close()
        table.destroy()
        main.destroy()

    table.protocol("WM_DELETE_WINDOW", on_close)
    table.mainloop()



# Main menu
main_frame = ctk.CTkFrame(main)
main_frame.pack(fill="both", expand=True, padx=50, pady=50)

# Title
ctk.CTkLabel(main_frame, text="Password Manager", font=('Arial', 28, 'bold')).pack(pady=(20, 40))

# Button frame
button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
button_frame.pack(pady=20)

# Buttons
LoginButton = ctk.CTkButton(button_frame, text="Login", command=LOGIN, width=200, height=40, font=('Arial', 14))
LoginButton.grid(row=0, column=0, padx=20, pady=10)

SignUpButton = ctk.CTkButton(button_frame, text="Sign Up", command=SIGNUP, width=200, height=40, font=('Arial', 14))
SignUpButton.grid(row=1, column=0, padx=20, pady=10)

QuitButton = ctk.CTkButton(main, text="Quit", command=main.destroy, width=150)
QuitButton.pack(pady=(10,20))
main.mainloop()

# Center the window
center_window(main, 600, 400)

# Start the application
main.mainloop()