import sqlConnector
import sqlalchemy
import pandas as pd

def finalSum():
    engine = sqlalchemy.create_engine('mysql+pymysql://root:12345@localhost:3306/checkData')
    df=pd.read_sql_table('checks',engine,columns=['amount'])
    sum=df.sum(axis=0)
    sum=str(sum)
    sum=sum.split('\n')
    return sum[0][10:]
if __name__ == '__main__':
    print(finalSum())
    while True:
        permission=input('To end press "n" else enter')
        if (permission=='n'):
            quit()
        print('Enter the values as told:- ')
        checkNumber=input('Enter the check number')
        issueDate=input('Enter issue date')
        partyName=input('Enter partyName: ')
        amount=int(input('Enter amount: '))
        passDate=input('Enter passDate: ')

        dataCollection= 'Insert into checks (checkNumber,issuedate,partyName, amount,passDate) values (%s,%s,%s,%s,%s)'
        datas=[(checkNumber,issueDate,partyName,amount,passDate)]

        sqlConnector.mycursor.executemany(dataCollection,datas)

        sqlConnector.myDataBase.commit()