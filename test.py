from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import pymysql as sq
import random
import time
root = Tk()
root.geometry("1000x700")
root.config(bg="#b3e763")



j=1

global t


def result():
    global root2
    lis=['q1','q2','q3','q4','q5']
    lis1=['op1','op2','op3','op4']
    la2=Label(text="RESULT",font=(None,40,'italic'))
    la2.pack()
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    
    #fra=Frame(root2,bg='red')
    cmd=f"select total from result where rollno={user}"
    c.execute(cmd)
    dat1=c.fetchone()
    la1=Label(text="Total number of correct answers: "+str(dat1[0]),font=(None,30,'italic'))
    la1.pack()
    for i in range(5):
        cmd=f"select ques from anskey where quesno={t[i]}"
        c.execute(cmd)
        da1=c.fetchone()
        cmd=f"select {lis[i]} from answer where rollno={user}"
        c.execute(cmd)
        da21=c.fetchone()
        cmd=f"select {lis1[da21[0]-1]} from anskey where quesno={t[i]}"
        c.execute(cmd)
        da2=c.fetchone()
        cmd=f"select ans from anskey where quesno={t[i]}"
        c.execute(cmd)
        da31=c.fetchone()
        cmd=f"select {lis1[da31[0]-1]} from anskey where quesno={t[i]}"
        c.execute(cmd)
        da3=c.fetchone()
        lab1=Label(root2,text=f'Q{i+1}.'+da1[0],font=(None,30,'italic'))
        if da2[0]==da3[0]:
            lab2=Label(root2,text=f'Your answer:'+da2[0],font=(None,15,'italic'),fg='light green')
        else:
            lab2=Label(root2,text=f'Your answer:'+da2[0],font=(None,15,'italic'),fg='red')
        lab3=Label(root2,text=f'Correct answer:'+da3[0],font=(None,15,'italic'),fg='green')
        lab1.pack()
        lab2.pack()
        lab3.pack()
    #fra.pack(extend=True,fill='both')
    root2.mainloop()

def next():
    global bu1,j
    fr.destroy()
    if j<5:
        j=j+1
        ques(t[j-1])
        
        
        
def prev():
    global j
    fr.destroy()
    if j>1:
        j=j-1
        ques(t[j-1])
        
        
def submit():
    global ll1
    ll1.destroy()

    lis=['q1','q2','q3','q4','q5']
    lis1=['op1','op2','op3','op4']
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    for i in range(5):
        cmd=f"select {lis[i]} from answer where rollno={user}"
        c.execute(cmd)
        da=c.fetchone()
        cmd=f"select ans from anskey where quesno={t[i]}"
        c.execute(cmd)
        da1=c.fetchone()
        if da[0]==da1[0]:
            cmd=f"update result set {lis[i]}=1 where rollno={user}"
            c.execute(cmd)
            db1.commit()
        else:
            cmd=f"update result set {lis[i]}=0 where rollno={user}"
            c.execute(cmd)
            db1.commit()

    cmd=f"update result set total=(q1+q2+q3+q4+q5)"
    c.execute(cmd)
    db1.commit()
    fr.destroy()
    
    result()

def select(j):
    global v,t,fr,bu1,bu2
    try:
        bu1.destroy()
        bu2.destroy()
    except NameError as nm:
        pass
    d=v.get()
    lis=['q1','q2','q3','q4','q5']
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    cmd=f"update answer set {lis[j-1]}={d} where rollno={user}"
    c.execute(cmd)
    db1.commit()
    print(d)
    bu1=Button(fr,text="next",command=lambda:next())
    bu2=Button(fr,text="prev",command=lambda:prev())
    if j>1:
        bu2.pack(side='bottom')
    if j==5:
        bu1.config(text="submit",command=lambda:submit())
    bu1.pack(side='bottom')
    
