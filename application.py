import csv
from functools import partial

import sqlalchemy
import pandas as pd
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os
import mysql.connector


class gui:
    
    def __init__(self,root):
        self.root = root
        titlespace=" "
        self.root.title(100*titlespace+"Cheque Collector")
        self.root.geometry("850x750+330+0")
        self.root.resizable(width=False,height=False)
###############################################################################################
        MainFrame= Frame(self.root,bd=10,width=770,height=700,relief=RIDGE,bg='cadet blue')
        MainFrame.grid()

        TitleFrame= Frame(MainFrame,bd=7,width=770,height=100,relief=RIDGE)
        TitleFrame.grid(row=0,column=0)
        TopFrame3= Frame(MainFrame,bd=5,width=770,height=500,relief=RIDGE)
        TopFrame3.grid(row=1,column=0)

        LeftFrame = Frame(TopFrame3, bd=5, width=770, height=400, relief=RIDGE,padx=2, bg='cadet blue')
        LeftFrame.pack(side=LEFT)
        LeftFrame1 = Frame(LeftFrame, bd=5, width=600, height=180, relief=RIDGE, padx=2,pady=9)
        LeftFrame1.pack(side=TOP)

        RightFrame = Frame(TopFrame3, bd=5, width=100, height=400, relief=RIDGE,padx=2, bg='cadet blue')
        RightFrame.pack(side=RIGHT)
        RightFrame1a = Frame(RightFrame, bd=5, width=90, height=300, relief=RIDGE, padx=12,pady=4)
        RightFrame1a.pack(side=TOP)
#======================================================================================================

        chequeNumber=StringVar()
        issueDate=StringVar()
        partyName=StringVar()
        amount=StringVar()
        passDate=StringVar()
#================================================
        def exit():
            iExit = tkinter.messagebox.askyesno("PMH","Confirm you want to exit")
            if iExit>0:
                root.destroy()
                return
        def reset(label):
            self.entCheckNumber.delete(0,END)
            #self.entissueDate.delete(0,END)
            self.entpartyName.delete(0,END)
            self.entAmount.delete(0,END)
            #self.entPassDate.delete(0,END)
            finalSum(label)
        def addData(label):
            if chequeNumber.get()=="" or issueDate.get()=="" or partyName.get()=="" or amount.get()=="":
                tkinter.messagebox.showerror("PMH","Enter the values correctly")
            else:

                myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345",database='pmh')
                mycursor = myDataBase.cursor()
                dataCollection = 'Insert into checks (chequeNumber,issuedate,partyName, amount,passDate) values (%s,%s,%s,%s,%s)'
                datas = [(chequeNumber.get(), issueDate.get(), partyName.get(), amount.get(), passDate.get())]

                mycursor.executemany(dataCollection, datas)
                myDataBase.commit()
                myDataBase.close()
                finalSum(label)
                reset(label)

        def displayName(label):
            myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345", database='pmh')
            mycursor = myDataBase.cursor()
            mycursor.execute("select * from checks")
            result = mycursor.fetchall()
            if len(result)!=0:
                self.check_records.delete(*self.check_records.get_children())
                for row in result:
                    self.check_records.insert('',END,values=row)
            myDataBase.commit()
            myDataBase.close()
            finalSum(label)
        def Traineinfo(ev):
            viewInfo=self.check_records.focus()
            learnerData=self.check_records.item(viewInfo)
            row=learnerData['values']
            chequeNumber.set(row[0])
            issueDate .set(row[1])
            partyName .set(row[2])
            amount .set(row[3])
            passDate .set(row[4])

        def update(label):
            myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345", database='pmh')
            mycursor = myDataBase.cursor()

            mycursor.execute( 'update checks set issuedate=%s,partyName=%s,amount=%s,passDate=%s where chequeNumber=%s',(
                issueDate.get(),
                partyName.get(),
                amount.get(),
                passDate.get(),
                chequeNumber.get(),
          ))
            myDataBase.commit()

            myDataBase.close()
            tkinter.messagebox.showinfo("PMH", "Updated Successfully")
            finalSum(label)

        def delete(label):
            myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345", database='pmh')
            mycursor = myDataBase.cursor()
            mycursor.execute("delete from checks where chequeNumber=%s",(
                chequeNumber.get(),
            ))
            myDataBase.commit()
            displayName(label)
            myDataBase.close()
            tkinter.messagebox.showinfo("PMH", "Deleted Successfully")
            finalSum(label)
        def search(label):
             try:
                myDataBase = mysql.connector.connect(host="localhost", user="root", passwd="12345", database='pmh')
                mycursor = myDataBase.cursor()
                mycursor.execute("select * from checks where partyName='%s'"%partyName.get().upper())
                getData=mycursor.fetchall()

                with open('searchData.csv','w') as f:
                    fieldnames = ['Cheque Number', 'Issue Date','Party Name','Amount','Pass Date']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)

                    writer.writeheader()
                    for i in range(len(getData)):
                     writer.writerow({'Cheque Number': getData[i][0], 'Issue Date': getData[i][1],'Party Name':getData[i][2],'Amount':getData[i][3],'Pass Date':getData[i][4]})
                    f.close()
                    os.system('searchData.csv')
                    finalSum(label)

             except  :
                  tkinter.messagebox.showinfo("PMH",'Search Error')
                  reset(label)
                  finalSum(label)

             myDataBase.close()

        def finalSum(label):
            engine = sqlalchemy.create_engine('mysql+pymysql://root:12345@localhost:3306/pmh')
            df = pd.read_sql_table('checks', engine, columns=['amount'])
            sum = df.sum(axis=0)
            sum = str(sum)
            sum = sum.split('\n')
            finalData=sum[0][10:]
            label.config(text=finalData)
