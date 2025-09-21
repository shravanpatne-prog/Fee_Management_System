from tkinter import *
from tkinter import ttk
import sqlite3


users = [
    {'username':'shravan','password':'123'},
    {'username':'sandeep','password':'456'}
    ]
    
        
def b_login():
    u = e_username.get()
    p = e_password.get()
    e_username.delete(0,END)
    e_password.delete(0,END)
    l_invalid1.place_forget()
    l_invalid2.place_forget()

    for user in users:
        if (user["username"]== u) and (user["password"] == p):
            login_f(1)
            menu_page(0)
            return

    l_invalid1.place(x=450, y=80)
    l_invalid2.place(x=450, y=130)

def login_f(args):
    if args == 1:
        login_frame.place_forget()
        return
    login_frame.place(x=350, y=175, width=700, height=250)

def total():
    global add
    add = java.get() + python.get() + ds.get()
    l_total.config(text="Total Fees: ₹ " + str(add))
    return

def selection(args):
    if args == "Cheque":
        l_check_no.place(x=500, y=370)
        e_check_no.place(x=680, y=370)
        l_bank.place(x=500, y=420)
        e_bank.place(x=600, y=420)
    else:
        l_check_no.place_forget()
        e_check_no.place_forget()
        l_bank.place_forget()
        e_bank.place_forget()

def add_student():
    s = e_student_id.get().strip()
    n = e_name.get().strip()
    m = e_mobile.get().strip()
    f = add
    if java.get() != 0 :
        j = '✔️'
    else:
        j = '❌'
    if python.get() != 0 :
        p = '✔️'
    else:
        p = '❌'
    if ds.get() != 0 :
        d = '✔️'
    else:
        d = '❌'
    
    try:
        ad = int(e_advance.get())
    except:
        ad = 0
    b = f - ad
    a = t_address.get("1.0",END).strip()
    D = e_date.get().strip()
    M = e_check_no.get().strip()
    B = e_bank.get().strip()

    conn = sqlite3.connect('student_fees_database.db')
    c = conn.cursor()
    c.execute('INSERT INTO student VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',
              (s,n,m,j,p,d,f,b,a,D,M,B))
    conn.commit()
    conn.close()
    
    clear_all()

def clear_all():
    global add
    e_student_id.delete(0,END)
    e_name.delete(0,END)
    e_mobile.delete(0,END)
    e_advance.delete(0,END)
    t_address.delete("1.0",END)
    e_date.delete(0,END)
    e_check_no.delete(0,END)
    e_bank.delete(0,END)

    add = 0
    l_total.config(text="Total Fees: ₹ 0")

    java.set(0)
    python.set(0)
    ds.set(0)
    d.set("Cash")

    l_check_no.place_forget()
    e_check_no.place_forget()
    l_bank.place_forget()
    e_bank.place_forget()
    return

def menu_page(args):
    if args == 1:
        menu_frame.place_forget()
        return
    menu_frame.place(x=450, y=150, width=500, height=400)

def new_student(args):
    if args ==1:
        new_student_frame.place_forget()
        menu_page(0)
        return
    new_student_frame.place(x=225, y=90, width=960, height=600)
    clear_all()
    return

def fees_due(args):
    if args == 1:
        fees_due_frame.place_forget()
        menu_page(0)
        return
    fees_due_frame.place(x=225, y=90, width=960, height=600)
    
    query = "SELECT Name, Mobile, Java, Python, DS, Fees, Balance FROM student WHERE Balance != '0'"
    conn = sqlite3.connect('student_fees_database.db')
    c = conn.cursor()
    c.execute(query)
    rows = c.fetchall()
    conn.close()

    table_frame = Frame(fees_due_frame, bg="crimson", bd=4, relief=RIDGE)
    table_frame.place(x=35,y=70, width=877, height=470)
    hs = Scrollbar(table_frame, orient = HORIZONTAL)
    hs.pack(side=BOTTOM, fill=X)
    vs = Scrollbar(table_frame, orient=VERTICAL)
    vs.pack(side=RIGHT, fill=Y)

    student_table = ttk.Treeview(table_frame,
                                 columns=("n","m","e","f","h","g","d"),
                                 xscrollcommand=hs.set,yscrollcommand=vs.set)
    hs.config(command=student_table.xview)
    vs.config(command=student_table.yview)
    student_table.heading("n",text="Name")
    student_table.heading("m",text="Mobile No.")
    student_table.heading("e",text="Java")
    student_table.heading("f",text="Python")
    student_table.heading("h",text="DS")
    student_table.heading("g",text="Fees")
    student_table.heading("d",text="Balance")
    student_table["show"]="headings"
    student_table.pack(fill=Y, expand=1)
    student_table.column("n",width=200)
    student_table.column("m",width=200)
    student_table.column("e",width=60)
    student_table.column("f",width=60)
    student_table.column("h",width=60)
    student_table.column("g",width=120)
    student_table.column("d",width=150)

    student_table.delete(*student_table.get_children())
    for row in rows:
        student_table.insert("", END, values=row)
    return