def ques(i):
    
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    global root2,v
    c=db1.cursor()
    v=IntVar()
    global j
    v.set(-1)
    cmd=f"select ques from anskey where quesno={i}"
    c.execute(cmd)
    data=c.fetchone()
    global fr
    fr=Frame(root2)
    lab=Label(fr,text=f"Q{j}.{data[0]}",font=(None,20,'italic'))
    lab.pack()
    cmd=f"select op1 from anskey where quesno={i}"
    c.execute(cmd)
    op1=c.fetchone()
    rad1=Radiobutton(fr, text=f"{op1[0]}",padx = 20,variable=v,value=1, command=lambda:select(j))
    rad1.pack()

    cmd=f"select op2 from anskey where quesno={i}"
    c.execute(cmd)
    op2=c.fetchone()
    rad2=Radiobutton(fr, text=f"{op2[0]}",padx = 20,variable=v, value=2,command=lambda:select(j))
    rad2.pack()

    cmd=f"select op3 from anskey where quesno={i}"
    c.execute(cmd)
    op3=c.fetchone()
    rad3=Radiobutton(fr, text=f"{op3[0]}",padx = 20,variable=v, value=3,command=lambda:select(j))
    rad3.pack()

    cmd=f"select op4 from anskey where quesno={i}"
    c.execute(cmd)
    op4=c.fetchone()
    rad4=Radiobutton(fr, text=f"{op4[0]}",padx = 20,variable=v, value=4,command=lambda:select(j))
    rad4.pack()

    fr.pack()

global remaining
remaining=180
def update_clock():
    global ll1,ff,remaining,root2
    if remaining <= 0:
        submit()
    else:
        try:
            m,s=divmod(remaining,60)
            ll1.configure(text=f'{m}:{s}')
            remaining = remaining - 1
            ff.after(1000, update_clock)
        except:
            pass

def test():
    root1.destroy()
    global root2,t,ll1,ff
    root2=Tk()
    ff=Frame(root2)
    ff.pack(side='top')
    t=random.sample(range(1,8),5)
    ll1=Label(root2,text="",font=(None,30,'italic'),fg='red')
    ll1.pack()
    update_clock()
    ques(t[0])
    root2.geometry('900x300')
    root2.mainloop()
def studenttest():
    global root1
    root1=Tk()
    root1.config(bg='light green')
    l1=Label(root1,text="Click Start to Start the test")
    bu1=Button(root1,text="Start",command=lambda:test())
    l1.config(font=(None,30,'italic'),justify='center',wraplength=400,bg='light green')
    bu1.config(font=(None,30,'italic'),bg='red')
    l1.pack()
    bu1.pack()

    root1.mainloop()




def student():
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    global user
    try:    
        if e3.get():
            user=int(e3.get())
        else:
            user=e3.get()

        passwd=e4.get()
        if not (bool(user) and bool(passwd)):
            messagebox.showinfo("not entered","cu")
    
    
        cmd=f"select * from stuuser where rollno={user}"
        c.execute(cmd)
        data=c.fetchone()
        if bool(data):
            if passwd==data[1]:
                root.destroy()
                studenttest()
                root.mainloop()
            else:
                messagebox.showinfo("wrong password")
        else:
            messagebox.showinfo("not a registered user")

    except ValueError as v:
        messagebox.showinfo("userid must be an integer","userid not valid")
"""def stu():
    user=int(e3.get())
    passwd=e4.get()
    print(user,passwd)
    print(type(user),type(passwd))"""



#admin login end
def savedata():
    global root
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    cmd=f"insert into info values({roll1},'{name}','{address}')"
    c.execute(cmd)
    db1.commit()
    cmd=f"insert into stuuser values({roll1},'{passwd1}')"
    c.execute(cmd)
    db1.commit()
    
    cmd=f"insert into answer values({roll1},0,0,0,0,0,0,0,0,0,0)"
    c.execute(cmd)
    db1.commit()
    cmd=f"insert into result values({roll1},0,0,0,0,0,0,0,0,0,0,0)"
    c.execute(cmd)
    db1.commit()
    root=Tk()
    main()
