from tkinter import *
from PIL import ImageTk,Image
from app import *
from time import sleep
from tkinter import font
import sqlite3
import re
import sys
#####-----GLOBAL VARIABLES-----####

bg_color='#355C7D'
global u_name
global u_pass

###--------Events for Login page-----------######

def clear_entry(event):
    if e_mail.get()=="email":
        e_mail.delete(0,"end")
        e_mail.insert(0,'')

def clear_entry1(event):
    if e_pass.get()=="password":
        e_pass.delete(0,"end")
        e_pass.insert(0,"")


def on_focusout(event):
    if e_mail.get()=="":
        e_mail.insert(0,"email")

def on_focusout1(event):
    if e_pass.get()=="":
        e_pass.insert(0,"password")


def set_user(event):
    e_mail.delete(0,"end")
    e_mail.insert(0,variable.get())

def clear_entries():
    e_mail.delete(0,"end")
    e_pass.delete(0,"end")
    e_mail.insert(0,"email")
    e_pass.insert(0,"password")

#Event for register----

def permit_register(event):

    u_name = e_mail.get()
    u_pass=e_pass.get()

    response = register(u_name,u_pass)
    if response=="Successfully registered":
        
        alert_box(response+" now login!")
    else:
        alert_box(response)

#Event for login---

def permit_login(event):


    u_name=e_mail.get()
    u_pass=e_pass.get()


    response = login(u_name,u_pass)

    if response[0]=="Successfully logined":
        global user_id
        user_id = response[1]
        user_name =response[2]
        
        account_window(user_id,user_name)
        clear_entries()
        root.destroy()
    else:
        alert_box(response[0])



##### --------------Main---------------#######

global root
global root1

root1=Tk()
root1.withdraw()

root=Toplevel()

root.geometry('600x500')
root.configure(bg=bg_color)
root.title('PassKeeper')
root.resizable(0,0)



title = LabelFrame(root,borderwidth=0,pady=20,bg=bg_color)
title.pack()

############ ------ Header ----------#################

label  = Label(title,text="PassKeeper",font=('Helvetice',44,'bold'),pady=10,bg=bg_color,fg='black')
label.pack()


#############---------Entries----------##############

entry_frame = Frame(root,borderwidth=0,bg=bg_color)
entry_frame.pack()

e_mail = Entry(entry_frame,bg="white",fg="black",font=('Helvetica',18,'bold'),borderwidth=2,bd=1)
e_mail.insert(0,"email")
e_mail.bind('<FocusIn>',clear_entry)
e_mail.bind('<FocusOut>',on_focusout)
e_mail.grid(row=0,column=1,pady=10)



e_pass = Entry(entry_frame,bg="white",fg="black",font=('Helvetica',18,'bold'),borderwidth=2,bd=1)
e_pass.insert(1,"password")
e_pass.bind('<FocusIn>',clear_entry1)
e_pass.bind('<FocusOut>',on_focusout1)
e_pass.grid(row=1,column=1)

###############-------Buttons----------############

global btn_frame
global label_error_frame

btn_frame = Frame(root,borderwidth=0,bg=bg_color)
btn_frame.pack()

btn_login = Button(btn_frame,text="Login",fg="black",bg="#18de39",padx=27,pady=12,font=('Helvetica',16,'bold'))
btn_login.bind('<Button-1>',permit_login)
btn_login.grid(row=0,column=0,padx=10,pady=10)

btn_register = Button(btn_frame,text="Register",bg="black",fg='white',padx=15,pady=12,font=('Helvetica',16,'bold'))
btn_register.bind('<Button-1>',permit_register)
btn_register.grid(row=0,column=1,padx=10)

label_error_frame = Frame(root,borderwidth=0,bg=bg_color)
label_error_frame.pack()



################## ----Footer ------###################

# user_tuple=display_all_user()

user_tuple =get_all_users()

variable = StringVar(root)
variable.set("Registered Users")

if len(user_tuple)==0:
    user_tuple=["No Users"]


reg_user = OptionMenu(root,variable,*user_tuple,
                        command=set_user)

reg_user.configure(highlightcolor="green")

reg_user.pack(side="right",ipady=3,padx=10)





##################END OF THE LOGIN SCREEN##########################




###############-------Events for Account page ----#################