def pay_balance(args):
    if args == 1:
        e_student_id_pay.delete(0,END)
        e_mobile_pay.delete(0,END)
        e_pay.delete(0,END)
        l_updated_amount.place_forget()
        pay_balance_frame.place_forget()
        menu_page(0)
        return
    pay_balance_frame.place(x=225, y=90, width=960, height=600)
    return

def search_pay():
    l_invalid1_pay.place_forget()
    l_invalid2_pay.place_forget()
    l_updated_amount.place_forget()
    e_pay.delete(0,END)
    global balance
    element = []
    
    sid = e_student_id_pay.get().strip()
    mob = e_mobile_pay.get().strip()
    r = check(sid,mob)
    if r == 3:
        query = "SELECT Balance FROM student WHERE 1=1 "
        if sid != "":
            query += "AND Student_Id = ?"
            element.append(sid)
        if mob != "":
            query += " AND Mobile = ?"
            element.append(mob)
                
        conn = sqlite3.connect("student_fees_database.db")
        c = conn.cursor()
        c.execute(query,element)
        rows = c.fetchall()
        conn.close()
        if rows:
            print(rows)
            balance = rows[0][0]
            e_pay.insert(0,balance)
            return
        
    elif r == 1:
        l_invalid1_pay.place(x=700,y=130)
        e_pay.delete(0,END)
        l_updated_amount.config(text="")
    elif r == 2:
        l_invalid2_pay.place(x=700,y=180)
        e_mobile_pay.delete(0,END)
        e_pay.delete(0,END)
        l_updated_amount.config(text="")
    else:
        l_invalid1_pay.place(x=700,y=130)
        l_invalid2_pay.place(x=700,y=180)
        e_student_id_pay.delete(0,END)
        e_mobile_pay.delete(0,END)
        e_pay.delete(0,END)
        l_updated_amount.config(text="")
        
 
def check(sid,mob):
    element = []
    if sid != "" or mob != "":
        if sid != "" and mob != "":
            query = "SELECT Student_ID FROM student WHERE Mobile = ? "
            element.append(mob)
            conn = sqlite3.connect("student_fees_database.db")
            c = conn.cursor()
            c.execute(query,element)
            element.clear()
            row = c.fetchall()
            if row is None or row[0][0] != sid:
                return 0
            return 3
        
        elif sid != "":
            query = "SELECT Student_ID FROM student WHERE Student_ID = ? "
            element.append(sid)
            conn = sqlite3.connect("student_fees_database.db")
            c = conn.cursor()
            c.execute(query,element)
            element.clear()
            row = c.fetchall()
            print(row)
            if row is None:
                return 1
            return 3
        
        elif mob != "":
            query = "SELECT Mobile FROM student WHERE Mobile = ? "
            element.append(mob)
            conn = sqlite3.connect("student_fees_database.db")
            c = conn.cursor()
            c.execute(query,element)
            element.clear()
            row = c.fetchall()
            print(row)
            if row is None:
                return 2
            return 3
        else:
            return 0

def pay():
    sid = e_student_id_pay.get().strip()
    mob = e_mobile_pay.get().strip()
    element = []
    amount = e_pay.get().strip()
    new_balance = int(balance) - int(amount)
    
    query = "UPDATE student SET Balance = ? WHERE 1=1 "
    element.append(new_balance)
    print(element)
    if sid != "":
        query += "AND Student_Id = ?"
        element.append(sid)
    if mob != "":
        query += " AND Mobile = ?"
        element.append(mob)

    conn = sqlite3.connect("student_fees_database.db")
    c = conn.cursor()
    c.execute(query,element)
    conn.commit()
    conn.close()
    e_student_id_pay.delete(0,END)
    e_mobile_pay.delete(0,END)
    e_pay.delete(0,END)
    update_amount = str(new_balance)
    l_updated_amount.config(text ="₹ "+update_amount)
    l_updated_amount.place(x=550, y=380)
    return