def submit1():
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    global e31,e32,e33,e34,roll1,address,passwd1,name
    try:    
        if e31.get():
            roll1=int(e31.get())
        else:
            roll1=e31.get()

        cmd=f"select * from stuuser where rollno={roll1}"
        c.execute(cmd)
        data=c.fetchone()
        if not(bool(data)):
            passwd1=e34.get()
            name=e32.get()
            address=e33.get()
        
            if not (bool(roll1) and bool(passwd1) and bool(name) and bool(address)):
                messagebox.showinfo("not entered","empty")
            else:
                if (len(passwd1)<5):
                    messagebox.showinfo("short password","atleast 5 char")
                else:
                    savedata()
        else:
            messagebox.showinfo("user already exists")

    except ValueError as v:
        messagebox.showinfo("userid must be an integer","userid not valid")
def registration():
    global e31,e32,e33,e34
    root.destroy()
    root31=Tk()
    f30=Frame(root31)
    f31=Frame(root31)
    f32=Frame(root31)
    f33=Frame(root31)
    f34=Frame(root31)
    f35=Frame(root31)

    label30 = Label(f30, text="Student Registration")
    label31 = Label(f31, text="Roll no.")
    label32 = Label(f32, text="Name")
    label33 = Label(f33, text="Address")
    label34 = Label(f34, text="Password")
    label30.config(font=(None,40,'italic'))
    label31.config(font=(None,20,'italic'))
    label32.config(font=(None,20,'italic'))
    label33.config(font=(None,20,'italic'))
    label34.config(font=(None,20,'italic'))
    e31=Entry(f31,font=(None,15,'italic'), borderwidth=2, relief="solid")
    e32=Entry(f32,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())
    e33=Entry(f33,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())
    e34=Entry(f34,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())

    label30.pack(expand=True)
    label31.pack(expand=True,side='left')
    label32.pack(expand=True,side='left')
    label33.pack(expand=True,side='left')
    label34.pack(expand=True,side='left')

    e31.pack(expand=False,side='left')
    e32.pack(expand=False,side='left')
    e33.pack(expand=False,side='left')
    e34.pack(expand=False,side='left')
    
    b31 = Button(f35, text="submit",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:submit1())
    b31.config(borderwidth=2, relief="solid")

    f30.pack(expand=True, fill="both")
    f31.pack(expand=True, fill="both")
    f32.pack(expand=True, fill="both")
    f33.pack(expand=True, fill="both")
    f34.pack(expand=True, fill="both")
    f35.pack(expand=True, fill="both")
    b31.pack()
    root31.mainloop()

def saveadmin():
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    cmd=f"insert into adminuser values ('{userna}','{passwdna}')"
    c.execute(cmd)
    db1.commit()
def submitadmin():
    global userna,passwdna,passwdcna,root
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    userna=e44.get()

    passwdna=e45.get()
    passwdcna=e46.get()

    if not (bool(userna) and bool(passwdna) and bool(passwdcna)):
        messagebox.showinfo("not entered","cu")
    
    
    cmd=f"select * from adminuser where user='{userna}'"
    c.execute(cmd)
    data=c.fetchone()
    if not (bool(data)):
        if passwdna==passwdcna:
            if len(passwdna)>=5 and any(i.isdigit() for i in passwdna):
                saveadmin()
                root41.destroy()
                root=Tk()
                main()
            else:
                messagebox.showinfo("password must contain 5 char and atleast one digit")
        else:
            messagebox.showinfo("password not matched")
    else:
        messagebox.showinfo("user already exixts")