#################################################################################################
        self.lbltitle=Label(TitleFrame,font=('arial',35,'bold'),text="PRADIP MEDICAL HALL",bd=7)
        self.lbltitle.grid(row=0,column=0,padx=132)
#####################################################################################################


        self.lblcheckNumber=Label(LeftFrame1,font=('arial',12,'bold'),text='Check Number',bd=7)
        self.lblcheckNumber.grid(row=0,column=0,sticky=W,padx=5)
        self.entCheckNumber=Entry(LeftFrame1,font=('arial',12,'bold'),bd=5,width=44,justify='left',textvariable=chequeNumber)
        self.entCheckNumber.grid(row=0,column=1,sticky=W,padx=5)

        self.lblissueDate = Label(LeftFrame1, font=('arial', 12, 'bold'), text='Issue Date', bd=7)
        self.lblissueDate.grid(row=1, column=0, sticky=W, padx=5)
        self.entissueDate = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=issueDate)
        self.entissueDate.grid(row=1, column=1, sticky=W, padx=5)

        self.lblpartyName = Label(LeftFrame1, font=('arial', 12, 'bold'), text='Party Name', bd=7)
        self.lblpartyName.grid(row=2, column=0, sticky=W, padx=5)
        self.entpartyName = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=partyName)
        self.entpartyName.grid(row=2, column=1, sticky=W, padx=5)

        self.lblamount = Label(LeftFrame1, font=('arial', 12, 'bold'), text='Amount', bd=7)
        self.lblamount.grid(row=3, column=0, sticky=W, padx=5)
        self.entAmount = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=amount)
        self.entAmount.grid(row=3, column=1, sticky=W, padx=5)

        self.lblpassDate = Label(LeftFrame1, font=('arial', 12, 'bold'), text="Pass Date", bd=7)
        self.lblpassDate.grid(row=4, column=0, sticky=W, padx=5)
        self.entPassDate = Entry(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left',textvariable=passDate)
        self.entPassDate.grid(row=4, column=1, sticky=W, padx=5)

        self.lbltotalSum = Label(LeftFrame1, font=('arial', 12, 'bold'), text='Total Expenditure: ', bd=7)
        self.lbltotalSum.grid(row=5, column=0, sticky=W, padx=5)
        self.enttotalSum = Label(LeftFrame1, font=('arial', 12, 'bold'), bd=5, width=44, justify='left')
        self.enttotalSum.grid(row=5, column=1, sticky=W, padx=5)
#######################################################################################################################
        scroll_y = Scrollbar(LeftFrame,orient=VERTICAL)
        self.check_records = ttk.Treeview(LeftFrame,height=14,columns=('chequeNumber','issuedate','partyName','amount','passDate'),yscrollcommand=scroll_y.set)
        scroll_y.pack(side=RIGHT,fill=Y)

        self.check_records.heading("chequeNumber",text="Check Number")
        self.check_records.heading("issuedate",text="Issue Date")
        self.check_records.heading("partyName",text="Party Name")
        self.check_records.heading("amount",text="Amount")
        self.check_records.heading("passDate",text="Pass Date")
        
        self.check_records['show']='headings'


        self.check_records.column("chequeNumber", width=70)
        self.check_records.column("issuedate", width=70)
        self.check_records.column("partyName", width=70)
        self.check_records.column("amount", width=70)
        self.check_records.column("passDate", width=70)
        
        self.check_records.pack(fill=BOTH,expand=1)
        self.check_records.bind("<ButtonRelease-1>",Traineinfo)
        displayName(self.enttotalSum)
#==================================================================================================================
        sum=partial(addData,self.enttotalSum)
        updater=partial(update,self.enttotalSum)
        deleter=partial(delete,self.enttotalSum)
        searcher=partial(search,self.enttotalSum)
        display=partial(displayName,self.enttotalSum)
        re=partial(reset,self.enttotalSum)

        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="SAVE", bd=4, padx=24,pady=1,width=8,height=2,command=sum).grid(row=0,column=0,padx=1)
        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="UPDATE", bd=4, padx=24,pady=1,width=8,height=2,command=updater).grid(row=1,column=0,padx=1)
        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="DELETE", bd=4, padx=24,pady=1,width=8,height=2,command=deleter).grid(row=2,column=0,padx=1)
        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="SEARCH", bd=4, padx=24,pady=1,width=8,height=2,command=searcher).grid(row=3,column=0,padx=1)
        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="DISPLAY", bd=4, padx=24, pady=1, width=8,height=2,command=display).grid(row=4, column=0, padx=1)
        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="RESET", bd=4, padx=24,pady=1,width=8,height=2,command=re).grid(row=5,column=0,padx=1)
        self.btnAddNew=Button(RightFrame1a,font=('arial', 12, 'bold'), text="EXIT", bd=4, padx=24,pady=1,width=8,height=2,command=exit).grid(row=6,column=0,padx=1)

if __name__ == '__main__':
    root=Tk()
    application = gui(root)
    root.mainloop()