def search_student(args):
    if args == 1:
        search_student_frame.place_forget()
        menu_page(0)
        return
    search_student_frame.place(x=220, y=90, width=960, height=300)


def search1(args):
    if args == 1:
        l_invalid1_search.place_forget()
        l_invalid2_search.place_forget()
        search1_frame.place_forget()
        return
    l_invalid1_search.place_forget()
    l_invalid2_search.place_forget()

    sid = e_student_id_search.get().strip()
    mob = e_mobile_search.get().strip()
    
    e_student_id_search.delete(0,END)
    e_mobile_search.delete(0,END)
    
    element = []
    query = "SELECT Student_ID, Name, Mobile, Java, Python, DS, Fees, Balance, Address,Date ,Check_No ,Bank FROM student WHERE 1=1 "
    if sid != "":
        query += "AND Student_Id = ? "
        element.append(sid)
    if mob != "":
        query += "AND Mobile = ? "
        element.append(mob)
    conn = sqlite3.connect("student_fees_database.db")
    c = conn.cursor()
    c.execute(query,element)
    rows = c.fetchall()
    conn.close()

    if rows:
        search1_frame.place(x=220, y=400, width=960, height=280)

        table_frame = Frame(search1_frame, bg="crimson", bd=4, relief=RIDGE)
        table_frame.place(x=35,y=70, width=877, height=200)
        hs = Scrollbar(table_frame, orient = HORIZONTAL)
        hs.pack(side=BOTTOM, fill=X)
        vs = Scrollbar(table_frame, orient=VERTICAL)
        vs.pack(side=RIGHT, fill=Y)

        student_table = ttk.Treeview(table_frame,
                                columns=("s","n","m","j","p","d","f","b","a","D","M","B"),
                                xscrollcommand=hs.set,yscrollcommand=vs.set)
        hs.config(command=student_table.xview)
        vs.config(command=student_table.yview)
        student_table.heading("s",text="Student_ID")
        student_table.heading("n",text="Name")
        student_table.heading("m",text="Mobile No.")
        student_table.heading("j",text="Java")
        student_table.heading("p",text="Python")
        student_table.heading("d",text="DS")
        student_table.heading("f",text="Fees")
        student_table.heading("b",text="Balance")
        student_table.heading("a",text="Address")
        student_table.heading("D",text="Date")
        student_table.heading("M",text="Check_No:")
        student_table.heading("B",text="Bank")
        student_table["show"]="headings"
        student_table.pack(fill=Y, expand=1)
        student_table.column("s",width=200)
        student_table.column("n",width=200)
        student_table.column("j",width=60)
        student_table.column("p",width=60)
        student_table.column("d",width=60)
        student_table.column("f",width=130)
        student_table.column("b",width=130)
        student_table.column("a",width=200)
        student_table.column("D",width=100)
        student_table.column("M",width=200)
        student_table.column("B",width=130)

        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert("", END, values=row)
    
    else:
        search1_frame.place_forget()
        l_invalid1_search.place(x=700,y=130)
        l_invalid2_search.place(x=700,y=180)
    return


master = Tk()
master.title('Fee Management System')
master.geometry('1400x700+20+20')

title = Label(master,text="Fee Management System",font=("Calibri",40,"bold"),bd=10,bg="crimson",fg="white",relief=GROOVE )
title.pack(side=TOP, fill=X)

