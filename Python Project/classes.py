import glob
import matplotlib.pyplot as plt


class User: #User (parent) class, here the general functions will be implemented
    
    def __init__(self): #constructor
     print("Calling parent constructor (User)")
     
    def menu(self): #main function, will be overriden in sub-classes Admin & Student
     print("available opeartions")
     
    def getAndCheckId(self): #function to get an ID and make sure that it's in the right format
        ID = input("Enter student ID : ")
        #raising errors if the ID is in wrong fromat
        if ID.isspace() == 1 or ID=="" : #if ID=space (or the user did not enter a value for the ID)
            raise Exception("Missing information!! please fill the required field")
        if ID[-1]==" " : #to remove the last character from the ID if it was a space
            ID = ID[:-1]
        if ID.isdigit()!= 1 : #if ID contains characters/special characters raise an exception
            raise Exception("Invalid ID number!! ID must only be numbers")
        if len(ID)!=7 :
            raise Exception("ID must contain 7 numbers (e.g: 1191042)")
        return ID
    
    def searchRecord(self,id): #function to check if ID(record file) exists or not 
        file_name = id + ".txt"
        status = 0
        try:
            fi = open(file_name, "r")
        except IOError: #id does not exist ,record not found
            status = -1
        else: #id exists ,record found
            fi.close()
        return status
    
    
    #functions used in studentStatics and globalStatics
    def getRemainingCourses(self,st_course,course):
        counter=0
        remaining_courses=[]
        for i in range(len(course)) :
            counter=0
            for j in range(len(st_course)):
                if str(st_course[j]).upper() == course[i]:
                    counter+=1
            if counter == 0:
                remaining_courses.append(course[i]) 
        return remaining_courses      

    def courseFileManipulation(self):
        f_hours=[]
        f_course=[]
        f1= open ("courses.txt","r") #Open file of  ENCS and ENEE courses  for computer engineering program
        data1 = f1.readlines()# read file line by line
        for line in data1:
            li = line.split(" ")
            f_course.append(li[0])# list that contains all required courses
            li[1] = str(li[1]).replace("\n", "") # Remove the newline signal
            f_hours.append(li[1]) # list that contains the credit hours of each required course
        return f_course,f_hours

    def getStudentInfo(self,id):
        #local variables 
        avg_per_sem=[] #list that represents student average per semester.
        hours_per_sem=[] #list that represents student taken hours per semester.
        student_courses_per_sem=[] #list that represents student courses per semester.
        student_grades_per_sem=[] #list that represents student grades per semester.
        student_courses=[]#list that represents student courses for all semesters.
        x=[]
        y=[]
        info=[]
        taken_hours=0
        total=0
        avg=0
        course_sum=0
        courses,hours=self.courseFileManipulation()
        student_info = id + ".txt"
        f2= open (student_info,"r") # Open student record file
        data2 = f2.readlines() 
        for line in data2: # read file line by line
            li = line.split(";")# split the data from file 
            li[1] = str(li[1]).replace("\n", ",") # to handle file format structure.
            y.append(li[0])#year and semester list
            x.append(li[1])#courses and grades list
        for i in x:# to extract student info for each sem.
            courses_grades=str(i)[1:len(str(i))-1].split(", ")
            for j in courses_grades:
                info = str(j).split(" ")
                student_courses_per_sem.append(info[0])
                student_courses.append(info[0])
                student_grades_per_sem.append(info[1]) 
            for k in range(len(student_courses_per_sem)) :#loop over all courses taken by student in a semester
                for h in range(len(courses)): #loop over all required courses
                    if str(student_courses_per_sem[k]).upper() == str(courses[h]):#search for a match
                        course_sum =int(hours[h])*int(student_grades_per_sem[k])#to calculate the grade of each taken course
                        taken_hours = taken_hours + int(hours[h])
                        total = total + course_sum 
                        course_sum=0
            hours_per_sem.append(taken_hours)        
            avg=total/taken_hours
            avg_per_sem.append(avg)
            student_courses_per_sem.clear()#clear for the next record
            student_grades_per_sem.clear()
            total=0
            taken_hours=0
        rc=self.getRemainingCourses(student_courses,courses)              
        return y ,avg_per_sem ,hours_per_sem,rc

    def plotHisto(self,avg_list,med_avg):
        plt.style.use('fivethirtyeight')
        bins = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # average range
        plt.hist(avg_list, bins=bins, edgecolor='black')
        median_avg = med_avg
        color = '#fc4f30'
        plt.axvline(median_avg, color=color, label='Average Median', linewidth=2)
        plt.legend()
        plt.title('Average distribution of students')
        plt.xlabel('Average')
        plt.ylabel('Number of students')
        plt.tight_layout()
        plt.show()

    def studentStatics(self,id,print_flag):  #studentStatics, will be used in both sub-classes Admin & Student
        status = self.searchRecord(id) #to check if the entered ID exists or not
        if status==0 : #id exists
            # local variables 
            total_taken_hours=0
            sum=0
            year_sem,avg_p_sem,hours_p_sem,remaining_courses=self.getStudentInfo(id)#lists
            
            for i in range(len(hours_p_sem)):
                total_taken_hours+=hours_p_sem[i]
            for i in range(len(avg_p_sem)):
                sum+=avg_p_sem[i]   
            over_all_average=sum/len(avg_p_sem)

            if print_flag == 1:
                print("Number of taken hours: "+str(total_taken_hours)+"\n")
                print("Average per semester: ")
                for i in range(len(avg_p_sem)):
                        print("*) "+str(year_sem[i])+":"+str(avg_p_sem[i]))
                print("\nOver all average: "+str(over_all_average)+"\n")
                print("Remaining Courses Are : ")
                for i in range(len(remaining_courses)):
                    print("*) "+str(remaining_courses[i]))
            return over_all_average,hours_p_sem, year_sem,total_taken_hours        
        else:
            print("record not found") 
            return 0         

        
        
    def globalStatics(self,print_flg): #globalStatics, will be used in both sub-classes Admin & Student
        allsemesters=[]#list that represents semesters from 2004 up to 2023
        hours_sum=[]#list of total taken hours for each semester
        count=[] #number of students who registerd in a spescific semester
        avg_hours=[]#list that represents average hours per semester
        sum_avg=0
        students_avg=[]#list that represents overall avg for each student.
        overall_students_avg=0
        ids=[]#list of students ids
        students_total_hours=[]#list that represents total taken hours for each student.

        f1= open ("year_semester.txt","r") #Open file of semesters
        data1 = f1.readlines()
        for line in data1:# read file line by line
            line = str(line).replace("\n", "") 
            allsemesters.append(line)
        for i in range(len(allsemesters)):
            hours_sum.append(0) #initilize lists
            count.append(0)
            avg_hours.append(0)    
        
        list_of_files = glob.glob('[0-9]*****[0-9].txt')           # create the list of files
        for file_name in list_of_files:#loop over all students records
            id=file_name.split(".")
            avg,hours_per_sem,year_sem,total_hours= self.studentStatics(id[0],0)
            ids.append(id[0])
            students_avg.append(avg)
            students_total_hours.append(total_hours)
            sum_avg+=avg
            for i in range(len(year_sem)):
                for j in range(len(allsemesters)):#search for semester match
                    if year_sem[i]== allsemesters[j] :
                        hours_sum[j]+=hours_per_sem[i]               
                        count[j]+=1 
        
        print(len(list_of_files))
        overall_students_avg=sum_avg/len(list_of_files) #calculate median average for all students
        if(print_flg == 1):
            print("Overall Students Average: %.2f" %overall_students_avg)
            print("=============================\n")
            print("Average hours per semester:")
            for i in range(len(allsemesters)):
                if count[i] != 0:
                    avg_hours[i]=hours_sum[i]/count[i]
                    print("*)"+str(allsemesters[i])+": %.2f" %avg_hours[i])
            self.plotHisto(students_avg,overall_students_avg)

        return students_avg,ids,students_total_hours   
   
    def searchBasedOnCriteria(self):    
        while 1:    
            print("Searching Criterias:")
            print(" (1) search for students above average")
            print(" (2) search for students below on average")
            print(" (3) search for students with GPA equals average")
            print(" (4) search for students who have taken certain hours (takenhours)")
            print(" (5) finish search")
            ans = input("choose one from the above criterias: ")
            
            if ans=='1' :
                average = float(input("enter the average: "))
                avg,id,_=self.globalStatics(0)
                print("Students who satisfy the choosen criteria are :\n")
                for i in range(len(avg)):
                    if avg[i]>average:
                        print("*) "+str(id[i])+" with average equals :%.2f"%avg[i])

            elif ans=='2' :
                average = float(input("enter the average: "))
                avg,id,_=self.globalStatics(0)
                print("Students who satisfy the choosen criteria are :\n")
                for i in range(len(avg)):
                    if avg[i]<average:
                        print("*) "+str(id[i])+" with average equals :%.2f"%avg[i])            
                
            elif ans=='3' : 
                average =float(input("enter the average: ")) 
                avg,id,_=self.globalStatics(0)
                print("Students who satisfy the choosen criteria are :\n")
                for i in range(len(avg)):
                    if avg[i]==average:
                        print("*) "+str(id[i]))
                
                
            elif ans=='4' : 
                taken_hours = int(input("enter the takenhours: "))
                _,id,students_taken_hours=self.globalStatics(0)
                print("Students who satisfy the choosen criteria are :\n")
                for i in range(len(students_taken_hours)):
                    if students_taken_hours[i]==taken_hours:
                        print("*) "+str(id[i]))
            elif ans=='5' : 
                break
            else:
                print("wrong choice")
    
     
    
