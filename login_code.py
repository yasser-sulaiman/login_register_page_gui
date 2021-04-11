import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql3

def loginf():
    conn = sql3.connect('login.db')
    #create cursor
    cursor = conn.cursor()
    
    #checking if the entered info are in the database or not
    cursor.execute("""
    SELECT email, password FROM pers_info
    WHERE password = :user_pass AND email = :user_email
    """,{'user_pass':password.get(), 'user_email':email.get()} )
    check = cursor.fetchall()
    if len(check) > 0:
        response = messagebox.showinfo('congrats', 'you have been loged in successfully')
        tk.Label(root, text = response).grid(row =1, column = 1, pady = 10)
    else:
        response = messagebox.showerror('Unvalid email or password', 'Please check your email and password')
    #closing the database
    conn.close()

    
def savef():
    #requirments for email and password to be satisfied
    if len(email_new.get())>5:
        if len(password_new.get())>=8:
            if password_new.get() == password_new_confirm.get():
                try:
                    conn = sql3.connect('login.db')
                    #create cursor
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO pers_info VALUES(:email_new, :password_new)
                        ''', {'email_new': email_new.get(),'password_new':password_new.get()})
                    #commit changes
                    conn.commit()
                    conn.close()
                    signup.destroy()
                except:
                    response = messagebox.showwarning('exist email', 'the email you have entered is already exists')               
            else:
                response = messagebox.showwarning('unmatched passwords', 'Please control your passwords')               
        else:
            response = messagebox.showwarning('Unvalid password', 'The password should be at least 8 charecters')           
    else:
        response = messagebox.showwarning('Unvalid Email', 'Please try with different email address')
        #tk.Label(signup, text = response).grid(row =1, column = 1, pady = 10)
        

def sign_up():
    global email_new
    global password_new, password_new_confirm
    global signup
    signup = tk.Toplevel()
    signup.title('sign up page')
    signup.geometry("250x250")

    #new email
    email_l = tk.Label(signup, text = "Email").grid(row = 1, column =0, pady = 10, stick='w')
    email_new = tk.Entry(signup)
    email_new.grid(row = 1, column = 1, pady = 10)
    
    #new password
    password_l = tk.Label(signup, text = "Password").grid(row = 2, column =0, pady = 10, stick='w')
    password_new = tk.Entry(signup, show='*')
    password_new.grid(row = 2, column = 1, pady = 10)

    #confirm password
    password_l_confirm = tk.Label(signup, text = "Confirm Password").grid(row = 3, column =0, pady = 10, stick='w')
    password_new_confirm = tk.Entry(signup, show='*')
    password_new_confirm.grid(row = 3, column = 1, pady = 10)

    #save button
    tk.Button(signup, text = 'save', command = savef, padx = 5).grid(row=4, column =1, pady = 10)


conn = sql3.connect('login.db')
#create cursor
cursor = conn.cursor()

#creating table if not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS pers_info (
email text unique,
password text)
""")
#commit changes
conn.commit()
conn.close()


root = tk.Tk()
root.title('login page')
root.geometry("200x250")

tk.Label(root, text = "Login page").grid(row = 0, column =1, columnspan = 2, pady = 10)
email = tk.Entry(root)
email.grid(row = 1, column = 1, pady = 10)
password = tk.Entry(root, show='*')
password.grid(row = 2, column = 1, pady = 10)

email_l = tk.Label(root, text = "Email").grid(row = 1, column =0, pady = 10)
password_l = tk.Label(root, text = "Password").grid(row = 2, column =0, pady = 10)

tk.Button(root, text = 'Login', command = loginf, padx = 5).grid(row=3, column =1, pady = 10)
tk.Button(root, text = 'sign up', command = sign_up).grid(row=4, column =1, pady = 10)

root.mainloop()