add=0
#Login_Frame
login_frame= Frame(master, bg="crimson", bd=4, relief=RIDGE )
login_f(0)
login_frame_title = Label(login_frame,text="LOGIN",font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
login_frame_title.pack(side=TOP,fill=X)

l_username = Label(login_frame,text="Username:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_username.place(x=20, y=80)
e_username = Entry(login_frame,font=("Calibri",18))
e_username.place(x=200, y=80)

l_password = Label(login_frame,text="Password:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_password.place(x=20, y=130)
e_password = Entry(login_frame,font=("Calibri",18))
e_password.place(x=200, y=130)

b_login= Button(login_frame, text="LOGIN", width=8, height=2, command=b_login)
b_login.place(x=300, y=190)

l_invalid1 = Label(login_frame,text=" Invalid ", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_invalid2 = Label(login_frame,text=" Invalid ", font=("calibri",25,"bold"), fg="white", bg="crimson")

#Menu_Frame
menu_frame = Frame(master, bg="crimson", bd=4, relief=RIDGE)

menu_frame_title = Label(menu_frame, text="Menu", font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
menu_frame_title.pack(side=TOP,fill=X)

b_new_student = Button(menu_frame, text="New Student", width=12, height=2,command=lambda:(menu_page(2),new_student(0)))
b_new_student.place(x=75, y=150)

b_fees_due = Button(menu_frame, text="Fees Due", width=12, height=2,command=lambda:(menu_page(2),fees_due(0)))
b_fees_due.place(x=300, y=150)

b_pay_balance = Button(menu_frame, text="Pay Balance", width=12, height=2,command=lambda:(menu_page(2),pay_balance(0)))
b_pay_balance.place(x=75, y=230)

b_search_student = Button(menu_frame, text="Search Student", width=12, height=2,command=lambda:(menu_page(1),search_student(0)))
b_search_student.place(x=300, y=230)

b_back = Button(menu_frame, text="Back", width=12, height=2,command=lambda:(menu_page(1),login_f(0)))
b_back.place(x=190, y=300)

#new_student_frame
new_student_frame= Frame(master, bg="crimson", bd=4, relief=RIDGE)

new_student_frame_title = Label(new_student_frame, text="New Student Form", font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
new_student_frame_title.pack(side=TOP,fill=X)

l_student_details = Label(new_student_frame, text="Student Details", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_student_details.place(x=70, y=80)

l_fee_details = Label(new_student_frame,text="Fee Details", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_fee_details.place(x=570, y=80)

l_student_id = Label(new_student_frame, text="Student ID:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_student_id.place(x=20, y=130)
e_student_id = Entry(new_student_frame,font=("Calibri",18))
e_student_id.place(x=200, y=130)

l_name = Label(new_student_frame, text="Name:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_name.place(x=20, y=190)
e_name = Entry(new_student_frame,font=("Calibri",18))
e_name.place(x=200, y=190)

l_mobile = Label(new_student_frame, text="Mobile:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_mobile.place(x=20, y=250)
e_mobile = Entry(new_student_frame,font=("Calibri",18))
e_mobile.place(x=200, y=250)

l_address = Label(new_student_frame, text="Address:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_address.place(x=20, y=320)
t_address = Text(new_student_frame,font=("calibri",18), width=20, height = 4)
t_address.place(x=200, y=320)

l_date1 = Label(new_student_frame, text="Date:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_date1.place(x=500, y=125)
l_date2 = Label(new_student_frame, text="(DD/MM/YYYY)", font=("calibri",15), fg="white", bg="crimson")
l_date2.place(x=500, y=160)
e_date = Entry(new_student_frame, font=("Calibri",18))
e_date.place(x=600, y=130)

l_subject = Label(new_student_frame, text="Subject:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_subject.place(x=500, y=190)
java = IntVar(value=0)
c1 = Checkbutton(new_student_frame, text="Java",font=("calibri",15), bg="crimson", variable=java, onvalue=20000, offvalue=0,command=total)
python = IntVar(value=0)
c2 = Checkbutton(new_student_frame, text="Python",font=("calibri",15),bg="crimson", variable=python, onvalue=20000, offvalue=0,command=total)
ds = IntVar(value=0)
c3 = Checkbutton(new_student_frame, text="DS",font=("calibri",15), bg="crimson", variable=ds, onvalue=25000, offvalue=0,command=total)
c1.place(x=650, y=200)
c2.place(x=750, y=200)
c3.place(x=850, y=200)
l_total = Label(new_student_frame, text="Total Fees:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_total.place(x=500, y=230)

l_advance= Label(new_student_frame, text="Advance:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_advance.place(x=500, y=280)
e_advance = Entry(new_student_frame,font=("Calibri",18))
e_advance.place(x=650, y=280)

l_pay_method= Label(new_student_frame, text="Payment Method:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_pay_method.place(x=500, y=320)
options = ["Cash","Cheque"]
d = StringVar(value=options[0])
d1 = OptionMenu(new_student_frame, d, *options, command=selection)
d1.place(x=800,y=325)

b_add = Button(new_student_frame, text="ADD", width=12, height=2,command=add_student)
b_add.place(x=325, y=520)

b_back = Button(new_student_frame, text="Back", width=12, height=2,command=lambda:new_student(1))
b_back.place(x=450, y=520)

#selection
l_check_no = Label(new_student_frame,text="Check No:",font=("calibri",25,"bold"), fg="white", bg="crimson")
e_check_no = Entry(new_student_frame,font=("Calibri",18))
l_bank= Label(new_student_frame, text="Bank:", font=("calibri",25,"bold"), fg="white", bg="crimson")
e_bank = Entry(new_student_frame,font=("Calibri",18))

#fees_due
fees_due_frame = Frame(master, bg="crimson", bd=4, relief=RIDGE)

fees_due_frame_title = Label(fees_due_frame, text="Fees Due", font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
fees_due_frame_title.pack(side=TOP,fill=X)

b_back = Button(fees_due_frame, text="Back", width=12, height=2,command=lambda:fees_due(1))
b_back.place(x=425, y=545)
#pay_balance
pay_balance_frame = Frame(master, bg="crimson", bd=4, relief=RIDGE)

pay_balance_frame_title = Label(pay_balance_frame, text="Pay Balance", font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
pay_balance_frame_title.pack(side=TOP,fill=X)

l_note= Label(pay_balance_frame, text="Enter Student ID or Mobile No", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_note.place(x=270, y=80)

l_student_id_pay = Label(pay_balance_frame, text="Student ID:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_student_id_pay.place(x=270, y=130)
e_student_id_pay = Entry(pay_balance_frame,font=("Calibri",18))
e_student_id_pay.place(x=440, y=130)

l_mobile_pay = Label(pay_balance_frame, text="Mobile No:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_mobile_pay.place(x=270, y=180)
e_mobile_pay = Entry(pay_balance_frame,font=("Calibri",18))
e_mobile_pay.place(x=440, y=180)

b_search_pay = Button(pay_balance_frame, text="Search", width=12, height=2,command=lambda:search_pay())
b_search_pay.place(x=425, y=230)

l_pay = Label(pay_balance_frame, text="Balance:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_pay.place(x=270, y=280)
e_pay = Entry(pay_balance_frame,font=("Calibri",18))
e_pay.place(x=460, y=280)

b_pay = Button(pay_balance_frame, text="Pay", width=12, height=2,command=lambda:pay())
b_pay.place(x=425, y=330)

l_updated_balance = Label(pay_balance_frame, text="Updated Balance:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_updated_balance.place(x=270, y=380)

l_updated_amount = Label(pay_balance_frame, font=("calibri",25,"bold"), fg="white", bg="crimson")


b_back = Button(pay_balance_frame, text="Back", width=12, height=2,command=lambda:pay_balance(1))
b_back.place(x=425, y=480)

l_invalid1_pay = Label(pay_balance_frame,text=" Invalid ", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_invalid2_pay = Label(pay_balance_frame,text=" Invalid ", font=("calibri",25,"bold"), fg="white", bg="crimson")

#search_student
search_student_frame = Frame(master, bg="crimson", bd=4, relief=RIDGE)

search_student_title = Label(search_student_frame, text="Search Student", font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
search_student_title.pack(side=TOP,fill=X)

l_note= Label(search_student_frame, text="Enter Student ID or Mobile No", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_note.place(x=270, y=80)

l_student_id_search = Label(search_student_frame, text="Student ID:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_student_id_search.place(x=270, y=130)
e_student_id_search = Entry(search_student_frame,font=("Calibri",18))
e_student_id_search.place(x=440, y=130)

l_mobile_search = Label(search_student_frame, text="Mobile No:", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_mobile_search.place(x=270, y=180)
e_mobile_search = Entry(search_student_frame,font=("Calibri",18))
e_mobile_search.place(x=440, y=180)

b_search1 = Button(search_student_frame, text="Search", width=12, height=2,command=lambda:search1(0))
b_search1.place(x=300, y=230)

b_back = Button(search_student_frame, text="Back", width=12, height=2,command=lambda:(search_student(1),search1(1)))
b_back.place(x=450, y=230)

l_invalid1_search = Label(search_student_frame,text=" Invalid ", font=("calibri",25,"bold"), fg="white", bg="crimson")
l_invalid2_search = Label(search_student_frame,text=" Invalid ", font=("calibri",25,"bold"), fg="white", bg="crimson")

#search1
search1_frame = Frame(master, bg="crimson", bd=4, relief=RIDGE)

search1_frame_title = Label(search1_frame, text="Student Details", font=("Calibri",30,"bold"), bg="white", fg="crimson", bd=4, relief=GROOVE)
search1_frame_title.pack(side=TOP,fill=X)

try:
    conn = sqlite3.connect('student_fees_database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS student (
        Student_ID TEXT PRIMARY KEY,
        Name TEXT,
        Mobile TEXT,
        Java INTEGER,
        Python INTEGER,
        DS INTEGER,
        Fees INTEGER,
        Balance INTEGER,
        Address TEXT,
        Date TEXT,
        Check_No TEXT,
        Bank TEXT
    )''')
    conn.commit()
    conn.close()
except sqlite3.OperationalError:
    pass

master.mainloop()

