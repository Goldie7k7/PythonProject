import tkinter as tk
import sqlite3 as sql
from tkinter import ttk
from tkinter import messagebox

conn = sql.connect('LoginInfo.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL,
password BLOB NOT NULL)''')


main = tk.Tk()


def SIGNUP():
    def signupverify():
        user = username_entry.get()
        passkey = password_entry.get()

        def newPASS():
            con = sql.connect('Passwords.db')
            cur = con.cursor()
            website = tk.Entry(table)
            web = tk.Label(table,text="Website:")
            web.pack()            
            website.pack()
            userNAME = tk.Label(table,text="Username:")
            usernameMain = tk.Entry(table)
            userNAME.pack()
            usernameMain.pack()
            passWORD = tk.Label(table,text="Password:")
            passwordMain = tk.Entry(table)
            passWORD.pack()
            passwordMain.pack()

            def submit():
                WEBSITE = website.get()
                USERNAME = usernameMain.get()
                PASSWORD = passwordMain.get()
                cur.execute(f'''INSERT INTO {user}
                            (website,username,password)
                                VALUES(?,?,?)''',(WEBSITE,USERNAME,PASSWORD))
                website.delete(0,'end')
                usernameMain.delete(0,'end')
                passwordMain.delete(0,'end')                                
                con.commit()
                con.close()            

            Submit = tk.Button(table,text="Submit",command=submit)
            Submit.pack()
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS {user}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )''')

        if user == '' and passkey == '':
            messagebox.showerror('Error','Fields cannot be empty.')
    
        elif user != '' and passkey != '':
            messagebox.showinfo('Sign Up','Sign Up was successful')

            window.destroy()
            table = tk.Tk()
            table.configure(bg='white')
            Data_Title = tk.Label(table,text="Your Data:",font=('Arial',30))
            New_Entry = tk.Button(table,text="New",command=newPASS)
            View = tk.Button(table,text="View")
            Data_Title.pack()
            New_Entry.pack()
            View.pack()

            c.execute('''
            INSERT INTO users(username,password)
            VALUES(?,?)''',(user,passkey))
            conn.commit()
            conn.close()
            table.mainloop()

        else:
            messagebox.showerror("Error",'Incorrect username or password')
    main.destroy()
    window = tk.Tk()
    window.title("Password Manager")

    global user
    global password

    frame = tk.Frame(window)
    frame.pack()

    #Saving User Info
    User_Info_Frame = tk.LabelFrame(frame,text="User Information")
    User_Info_Frame.grid(row=0,column=0,padx=20,pady=20)

    username = tk.Label(User_Info_Frame, text="Username:")
    username.grid(row=0,column=0)
    password = tk.Label(User_Info_Frame, text="Password:")
    password.grid(row=1,column=0)

    username_entry = tk.Entry(User_Info_Frame)
    password_entry = tk.Entry(User_Info_Frame,show="*")
    username_entry.grid(row=0,column=1,padx=10,pady=10)
    password_entry.grid(row=1,column=1,padx=10,pady=10)

    button = tk.Button(window,text="Sign Up",command=signupverify)
    button.pack(pady=20)

    window.mainloop()

def LOGIN():
    def loginverify():
        user = username_entry.get()
        passkey = password_entry.get()

        def newPASS():
            con = sql.connect('Passwords.db')
            cur = con.cursor()
            website = tk.Entry(table)
            web = tk.Label(table,text="Website:")
            web.pack()            
            website.pack()
            userNAME = tk.Label(table,text="Username:")
            usernameMain = tk.Entry(table)
            userNAME.pack()
            usernameMain.pack()
            passWORD = tk.Label(table,text="Password:")
            passwordMain = tk.Entry(table)
            passWORD.pack()
            passwordMain.pack()

            def submit():
                WEBSITE = website.get()
                USERNAME = usernameMain.get()
                PASSWORD = passwordMain.get()
                cur.execute(f'''INSERT INTO {user}
                            (website,username,password)
                                VALUES(?,?,?)''',(WEBSITE,USERNAME,PASSWORD))
                website.delete(0,'end')
                usernameMain.delete(0,'end')
                passwordMain.delete(0,'end')
                con.commit()
                con.close()                                

            Submit = tk.Button(table,text="Submit",command=submit)
            Submit.pack()
            cur.execute(f'''
                CREATE TABLE IF NOT EXISTS {user}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )''')

        c.execute('SELECT 1 FROM users WHERE username = ? AND password = ? LIMIT 1', (user, passkey))
        resultuser = c.fetchone() is not None


        if resultuser:
            messagebox.showinfo('Login','Login was successful')

            window.destroy()
            table = tk.Tk()
            table.configure(bg='white')
            Data_Title = tk.Label(table,text="Your Data:",font=('Arial',30))
            New_Entry = tk.Button(table,text="New",command=newPASS)
            View = tk.Button(table,text="View")
            Data_Title.pack()
            New_Entry.pack()
            View.pack()
        else:
            messagebox.showerror("Error",'Incorrect username or password')
    main.destroy()
    window = tk.Tk()
    window.title("Password Manager")

    global username
    global password

    frame = tk.Frame(window)
    frame.pack()

    #Saving User Info
    User_Info_Frame = tk.LabelFrame(frame,text="User Information")
    User_Info_Frame.grid(row=0,column=0,padx=20,pady=20)

    username = tk.Label(User_Info_Frame, text="Username:")
    username.grid(row=0,column=0)
    password = tk.Label(User_Info_Frame, text="Password:")
    password.grid(row=1,column=0)

    username_entry = tk.Entry(User_Info_Frame)
    password_entry = tk.Entry(User_Info_Frame,show="*")
    username_entry.grid(row=0,column=1,padx=10,pady=10)
    password_entry.grid(row=1,column=1,padx=10,pady=10)

    button = tk.Button(window,text="Login",command=loginverify)
    button.pack(pady=20)
    #May need later
    #title = tk.Label(User_Info_Frame, text="Title")
    #title_combobox = ttk.Combobox(User_Info_Frame, values=[])

    window.mainloop()

LoginButton = tk.Button(main,text="Login",command=LOGIN)
LoginButton.pack()
SignUpButton = tk.Button(main,text="Sign Up",command=SIGNUP)
SignUpButton.pack()
main.mainloop()