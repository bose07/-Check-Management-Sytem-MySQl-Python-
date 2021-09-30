from os.path import exists
import csv


def calculate_totalMoney():
    val=[]
    data=0
    if exists('transaction.txt'):
        with open('transaction.txt','r') as f:
            getData=f.read()

            getData=getData.split(" ")
            for i in range(len(getData)):
                val.append(getData[i])
    else:
        story=open('transaction.txt','r')
        getData = story.read()

        getData = getData.split(" ")
        for i in range(len(getData)):
            val.append(getData[i])

    for j in range(len(val)):
        if (val[j]==""):
            continue
        else:
            data+=int(val[j])

    f.close()
    if exists('transaction.txt'):
        with open('transaction.txt','r') as r:
                stripped = (line.strip() for line in r)
                lines=(line.split(' ') for line in stripped if line)
                with open('values.csv','a') as val:
                    writer = csv.writer(val)
                    writer.writerow(('Check Number','Party Name','Amount'))
                    writer.writerow(lines)

    return data


if __name__ == '__main__':
    print("If you want to stop press s ")
    while True:
        print(calculate_totalMoney())
        wantToContinue=input('Want To Continue')
        if (wantToContinue == 'n'):
            quit()
        checkNumber = input('Enter Check Number: ')
        partyName = input("Enter the PartyName: ")
        amount = input("Enter the amount: ")
        # todo CheckDate and CheckPassing Dates are to be added automatically
        toAdd=checkNumber+" "+partyName+" "+amount+"\n"

        transation=amount+" "
        if exists('storage.txt'):
            with open('storeage.txt','a') as store:
                store.write(toAdd)
                store.close()
            with open('transaction.txt','a') as trans:
                trans.write(transation)
        else:
            ledger = open('storeage.txt','a')
            ledger.write(toAdd)
            ledger.close()
            with open('transaction.txt','a') as trans:
                trans.write(transation)

