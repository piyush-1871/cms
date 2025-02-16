import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="ems")


#To Retrieve data from database
c = mydb.cursor()
c.execute("select * from employees")
for r in c:
    print(r)



"""    
# Input data
emp_id = int(input("Enter the employee id: "))
first_name = input("Enter the first name of user: ")
last_name = input("Enter the last name of user: ")
age = int(input("Enter the age: "))
gender = input("Enter the gender: ")
department = input("Enter the department: ")
salary = input("Enter the salary: ")
contact_no = input("Enter the contact no : ")
address = input("Enter the address of employee: ")


# Create a cursor object
c = mydb.cursor()

# Execute the SQL command with placeholders
c.execute(
    "INSERT INTO employees (emp_id, first_name, last_name, age, gender, department, salary, contact_no, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
    (emp_id, first_name, last_name, age, gender, department, salary, contact_no, address)
)

# Commit the transaction
mydb.commit()

print("Employee added successfully!!")

"""
    


    