class Admin(User): #Admin class, will represent functions and menu options available for an Admin user
    
    def __init__(self): #constructor
     print("Welcome to Admin Menu ^_^")
     
    def addRecord(self,id): #function to add a new Record(student) file
        file_name = id + ".txt"
        try:
            fi = open(file_name, "r")
        except IOError: #create a new student file if ID doesn't exist yet
            fi = open(file_name, "w")
            print("record created successfully")
        else: #to raise an error if the entered ID is not unique (this student already exists)
            raise Exception("ID is not unique") #print("Error: ID is not unique")
        fi.close()
     
    def addRecordInfo(self,id): #function to add informations to a student's record file
     status = self.searchRecord(id) #to check if the entered ID exists or not
     if status==0 : #id exists
        
        while 1:
            year = input("enter year (please stick to the correct year format: 2020-2021) : ")
            #raising errors if the entered year is missing or is in wrong format
            if year.isspace() or year=="" : #if year=space (or the user did not enter a value for the year)
                raise Exception("Missing information!! please fill the required field")
            if year[-1]==" " : #to remove the last character from the year if it was a space
                year = year[:-1]
            y = year.split("-")
            if len(y)!=2:
             raise Exception("Missing information!! please fill all required fields")
            if y[0]=="" or y[1]=="" :
                raise Exception("Missing information!! please fill all required fields")
            if (int(y[1])-int(y[0]))!=1 :
                raise Exception("Invalid year format!, the older year should be first (e.g: 2022-2021)")
            if len(y[0])!=4 or len(y[1])!=4 :
                raise Exception("Invalid year format!, each year should contain only 4 numbers (e.g: 2013)")
            
            semester = input("enter semester : ")
            #to raise an error if entered semester is missing or in wrong format
            if semester.isspace() or semester=="":
                raise Exception("Missing information!! please fill the required field")
            if semester[-1]==" " : #to remove the last character from the semester if it was a space
                semester = semester[:-1]
            if int(semester)!= 1 and int(semester )!=2 and int(semester )!=3:
                raise Exception("Invalid semester number")
            year_semester = year + "/" + semester
            
            #if user tries to enter a year with semester that already exists 
            file_name = id + ".txt"
            fi = open(file_name, "r")
            if year_semester in fi.read():
             print("the student already took this semester, try another year/semester")
             fi.close()
            else:
             fi.close()
             break          
        
        
        
        my_dict = { "course" : [] , "grade" : []  } #dictionary to hold values for the courses and their grades
        while 1 :
         course_grade = input("enter course and it's grade (separated by a space) or -1 to end : ")
         if course_grade.isspace() or course_grade=="":
            raise Exception("Missing information!! please fill all required fields")
         if course_grade == "-1" : 
            break
         if course_grade[-1]==" " : #to remove the last character from the course_grade if it was a space
            course_grade = course_grade[:-1] 
         x = course_grade.split(" ")
         if len(x)!=2:
            raise Exception("Missing information!! please fill all required fields")
         course_name = x[0]
         grade_value = x[1]
         #to raise an error if either entered course or entered grade is missing or in wrong format
         if x[0]=="" or x[1]=="" :
            raise Exception("Missing information!! please fill all required fields")
         if course_name.isalnum()!=1 or course_name.isdigit()==1:
            raise Exception("Invalid course name, course name should contain both characters and numbers")
         if grade_value.isdigit()!= 1 :
            raise Exception("Invalid course grade!! grade must only be number") 
         if grade_value.isdigit() == 1 and (int(grade_value) > 100 or int(grade_value) < 0):
            raise Exception("Invalid course grade!! grade must only be number with a range (0 to 99)") 
          
         #add entered course & grade to the dictionary
         my_dict["course"].append(course_name)
         my_dict["grade"].append(grade_value) 
        
        object = StudentData(id,year_semester,my_dict) #make a student object of these values
        object.printFormatedfile() #append entered informations to the student record file
        print("the informations are added successfully to the student record")

     else : #id doesn't exist
        print("record not found")
        ans = input("do you want to create this record? (y/n)") #to give the user a chance to create the record file for the entered id
        if ans=='y' :
          file_name = id + ".txt"
          fi = open(file_name, "w")
          print("record created successfully")
          fi.close()
          self.addRecordInfo(id) #return to the function to add the informations
 
    def updateRecordInfo(self,id): #function to update informations for a student's record file
     status=self.searchRecord(id) #to make sure that the record exists
     if status == 0 : #record exists
        
      while 1 :
        course=input("enter the name of the course: ")
        new_grade=input("enter the new grade for this course : ")
    
        #to raise an error if either entered course or entered grade is missing or in wrong format
        if new_grade.isspace() or course.isspace():
            raise Exception("Missing information!! please fill all required fields")
        #to remove the last character from the inputs if it was a space
        if new_grade[-1]==" " :
            new_grade = new_grade[:-1]
        if new_grade.isdigit()!= 1 :
            raise Exception("Invalid course grade!! grade must only be number") 
        if new_grade.isdigit() == 1 and (int(new_grade) > 100 or int(new_grade) < 0):
            raise Exception("Invalid course grade!! grade must only be number with a range (0 to 99)")  
        #to remove the last character from the inputs if it was a space
        if course[-1]==" " :
            course = course[:-1]
        
        #search for the entered course in the file
        file_name = id + ".txt"
        with open(file_name) as f:
         if course in f.read(): #course found 
            with open(file_name) as f2: 
             filedata = f2.read()
             words=filedata.split()
             for word in words:
                if word == course:
                 pos = words.index(word)+1  
                 old_grade=str(words[pos])
             filedata = filedata.replace(old_grade,new_grade+',')
             f2.close()
            f.close()
          
            #to update the file with the new value
            with open(file_name, 'w') as ff:
             ff.write(filedata)
            ff.close()
            print("done, you can check the file now")
            break
        
         else : #if the entered course doesn't exist
            print("The entered course doesn't exist !?")
            ans=input("do you want to try again (y/n)")
            if ans=='n' :
             break
  
     else : #record does not exist
        print("student record does not exist (this id does not exist)")
        print("if you want to create this record you can go to choice 1 from the main menu")
     
    def menu(self):  #override menu method in superclass Use
     while 1:
        print("*************************************************************************")
        print ("available opeartions:")
        print (" (1) add a new record file")
        print (" (2) add a new semester with student course and grade")
        print (" (3) update")
        print (" (4) student statics")
        print (" (5) global statics")
        print (" (6) search")
        print (" (7) exit") 
        op = int (input ("select a choice from the above operations : "))
        print("*************************************************************************")    
        if op == 1: 
            id=self.getAndCheckId()
            self.addRecord(id) #call addRecord function
        elif op == 2:
            id=self.getAndCheckId()
            self.addRecordInfo(id)
        elif op == 3:
            id=self.getAndCheckId()
            self.updateRecordInfo(id)
        elif op == 4:
            id=self.getAndCheckId()
            self.studentStatics(id,1)
        elif op == 5:
            self.globalStatics(1)
        elif op == 6:
            self.searchBasedOnCriteria()
        elif op == 7:
            print("BYE!")
            break
        else:
            print ("invalid operation") 
 
         
