#imported files//classes
from classes import *

#main menu
while 1 :
    print("------------------------------------------------------------------------")
    result = int(input("Choose user type: 1.Admin 2.student 3.exit\n"))
    if result==1 :
        user =  Admin() #create an object from Admin class
        user.menu() #display Admin menu

    elif result==2 :
        user =  Student() #create an object from Student class
        user.menu() #display Student menu

    elif result==3 :
        print("BYE! ^_^")
        exit(0) #exit the main menu

    else :
        print("invalid user type -_-")