def insert_data_account():
    dict=data_display(user_id)
    dict=dict[::-1]

    if len(dict)==0:
        account_list.delete(0,END)
        account_list.insert(END,"you have no data!!")
        account_list.insert(END,"click the add button to add your passwords")
    else:
        account_list.delete(0,END)
        for account in dict:
            account_list.insert(END,f"--------------------------------------------------------------------------")
            account_list.insert(END,f"Account : {account[1]}")
            account_list.insert(END,f"Username: {account[2]}")
            account_list.insert(END,f"Password: {account[3]}")
            account_list.insert(END,f"--------------------------------------------------------------------------")


def submit_data(event):
    data_account = u_acc_type.get()
    data_username = u_acc_name.get()
    data_password = u_acc_pass.get()

    response=data_insert(user_id,data_account,data_username,data_password)

    dict=data_display(user_id)
    dict=dict[::-1]

    if response==0:
        alert_box("Some fields are empty!!")
        print("#####")

    insert_data_account()

    add_box.destroy()



def alert_box(error):
    error_window = Toplevel()
    error_window.geometry("500x100")
    error_window.config(bg=bg_color)
    error_window.title('ERROR!')
    
    erro_label = Label(error_window,text=error,font=('Helvetica',18,'bold'),fg='white',bg=bg_color,wraplength=500)
    erro_label.pack(padx=10,pady=10)
    btn_error = Button(error_window,text="close",command=error_window.destroy,font=('Helvetica',20,'bold'))
    btn_error.pack(pady=10,padx=10)

def logout(event):
    user_account_window.destroy()
    root.destroy()
    root1.destroy()

def delete_acc(event):
    
    response = delete_account(entry_response.get(),user_id)
    dict=data_display(user_id)
    dict=dict[::-1]

    
    insert_data_account()
    

def update_account_box(event):
    global update_box
    global acc_data

    acc_name = entry_response.get()
    data = data_display_acc(user_id,acc_name)
    
    
    if data==None:
        return alert_box("No such account")

    update_box = Toplevel()
    update_box.geometry("500x200")
    update_box.config(bg=bg_color)
    update_box.title("Add account")
    update_box.resizable(0,0)
    
    global u_acc_type_1
    global u_acc_name_1
    global u_acc_pass_1



    acc_data=data[0]

    u_acc_type_label_1 = Label(update_box,fg="black",text="Account Type :",font=('Helvetica',16,'bold'),bg=bg_color)
    u_acc_type_label_1.grid(row=0,column=1,padx=10,pady=10)

    u_acc_type_1 = Entry(update_box,bg="white",fg="black",font=('Helvetica',16,'bold'),borderwidth=2,bd=1)
    u_acc_type_1.insert(0,data[0])
    u_acc_type_1.grid(row=0,column=2,padx=10,pady=10)

    u_acc_name_label_1 = Label(update_box,fg="black",text="Username :",font=('Helvetica',16,'bold'),bg=bg_color)
    u_acc_name_label_1.grid(row=1,column=1,padx=10,pady=10)

    u_acc_name_1 = Entry(update_box,bg="white",fg="black",font=('Helvetica',16,'bold'),borderwidth=2,bd=1)
    u_acc_name_1.insert(0,data[1])
    u_acc_name_1.grid(row=1,column=2,padx=10,pady=10)

    u_acc_pass_label_1 = Label(update_box,fg="black",text="Password :",font=('Helvetica',16,'bold'),bg=bg_color)
    u_acc_pass_label_1.grid(row=2,column=1,padx=10,pady=10)

    u_acc_pass_1 = Entry(update_box,bg="white",fg="black",font=('Helvetica',16,'bold'),borderwidth=2,bd=1)
    u_acc_pass_1.insert(0,data[2])
    u_acc_pass_1.grid(row=2,column=2,padx=10,pady=10)

    btn_submit_1 = Button(update_box,text="UPDATE",bg="blue",fg="white",font=('Helvetica',16,'bold'))
    btn_submit_1.bind('<Button-1>',update_data)
    btn_submit_1.grid(row=3,column=2,padx=10,pady=10)


def update_data(event):
    acc_name = entry_response.get()
    acc = u_acc_type_1.get()
    mail = u_acc_name_1.get()
    password = u_acc_pass_1.get()
    
    dict1=data_display(user_id)

    update_account(acc_name,user_id,acc,mail,password)

    dict1=data_display(user_id)
    dict1 = dict1[::-1]


    insert_data_account()

    update_box.destroy()