class Student(User): #Student class, will represent functions and menu options available for a student user
    
    def __init__(self): #constructor
        print("Welcome to Student Menu ^_^") 
    
    def menu(self): #override menu method in superclass User
     while 1:
        print("*************************************************************************")
        print ("available opeartions:")
        print (" (1) student statics")
        print (" (2) global statics")
        print (" (3) exit")
        op = int (input ("select a choice from the above operations : "))
        print("*************************************************************************")  
        if op == 1:
           id = self.getAndCheckId()  #getAndCheckId() method is defiend in the superclass
           self.studentStatics(id,1)
        elif op == 2:
           self.globalStatics(1)
        elif op == 3:
            print("BYE!")
            break
        else:
            print ("invalid operation") 
 
 
class StudentData(): #StudentData class, will represent the needed data for each student record file

    #constructor and Attributes
    def __init__(self, id, year_semester, course_grade):
     self.__id = id #private Attributes
     self.__year_semester = year_semester
     self.__course_grade = course_grade
      
    #Getters
    def getID(self):
     return self.__id
    def getYearSemester(self):
     return self.__year_semester
    def getCourseGrade(self):
     return self.__course_grade

    #Setters
    def setID(self, id):
     self.__id = id
    def setYearSemester(self, year_semester):
     self.__year_semester = year_semester
    def setCourseGrade(self, course_grade):
     self.__course_grade = course_grade

    #function to print the attributes of a student object
    def printFormatedInfo(self):
     return (self.__year_semester + " ; " + self.__course_grade ) 

    #function to print the attributes of a student object to a file
    def printFormatedfile(self):
        courses_number = len(self.__course_grade["course"]) #number of courses the student took that year/semester
        file_name = self.__id + ".txt"
        fo = open(file_name, "a") #to add a new record to the file
        fo.write(self.__year_semester + " ; ") 
        for i in range(courses_number):
            if i!= (0) :  #to make sure data is entered to the file in the right structure
                fo.write(", " + self.__course_grade["course"][i] + " " + self.__course_grade["grade"][i])
            else :
                fo.write(self.__course_grade["course"][i] + " " + self.__course_grade["grade"][i])     
        fo.write("\n")
        fo.close()
        