def addadmin():
    f40.destroy()
    f41.destroy()
    f42.destroy()
    global e44,e45,e46
    f43=Frame(root41)
    f44=Frame(root41)
    f45=Frame(root41)
    f46=Frame(root41)
    f47=Frame(root41)
    label43 = Label(f43, text="Add New Admin")
    label44 = Label(f44, text="Admin username")
    label45 = Label(f45, text="Admin Password")
    label46 = Label(f46, text="Confirm Admin Password")
    label43.config(font=(None,40,'italic'))
    label44.config(font=(None,20,'italic'))
    label45.config(font=(None,20,'italic'))
    label46.config(font=(None,20,'italic'))
    e44=Entry(f44,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())
    e45=Entry(f45,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())
    e46=Entry(f46,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())

    b47 = Button(f47, text="submit",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:submitadmin())
    b47.config(borderwidth=2, relief="solid")

    label43.pack(expand=True)
    label44.pack(expand=True,side='left')
    label45.pack(expand=True,side='left')
    label46.pack(expand=True,side='left')

    e44.pack(expand=False,side='left')
    e45.pack(expand=False,side='left')
    e46.pack(expand=False,side='left')
    b47.pack()
    f43.pack()
    f44.pack()
    f45.pack()
    f46.pack()
    f47.pack()
    root41.mainloop()

def editadd2():
    global root
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    addr=e57.get()
    cmd=f"update info set address='{addr}' where rollno={rolle}"
    c.execute(cmd)
    db1.commit()
    root41.destroy()
    root=Tk()
    main()

def editname2():
    global root
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    nam=e57.get()
    cmd=f"update info set name='{nam}' where rollno={rolle}"
    c.execute(cmd)
    db1.commit()
    root41.destroy()
    root=Tk()
    main()
def editadd1():
    f54.destroy()
    f55.destroy()
    global e57
    f56=Frame(root41)
    f57=Frame(root41)
    f58=Frame(root41)
    label56 = Label(f56, text="Edit Student Address")
    label57 = Label(f57, text="Enter New Address")
    label56.config(font=(None,40,'italic'))
    label57.config(font=(None,20,'italic'))
    e57=Entry(f57,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())
    b58 = Button(f58, text="Submit",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:editadd2())
    b58.config(borderwidth=2, relief="solid")
    label56.pack(expand=True)
    label57.pack(expand=True,side='left')
    e57.pack(expand=False,side='left')
    b58.pack()
    f56.pack()
    f57.pack()
    f58.pack()
    root41.mainloop()

def editname():
    f54.destroy()
    f55.destroy()
    global e57
    f56=Frame(root41)
    f57=Frame(root41)
    f58=Frame(root41)
    label56 = Label(f56, text="Edit Student Name")
    label57 = Label(f57, text="Enter New Name")
    label56.config(font=(None,40,'italic'))
    label57.config(font=(None,20,'italic'))
    e57=Entry(f57,font=(None,15,'italic'), borderwidth=2, relief="solid",textvariable=StringVar())
    b58 = Button(f58, text="Submit",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:editname2())
    b58.config(borderwidth=2, relief="solid")
    label56.pack(expand=True)
    label57.pack(expand=True,side='left')
    e57.pack(expand=False,side='left')
    b58.pack()
    f56.pack()
    f57.pack()
    f58.pack()
    root41.mainloop()

def editadd():
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    global e52,rolle
    try:    
        if e52.get():
            rolle=int(e52.get())
        else:
            rolle=-1

        cmd=f"select * from info where rollno={rolle}"
        c.execute(cmd)
        data=c.fetchone()
        if bool(data):
            editstuinfo()
        else:
            messagebox.showinfo("user does not exists")

    except ValueError as v:
        messagebox.showinfo("userid must be an integer","userid not valid")

def editstuinfo():
    f51.destroy()
    f52.destroy()
    f53.destroy()
    global f54,f55
    f54=Frame(root41)
    f55=Frame(root41)
    
    
    b54 = Button(f54, text="Edit Address",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:editadd1())
    b55 = Button(f54, text="Edit Name",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:editname())
    
    b54.config(borderwidth=2, relief="solid")
    b55.config(borderwidth=2, relief="solid")
    b54.pack()
    b55.pack()
    f54.pack()
    f55.pack()
    root41.mainloop()

