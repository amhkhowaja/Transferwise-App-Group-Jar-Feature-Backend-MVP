import json
import time
from datetime import datetime
from flask import Flask, jsonify

app= Flask(__name__)
@app.route("/")
def index():
    return "WISE GroupJar API"

class AccountHolder:
    def __init__(self, id , name , amount, currency, right=True):
        self.__id= id
        self.__name= name
        self.__amount= amount
        self.__currency=currency
        self.__Right=right
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)
        
        jarobj= self.get_dict()
        jsonfile['account_holders'].append(jarobj)
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
    def get_name(self):
        return self.__name
    def get_amount(self):
        return self.__amount
    def add_amount(self, amount):
        #object oriented action
        self.__amount+=amount
        #opening file
        with open('groupjar.json') as file:
            jsonfile=json.load(file)
        #filter the account_holder record
        ac=list(filter(lambda x: x['id']==self.get_id(),jsonfile['account_holders']))[0]
        #action
        ac['amount']=self.get_amount()
        #writing file
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
    def get_id(self):
        return self.__id
    def get_currency(self):
        return self.__currency
    def has_Right(self):
        return self.__Right
    def deposite(self,jar, amount):
        if self.__currency==jar.get_currency():
            if self.__amount>=amount:
                self.__amount-=amount#
                jar.add_amount(amount)#
                transaction = Transaction('CREDIT', amount,self)
                jar.add_transaction(transaction)
                 #json part:
                #opening file
                with open('groupjar.json') as file:
                    jsonfile=json.load(file)
                #filter the entities record
                print(self.get_id())
                ac=list(filter(lambda x: x['id']==self.get_id(),jsonfile['account_holders']))[0]
                jr=list(filter(lambda x: x['id']==jar.get_id(),jsonfile['jar']))[0]

                #action
                ac['amount']=self.get_amount()
                jr['amount']=jar.get_amount()
                #writing file
                j=json.dumps(jsonfile, indent=4)
                with open('groupjar.json', 'w') as file:
                    file.write(j)            
            else:
                print("{} does not have enough money".format(self.get_name()))
        else :
            print("the currency is different than jar's currency ")
    def withdraw_money(self, jar, amount):
        if self.has_Right() and self.__currency==jar.get_currency():
            if jar.get_amount()>=amount:
                jar.withdraw_amount(amount)
                self.add_amount(amount)
                transaction = Transaction('DEBIT', amount,self)
                jar.add_transaction(transaction)
                #json part:
                with open('groupjar.json') as file:
                    jsonfile=json.load(file)

                #filter the entities record
                ac=list(filter(lambda x: x['id']==self.get_id(),jsonfile['account_holders']))[0]
                jr=list(filter(lambda x: x['id']==jar.get_id(),jsonfile['jar']))[0]

                #action
                ac['amount']=self.get_amount()
                jr['amount']=jar.get_amount()
                #writing file
                j=json.dumps(jsonfile, indent=4)
                with open('groupjar.json', 'w') as file:
                    file.write(j)            
            else:
                print("{} does not have enough money".format(jar.get_name()))
        else :
            print("You donot have right to withdraw the amount ")
    def get_dict(self):
        d= {
            'id': self.get_id(),
            'name': self.get_name(),
            'amount': self.get_amount(),
            'currency': self.get_currency(),
            'right': self.has_Right()
        }
        return d
    