def add_box(event):
    global add_box
    add_box = Toplevel()
    add_box.geometry("500x200")
    add_box.config(bg=bg_color)
    add_box.title("Add account")
    add_box.resizable(0,0)
    
    global u_acc_type
    global u_acc_name
    global u_acc_pass

    u_acc_type_label = Label(add_box,fg="black",text="Account Type :",font=('Helvetica',16,'bold'),bg=bg_color)
    u_acc_type_label.grid(row=0,column=1,padx=10,pady=10)

    u_acc_type = Entry(add_box,bg="white",fg="black",font=('Helvetica',16,'bold'),borderwidth=2,bd=1)
    u_acc_type.grid(row=0,column=2,padx=10,pady=10)

    u_acc_name_label = Label(add_box,fg="black",text="Username :",font=('Helvetica',16,'bold'),bg=bg_color)
    u_acc_name_label.grid(row=1,column=1,padx=10,pady=10)

    u_acc_name = Entry(add_box,bg="white",fg="black",font=('Helvetica',16,'bold'),borderwidth=2,bd=1)
    u_acc_name.grid(row=1,column=2,padx=10,pady=10)

    u_acc_pass_label = Label(add_box,fg="black",text="Password :",font=('Helvetica',16,'bold'),bg=bg_color)
    u_acc_pass_label.grid(row=2,column=1,padx=10,pady=10)

    u_acc_pass = Entry(add_box,bg="white",fg="black",font=('Helvetica',16,'bold'),borderwidth=2,bd=1)
    u_acc_pass.grid(row=2,column=2,padx=10,pady=10)

    btn_submit = Button(add_box,text="ADD",bg="red",fg="white",font=('Helvetica',16,'bold'))
    btn_submit.bind('<Button-1>',submit_data)
    btn_submit.grid(row=3,column=2,padx=10,pady=10)


###############--------ACCOUNT WINDOWS --------##################


global user_id

def account_window(user_id,user_name):
    global user_account_window
    global btn_delete
    global entry_response

    user_account_window = Toplevel()

    user_account_window.geometry("600x600")
    user_account_window.configure(bg=bg_color)
    user_account_window.title('PassKeeper')
    user_account_window.resizable(0,0)
    
    global dict
    global account_list
    
    dict=data_display(user_id)
    dict = dict[::-1]


    labelrt = Label(user_account_window,text=f"Welcome {user_name}",font=('Helvetica',20,"bold"),bg='black',fg="white",pady=10)
    labelrt.pack(fill=X)


    scroll = Scrollbar(user_account_window)
    scroll.pack(side=RIGHT,fill=Y)
    

    account_list = Listbox(user_account_window,yscrollcommand=scroll.set,font=('Helvetica',16,'bold'),bg="white",fg="black",width=200,height=100)


    btn_add = Button(user_account_window,text='Add',bg='#27d653',fg='black',padx=30,pady=10,font=('Helvetica',16,'bold'))
    btn_add.bind('<Button-1>',add_box)
    btn_add.pack(padx=10,pady=10)

    btn_logout = Button(user_account_window,text='Logout',bg='#e31931',fg='white',padx=20,pady=10,font=('Helvetica',16,'bold'))
    btn_logout.bind('<Button-1>',logout)
    btn_logout.pack(side='bottom',padx=5,pady=5)


    sub_bottom_frame = Frame(user_account_window,bg='black')
    sub_bottom_frame.pack(side="top",fill=X)
    label_acc = Label(sub_bottom_frame,text="Enter account name to perform the operations",font=('Helvetica',14,'bold'),bg='black',fg='white')
    label_acc.pack(padx=5,pady=5)


    entry_response = Entry(sub_bottom_frame,fg="black",bg="white",font=('Helvetica',20))
    entry_response.pack(side="left",padx=10)
    btn_delete = Button(sub_bottom_frame,text='Delete',bg='#d91421',fg='white',padx=13,pady=10,font=('Helvetica',16,'bold'))
    btn_delete.bind('<Button-1>',delete_acc)
    btn_delete.pack(ipady=1,padx=3,pady=3)

    btn_update = Button(sub_bottom_frame,text="Update",bg='#3084d9',fg='black',padx=10,pady=10,font=('Helvetica',16,'bold'))
    btn_update.bind('<Button-1>',update_account_box)
    btn_update.pack(ipady=1,padx=3,pady=3)

    insert_data_account()


    account_list.pack(side=LEFT)

    scroll.config(command=account_list.yview)

#####----------------------END OF THE ACCOUNT PAGE---------------------#####

#-----------------------------MAIN-------------------------------#
def on_quit():
    root.quit()
    
root.protocol('WM_DELETE_WINDOW',on_quit)


root.mainloop()
commit_close()


