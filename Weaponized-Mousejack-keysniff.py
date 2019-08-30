#GainSec
#Keysniff/Mousejack Weaponized Tool


import sqlite3
import os
import datetime
import urllib
import re
import tabulette

#assign variable database to the name of the db stored on the computer
database = 'finaldb.db'
#connect to said database
dbcon = sqlite3.connect(database)
#grab = open('flog', 'r')

#function to check for database connection
def dbcheck():
  try:
    dbcon = sqlite3.connect(database)
    print('Database Connected')
  except dbcon.DatabaseError:
    print('Cant Find Database')
    exit(0)

#function to check if log file is open correctly
def logcheck():
    try:
        grab = open('flog', 'r')
        print('State of Log File(If True it is not open): ', grab.closed)
        readgrab = grab.read()
      #  print (readgrab)
        grab.close()
    except readgrab == ' ':
       print('Cant read from log file')

#function to check if jackit table exists, if it doesn't it asks user if they want to make the table
def dbcheck2():
    try:
       # dbcon = sqlite3.connect(database)
        dbcon.execute('SELECT * FROM jackit')
        print('jackit Table exists already!')
    except dbcon.DatabaseError:
        print('Table \"jackit"/ doesnt exist, would you like to make it? ')
        answer = input('Enter 1 to create table, 2 to exit')
        if answer == '1':
            dbcon.execute('CREATE TABLE jackit  (address TEXT, date TEXT, vendor TEXT, success TEXT)')
            dbcon.commit()
            print('jackit Table created!')
#pulls all the dongle addresses (like mac addresses) from the log file
#It uses the re.compile to search for instance where any number or any capital letter has a colon before and after it
#it only grabs the ones that have 10 instances of this
#It uses the users entry for how many dongles there are (3 in this case) to find the entry number from adrtag
#every 4 strings re.findall found were correct so thats why it goes 0,4,8,12 etc.
#Then sends it to the database after listing it for the user to be sure
def macgrab():
    mgrab = open('flog', 'r')
    readmgrab = mgrab.read()
    madr = re.compile(u'(?:[0-9A-F]:?){10}')
    adrmgrab = str(madr)
    adrtag = re.findall(madr, readmgrab)
    #print(adrtag)
    print('How many Dongles are there listed? ')
    dongnum = input()
    dongnum = int(dongnum) - 1
    x = dongnum
    list = [0, 4, 8, 12, 16, 20, 24, 28, 32]
    while int(dongnum) >= 0:
        x = int(x)
        print('Entry from file: ',list[x])
        print('Address are: ',adrtag[list[x]])
        #maclist = []
        #maclist.append(adrtag[list[x]])
        #macstring = "".join(str(x) for x in maclist)
        #print('macstring = ', macstring)
        #print('maclist = ',maclist)
        with dbcon:
            dbcon.executemany("INSERT into jackit (address) VALUES(?)",adrtag[list[x]])
            dongnum = int(dongnum) - 1
            x = int(x) - 1
#Function to pull the vendor types of the dongles from the log file
#After that it prompts user to say how many dongles (in this case 3)
#It'll then use that to pull the correct vendor lists because
#re.compile used below first result (result 0)
#Is part of the headers in the log file
#Then it enters it into database            
def vendors():
    venlog = open('flog', 'r')
    vengrab = venlog.read()
    ven = re.compile(u'([L-M]........)')
    vgrab = str(ven)
    ventag = re.findall(ven, vengrab)
    #print(ventag)
    print('How many Dongles are there listed? ')
    vnum = input()
    vnum = int(vnum) - 1
    y = vnum
    vlist = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    while vnum >=0:
        z = int(vnum)
        z = int(z)
        vendors = ventag[vlist[z]]
        print('Vendor Entry: ',vendors)
        with dbcon:
            dbcon.executemany("INSERT into jackit (vendor) VALUES(?)",ventag[vlist[z]])
     #   vendors = ventag[vlist[z]]
        vnum = int(vnum) - 1
        z = int(z) - 1      

#Keeps track of success rate and then enters it into database       
def success():
    print('Was the attack successful for all devices tried? Type 1 for yes and 2 for no')
    suc = input()
    suc = str(suc)
    if suc == '1':
        print('Attacks were successful!')
        with dbcon:
            dbcon.executemany("INSERT into jackit (success) VALUES(?)", suc)
    else:
        print('Maybe Next Time!')
        with dbcon:
            dbcon.executemany("INSERT into jackit (success) VALUES(?)", suc)

#Finds Date+Time and enteres it into database
def date():
    current_time = datetime.datetime.now().time()
    print('Time Now: ', current_time)
    with dbcon:
        dbcon.executemany("INSERT into jackit (date) VALUES(?)", str(current_time))


#function to run everything
def test():
    menu1()
    dbcheck()
    dbcheck2()
    logcheck()
    macgrab()
    vendors()
    success()
    date()  

#Function to check password, basically the same as in the other program
def menu1():
    passfilecheck = open('passfile', 'r')
    print('Have you set a password? Enter 1 for Yes or 2 for No')
    setpass = input()
    if setpass == '2':
        passfilecheck.close()
        print('Please set a PIN for log files')
        password = input()
        print('Your Pin Is: ', password)
        passfilecheck = open('openfile', 'w+')
        int(password)
        hiddenpass = password * 12345
        int(hiddenpass)
        passfilecheck.write(str(hiddenpass))
    elif setpass == '1':
        print('Please enter your PIN')
        securitycheck = input()
        passfilecheck = open('passfile', 'r')
        enpass = passfilecheck.read()
        int(securitycheck)
        securitycheck = securitycheck * 12345
        int(securitycheck)
        passfilecheck.close()
        if securitycheck == enpass:
            print('Welcome Back')
            passfilecheck.close()
        else:
            print('incorrect password')

#Run the test function!
test()