def editinfo():
    f40.destroy()
    f41.destroy()
    f42.destroy()
    global e52,f51,f52,f53
    f51=Frame(root41)
    f52=Frame(root41)
    f53=Frame(root41)
    label51 = Label(f51, text="Edit Student Info")
    label52 = Label(f52, text="Enter roll number")
    label51.config(font=(None,40,'italic'))
    label52.config(font=(None,20,'italic'))
    e52=Entry(f52,font=(None,15,'italic'), borderwidth=2, relief="solid")

    b53 = Button(f53, text="submit",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:editadd())
    b53.config(borderwidth=2, relief="solid")

    label51.pack(expand=True)
    label52.pack(expand=True,side='left')
    e52.pack(expand=False,side='left')
    b53.pack()
    f51.pack()
    f52.pack()
    f53.pack()
    root41.mainloop()
def admin1():
    global f40,f41,f42,root41
    root.destroy()
    root41=Tk()
    root41.geometry('600x400')
    f40=Frame(root41)
    f41=Frame(root41)
    f42=Frame(root41)
    

    label40 = Label(f40, text="Admin Account")
    
    label40.config(font=(None,40,'italic'))
    
    

    label40.pack(expand=True)
    

   
    b41 = Button(f41, text="Add New Admin",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:addadmin())
    b41.config(borderwidth=2, relief="solid")
    b42 = Button(f42, text="Edit Student Info",font=(None,20,'italic'),bg="#ffffff",height=2,width=15,command=lambda:editinfo())
    b42.config(borderwidth=2, relief="solid")

    f40.pack(expand=True, fill="both")
    f41.pack(expand=True, fill="both")
    f42.pack(expand=True, fill="both")
    
    b41.pack()
    b42.pack()
    root41.mainloop()

def admin():
    db1 = sq.connect(host="localhost",port=3306,user="root",password="",database="tandq")
    c=db1.cursor()
    global usera  
    usera=e1.get()

    passwda=e2.get()
    if not (bool(usera) and bool(passwda)):
        messagebox.showinfo("not entered","cu")
    
    
    cmd=f"select * from adminuser where user='{usera}'"
    c.execute(cmd)
    data=c.fetchone()
    if bool(data):
        if passwda==data[1]:
            admin1()
            root.mainloop()
        else:
            messagebox.showinfo("wrong password")
    else:
        messagebox.showinfo("not a registered user")

