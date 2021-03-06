import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS card")
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)")
class User:
    def __init__(self):
        self.number = None
        self.pin = None
        self.curnumber = None
        self.curpin = None
    def result(self):
        def getchecksum(self, inputstring):
            sum = 0
            for el in inputstring:
                sum += int(el)
            checksum = (sum + 9) // 10 * 10 - sum
            return checksum
        def tochanged(self, inputstring):
            return ''.join(map(str, [i - 9 if i > 9 else i for i in
                                     [int(i) if k % 2 != 0 else int(i) * 2 for k, i in enumerate(inputstring)]]))
        number = '400000' + ''.join(["%s" % random.randint(0, 9) for i in range(0, 9)])
        number2 = tochanged(self, number)
        self.number = number + str(getchecksum(self, number2))
        return self.number
    def generatepin(self):
        self.pin = ''.join(["%s" % random.randint(0, 9) for i in range(0, 4)])
        return  self.pin
user = User()
def luhncheck(inputstring):
    st = ''.join(map(str, [i - 9 if i > 9 else i for i in
                                     [int(i) if k % 2 != 0 else int(i) * 2 for k, i in enumerate(inputstring[:-1])]]))
    sum = 0
    for el in st:
        sum += int(el)
    checksum = int(inputstring[-1])
    return (sum + checksum) % 10 == 0
def startmenu():
    choice = input('1. Create an account\n2. Log into account\n0. Exit\n')
    if choice == '1':
        createacc()
    elif choice == '2':
        return logtoacc()
    elif choice == '0':
        print('Bye!')
def createacc():
    print('Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}\n'.format(user.result(),user.generatepin()))
    cur.execute("INSERT INTO card(number, pin) VALUES(?, ?)", (user.number, user.pin))
    conn.commit()
    return startmenu()
def inacc():
    choice = input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
    if choice == '1':
      print("Balance: {}".format(cur.execute('select balance from card where number = ? and pin = ?',(int(user.curnumber),int(user.curpin))).fetchone()[0]))
      print('\n')
      return inacc()
    if choice == '2':
        cur.execute('update card set balance = balance + ? where number = ? and pin = ?',(int(input('Enter income:')),int(user.curnumber),int(user.curpin)))
        print('\n')
        conn.commit()
        print('Income was added!')
        print('\n')
        return inacc()
    if choice == '3':
        print('Transfer')
        transto = input('Enter card number:')
        if luhncheck(transto) == False:
            print('Probably you made a mistake in the card number. Please try again!')
        if cur.execute('select number from card where number = ?',(int(transto),)).fetchone() == None:
            print('Such a card does not exist.')
        if cur.execute('select number from card where number = ?', (int(transto),)).fetchone() != None:
            print('Enter how much money you want to transfer:')
            howmuch = input('Enter how much money you want to transfer:')
            if int(howmuch) > cur.execute('select balance from card where number = ? and pin = ?',(int(user.curnumber),int(user.curpin))).fetchone()[0]:
                print('Not enough money!')
            else:
                cur.execute('update card set balance = ? where number = ?',(howmuch,transto))
                cur.execute('update card set balance = balance - ? where number = ?', (howmuch, user.curnumber))
                print('Success!')
        conn.commit()
        return inacc()
    if choice == '4':
        cur.execute('delete * from card where number = ?',(user.curnumber,))
        print('The account has been closed!')
        conn.commit()
        return startmenu()
    if choice == '0':
        print('Bye!')
def logtoacc():
    num = input('Enter your card number:')
    pin = input('Enter your PIN:')
    print('\n')
    if cur.execute('select number,pin from card where number = ? and pin = ?',(int(num),int(pin))).fetchone() != None:
     print('You have successfully logged in!\n')
     user.curnumber = num
     user.curpin = pin
     return inacc()
    else:
     print('Wrong card number or PIN!')
     return startmenu()

startmenu()