class Jar:
    __account_holders:AccountHolder

    def __init__(self, id,name, currency, admins):
        
        self.__id= id
        self.__amount=0
        self.__name=name 
        self.__currency= currency
        self.__type = "GROUP"
        self.admins = [admins]
        self.account_holders=[admins]
        self.transactions=[]
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)
        
        jarobj= self.get_dict()
        jsonfile['jar'].append(jarobj)
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
    def get_name(self):
        return self.__name
    def get_id(self):
        return self.__id
    def get_amount(self):
        return self.__amount
    def get_currency(self):
        return self.__currency
    def get_type(self):
        return self.__type
    def get_acount_holders(self):
        return self.account_holders
    def get_admins(self):
        return self.admins
    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)

        #filter the entities record
        jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]

        #action
        jr['transactions'].append(transaction.get_dict())
        #writing file
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
    def get_all_transaction(self):
        return self.transactions
    def add_member(self, user):
        self.account_holders.append(user)
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)

        #filter the entities record
        print(self.get_id())
        jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]
        print(jr)

        #action
        jr['account_holders'].append(user.get_dict())
        #writing file
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
    
    def remove_member(self, user):
        if user in self.__account_holders:
            self.account_holders.remove(user)
            #json part:
            with open('groupjar.json') as file:
                jsonfile=json.load(file)

            #filter the entities record
            jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]

            #action
            jr['account_holders'].remove(user.get_dict())
            if (user.get_dict() in jr['admins']):
                jr['admins'].remove(user.get_dict())
            #writing file
            j=json.dumps(jsonfile, indent=4)
            with open('groupjar.json', 'w') as file:
                file.write(j)
        else:
            print("cannot remove the user {}".format(user))
    #make admin
    def make_admin(self, user):
        if user in self.account_holders:
            self.admins.append(user)
            #json part:
            with open('groupjar.json') as file:
                jsonfile=json.load(file)

            #filter the entities record
            jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]

            #action
            jr['admins'].append(user.get_dict())
            #writing file
            j=json.dumps(jsonfile, indent=4)
            with open('groupjar.json', 'w') as file:
                file.write(j)
        else :
            print("{} is not the member of this jar".format(user))
    def remove_admin(self, user):
        if user in self.admins:
            self.admins.remove(user)
            #json part:
            with open('groupjar.json') as file:
                jsonfile=json.load(file)

            #filter the entities record
            jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]

            #action
            jr['admins'].remove(user.get_dict())
            #writing file
            j=json.dumps(jsonfile, indent=4)
            with open('groupjar.json', 'w') as file:
                file.write(j)
    def add_amount(self, amount):
        self.__amount+=amount  
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)

        #filter the entities record
        jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]

        #action
        jr['amount']+=amount
        #writing file
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
    def withdraw_amount(self, amount):
        self.__amount -=amount  
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)

        #filter the entities record
        jr=list(filter(lambda x: x['id']==self.get_id(),jsonfile['jar']))[0]
        print(jr)

        #action
        jr['amount']-=amount
        #writing file
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)  
    
    def get_dict(self):
        d={
            'id':self.get_id(),
            'name': self.get_name(),
            'amount': self.get_amount(),
            'currency': self.get_currency(),
            'type': self.get_type(),
            'admins':list(map(lambda x: x.get_dict(),self.get_admins())),
            'account_holders':list(map(lambda x: x.get_dict(),self.get_acount_holders())),
            'transactions':list(map(lambda x: x.get_dict(),self.get_all_transaction())),
        }
        return d

    

class Transaction:
    def __init__(self, type, amount, sender):
        self.__id=datetime.now().__str__()
        self.__type=type #debit #credit
        self.__amount=amount
        self.sender=sender
        #json part:
        with open('groupjar.json') as file:
            jsonfile=json.load(file)
        
        jarobj= self.get_dict()
        jsonfile['transactions'].append(jarobj)
        j=json.dumps(jsonfile, indent=4)
        with open('groupjar.json', 'w') as file:
            file.write(j)
        
    def get_type(self):
        return self.__type
    def get_id(self):
        return self.__id
    def get_amount(self):
        return self.__amount
    def get_sender(self):
        return self.sender
    def get_dict(self):
        a = {
            'id': self.get_id(),
            'type': self.get_type(),
            'amount': self.get_amount(),
            'sender': self.get_sender().get_dict()  
        }
        return a
    
if __name__ == "__main__":
    ac1= AccountHolder(1, "Aadarsh Mehdi",  500, "EUR")
    eur = Jar(123,'Family','EUR', ac1)
    ac2= AccountHolder(2, "Makhlug Jafarov", 2000, "EUR", right =False)
    ac3= AccountHolder(3, "Bayram", 5000, "EUR", right =False)
    eur.add_member(ac2)
    eur.add_member(ac3)
    print("Before depositing : "+str(eur.get_amount()))
    print("Before depositing : "+str(list(map(lambda x : x.get_type(),eur.get_all_transaction()))))

    ac1.deposite(eur, 250)
    ac2.deposite(eur, 500)
    print("After depositing : "+str(eur.get_amount()))
    print("After depositing : "+str(list(map(lambda x : x.get_type(),eur.get_all_transaction()))))
    
    time.sleep(1)
    #after
    ac1.withdraw_money(eur, 500)
    print("After withdrawing : "+str(eur.get_amount()))
    print("After withdrawing : "+str(list(map(lambda x : x.get_type(),eur.get_all_transaction()))))
    
    print(list(map(lambda x : x.get_name(),eur.get_acount_holders())))
    