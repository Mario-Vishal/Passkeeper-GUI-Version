import sqlite3
from user import *

conn = sqlite3.connect('.credentials.db')
c= conn.cursor()

#################################### THE LOGIN/REGISTER PAGE ####################################

def db_contains(user_mail):

        try:
            c.execute("SELECT * FROM credentials WHERE email=?",(user_mail,))
            value=c.fetchone()
        except:
            value=0
        if value:
            return True
        else:
            return False


def get_val():

    user_mail = input("Enter your mail id : ")
    user_password = input("Enter your password : ")

    return [user_mail,user_password]

### ------------------- Registration -------------- ###

def register(user_mail,user_password):

        user = user_credentials(user_mail,user_password)

        if not user.email_check():
            
            return "Enter Valid email address"

        if not user.password_check():
            
            return "Password is too short"

        if db_contains(user.email):
            
            return "User already exists"

        else:
            params = (user.email,user.password)
            c.execute(f"INSERT INTO credentials(email,password) VALUES(?,?)",params)
            uname = user.email.split('@')[0]
            

            c.execute("SELECT user_id FROM credentials WHERE (email=? and password=?)",params)
            value = c.fetchone()[0]

            return "Successfully registered"




### ----------------- Login ----------------- ###

def login(user_mail,user_password):

    user = user_credentials(user_mail,user_password)

    params=(user.email,user.password)
    try:
        c.execute("SELECT user_id FROM credentials WHERE (email=? and password=?)",params)
        value = c.fetchone()[0]
    except:
        value=False

    if value:
        uname = user_mail.split('@')[0]

        

        return ["Successfully logined",value,uname]
    else:
        # print("Error Please check your credentials!!")
        return "Error Please check your credentials!!",value


########################################## THE HOME PAGE ########################################

def data_display(user_id):
    c.execute("SELECT data_id,account,username,password FROM data WHERE user_id=?",str(user_id))
    details = c.fetchall()

    return details

def data_display_acc(user_id,acc_name):
    c.execute("SELECT account,username,password FROM data WHERE user_id=? AND account=?",(str(user_id),acc_name))
    details = c.fetchone()
    
    return details

def data_insert(user_id,data_account,data_username,data_password):

    params = (user_id,data_account,data_username,data_password)
    if len(data_account)==0 or len(data_password)==0 or len(data_username)==0:
        return 0
    else:
        c.execute("INSERT INTO data(user_id,account,username,password) VALUES(?,?,?,?)",params)
        conn.commit()
        return 1

    

def get_all_users():

    c.execute("SELECT email FROM credentials")

    user_list = c.fetchall()
    result=[]
    for user in user_list:
        result.append(user[0])

    return tuple(result)

def delete_all_users():
    c.execute("DROP TABLE credentials")
    c.execute("DROP TABLE data")

def disp_all_data(user_id):
    c.execute(f'SELECT * FROM data where user_id={user_id}')
    result = c.fetchall()
    
    return result
# 

def delete_account(acc_name,user_id):

    
    if c.execute(f'DELETE FROM data where account="{acc_name}"'):
        conn.commit()
        
        return "done"
    else:
        print("no")
        return "No such account name"


def update_account(acc_name,user_id,acc,mail,password):
    params=(acc_name,mail,password,acc_name,user_id)
    c.execute(f"UPDATE data SET account='{acc}',username='{mail}',password='{password}' WHERE account='{acc_name}' AND user_id={user_id}")
    conn.commit()

    

 #----------------------------creating table credentials------------------------#
try:



    c.execute("""CREATE TABLE credentials(
                user_id INTEGER PRIMARY KEY,
                email text,
                password text)""")
except:
    pass

#-----------------------------creating table data-------------------------------#

try:
    c.execute("""CREATE TABLE data(
        user_id INTEGER,
        data_id INTEGER PRIMARY KEY,
        account text,
        username text,
        password text,
        FOREIGN KEY (user_id) REFERENCES credentials(user_id)
    )
    """)
except:
    pass


#-----------------------main function--------------------------#


def commit_close():
    conn.commit()
    conn.close()