def main():
    global e1,e2,e3,e4,root
    root.geometry("1000x700")
    root.config(bg="#b3e763")

    left = Frame(root, borderwidth=2, relief="solid")
    left.config(bg="#b3e763",)
    right = Frame(root, borderwidth=2, relief="solid")
    right.config(bg="#b3e763")
    container = Frame(left, borderwidth=2, relief="solid")
    container.config(bg="#e19586")
    box1 = Frame(right, borderwidth=2, relief="solid")
    box2 = Frame(right, borderwidth=2, relief="solid")
    box1.config(bg="#c9cb23")
    box2.config(bg="#cb233f")
    #admin login start
    f1=Frame(container)
    f2=Frame(container, borderwidth=2, relief="solid")
    f3=Frame(container)
    f3.config(bg="#e19586")

    label1 = Label(f1, text="Admin login")

    f4=Frame(f2)
    f4.config(bg="#e19586")
    f5=Frame(f2)
    f5.config(bg="#e19586")
    label4 = Label(f4, text="Admin Username")
    #label4.grid(row=0,column=0)
    label4.config(font=(None,20,'italic'),bg='#e19586',fg='#000000')
    e1=Entry(f4,font=(None,20,'italic'), borderwidth=2, relief="solid")
    #e1.grid(row=0,column=1)
    label5 = Label(f5, text="Admin Password")
    #label5.grid(row=1,column=0)
    label5.config(font=(None,20,'italic'),bg='#e19586',fg='#000000')
    e2=Entry(f5,font=(None,20,'italic'), borderwidth=2, relief="solid",show="*")
    #e2.grid(row=1,column=1)


    label1.config(font=(None,40,'italic'),bg='#e19586',fg='#000000')
    b1 = Button(f3, text="Login",bg='sky blue',fg='#000000',height=2,width=15,font=(None,20,'italic'),command=lambda:admin())

    #admin login end

    #admin login start
    f6=Frame(box1)
    f7=Frame(box1, borderwidth=2, relief="solid")
    f8=Frame(box1)
    f8.config(bg="#c9cb23")

    label2 = Label(f6, text="Student login")
    label2.config(font=(None,30,'italic'),bg="#c9cb23",fg='#000000')
    b2 = Button(f8, text="Student login")

    f9=Frame(f7)
    f9.config(bg="#c9cb23")
    f10=Frame(f7)
    f10.config(bg="#c9cb23")
    label6 = Label(f9, text="Student Username")
    #label4.grid(row=0,column=0)
    label6.config(font=(None,15,'italic'),bg="#c9cb23",fg='#000000')
    e3=Entry(f9,font=(None,15,'italic'), borderwidth=2, relief="solid")
    #e1.grid(row=0,column=1)
    label7 = Label(f10, text="Student Password")
    #label5.grid(row=1,column=0)
    label7.config(font=(None,15,'italic'),bg="#c9cb23",fg='#000000')
    e4=Entry(f10,font=(None,15,'italic'), borderwidth=2, relief="solid",show="*",textvariable=StringVar())
    #e2.grid(row=1,column=1)



    b2 = Button(f8, text="Login",bg='sky blue',fg='#000000',height=1,width=10,font=(None,15,'italic'),command=lambda :student())


    label3 = Label(box2, text="Student registration")
    label3.config(font=(None,20,'italic'),bg="#cb233f")
    b3 = Button(box2, text="Register for\nTest",font=(None,20,'italic'),bg="#cb233f",height=2,width=15,command=lambda:registration())
    b3.config(borderwidth=2, relief="solid",bg='sky blue')

    left.pack(side="left", expand=True, fill="both")
    right.pack(side="right", expand=True, fill="both")
    container.pack(expand=True, fill="both", padx=5, pady=5)
    box1.pack(expand=True, fill="both", padx=10, pady=10)
    box2.pack(expand=True, fill="both", padx=10, pady=10)

    f1.pack(expand=True, fill="both")
    f2.pack(expand=True, fill="both",padx=10, pady=10)
    f3.pack(expand=True, fill="both")
    f4.pack(expand=True, fill="both")
    f5.pack(expand=True, fill="both")

    f5.pack(expand=True, fill="both")
    f6.pack(expand=True, fill="both",padx=10, pady=10)
    f7.pack(expand=True, fill="both")
    f8.pack(expand=True, fill="both")
    f9.pack(expand=True, fill="both")
    f10.pack(expand=True, fill="both")

    b1.pack(side='bottom')
    label1.pack(expand=True, fill="both")
    label3.pack(expand=True,fill="both")
    label4.pack(expand=True, fill="both",side='left')
    label5.pack(expand=True, fill="both",side='left')

    label2.pack(expand=True, fill="both")
    label6.pack(expand=True, fill="both",side='left')
    label7.pack(expand=True, fill="both",side='left')

    e1.pack(expand=False,side='left')
    e2.pack(expand=False,side='left')

    e3.pack(expand=False,side='left')
    e4.pack(expand=False,side='left')

    b2.pack(side="bottom")
    b3.pack(side="bottom",expand=FALSE)
    root.mainloop()

main()
root.mainloop()
