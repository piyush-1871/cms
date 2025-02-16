#import the libraries
import streamlit as st
import pandas as pd
import mysql.connector
import datetime
import os
from PIL import Image
import plotly.express as px
import pyotp
import time

st.set_page_config(page_title="CMS")

st.title("CUSTOMER MANAGEMENT SYSTEM")
choice = st.sidebar.selectbox("My Menu", ("Home", "User", "Admin"))
if(choice == "Home"):
    st.image("https://chisellabs.com/glossary/wp-content/uploads/2023/05/f17fea9f-e83a-4f9b-924c-508d29a53f24.png")

#----------------------------Admin Section----------------------#        
elif(choice == 'Admin'):
    if 'alogin' not in st.session_state:
        st.session_state['alogin'] = False
    admin_id = st.text_input("admin id: ")
    admin_pass = st.text_input("admin password: ", type = "password")  
    btn = st.button("Login")  
    if btn:
        mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
        c = mydb.cursor()
        c.execute("select * from admin")
        for r in c:
            if(r[0] == admin_id and r[1] == admin_pass):
                st.session_state['alogin'] = True
                break
    if(btn and not st.session_state['alogin']):
        st.write("Incorrect ID or Password!")
    
    if(st.session_state['alogin']):
        st.write("Login Successfull!")
        
        choice2 = st.selectbox("Features", ("None", "View All Customers", "Add New Customer", "Remove Customer", "Add New Admin", "Record Transaction", "View All Transaction", "View All Admin","Analytics Dashboard", "Pending Service Requests", "View All Service Requests", "Logout"))
        #-------------View All Customers---------------
        if(choice2 == "View All Customers"):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
            df = pd.read_sql("select cust_id, first_name, last_name, age, gender, phone, address, email_id from customers", mydb)
            df_no_index = df.to_records(index=False)
            #Display dataframe
            st.dataframe(df_no_index)
            
            if st.button("Export Data to CSV"):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="customers.csv",
                    mime="text/csv",
                )
        #-------------Add New Customers----------------
        elif(choice2 == "Add New Customer"):
            #Input Fields
            cust_id = st.number_input("Enter the Customer ID: ", min_value = 1, step = 1, format = '%d')
            first_name = st.text_input("Enter the first name: ")
            last_name = st.text_input("Enter the last name: ")    
            age = st.number_input("Enter the Age: ", min_value = 18, max_value = 100, step = 1, format = '%d')     
            gender = st.selectbox("Enter the gender (M/F): ", ['M', 'F'])
            phone = st.text_input("Enter the phone no. : ")
            address = st.text_input("Enter the address : ")
            email_id = st.text_input("Enter the email : ")
            user_pass = st.text_input("Enter the password for Customer: ")
            btn3 = st.button("Submit")
            if(btn3):
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                c = mydb.cursor()
                #Check if customer id already exists
                c.execute("SELECT COUNT(*) FROM customers WHERE cust_id = %s", (cust_id,))
                if(c.fetchone()[0] > 0):
                    st.error("Customer ID already exists. Please choose different Customer ID.")
                else:
                    #Insert the new user into user table first
                    c.execute("INSERT INTO user (email_id, user_pass) VALUES (%s, %s)", (email_id, user_pass))
                    
                    #Insert into customers table
                    c.execute("INSERT INTO customers (cust_id, first_name, last_name, age, gender, phone, address, email_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (cust_id, first_name, last_name, age, gender, phone, address, email_id))
                    
                    
                    
                    mydb.commit()
                   
                    st.header("Customer Added Successfully!")
        #-------------Remove Customers-----------------
        elif(choice2 == "Remove Customer"):
            cust_id = st.number_input("Enter the Customer ID: ", min_value = 1, step=1, format="%d")
            btn4 = st.button("Delete")
            
            if(btn4):
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                c = mydb.cursor()
                
                c.execute("SELECT email_id FROM customers WHERE cust_id = %s", (cust_id,))
                result = c.fetchone()
                
                # Debugging: Check the result returned by the query
                print(f"Query result: {result}")
        
                if result:  
                    email_id = result[0]  
                                   
                    #Delete the cutomer record
                    c.execute("DELETE FROM customers WHERE cust_id = %s", (cust_id,))
                    #Delete the corresponding email
                    c.execute("DELETE FROM user WHERE email_id = %s", (email_id,)) 
                    #Delete the corresponding transactions
                    c.execute("DELETE FROM transactions WHERE cust_id = %s", (cust_id,))
                    
                    
                    mydb.commit()
                    
                    st.header("Customer record Deleted!")
                else:
                    st.error("Customer ID not found.")              
        #-------------Add New Admin--------------------       
        elif(choice2 == "Add New Admin"):
            admin_id = st.text_input("Enter admin email id: ")
            admin_pass = st.text_input("Enter the password: ")
            btn5 = st.button("Add")
            
            if(btn5):
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                
                c = mydb.cursor()
                c.execute("insert into admin values(%s,%s)", (admin_id, admin_pass))
                mydb.commit()
                st.header("Admin Added Successfully!")
        #-------------Record Transactions--------------
        elif(choice2 == "Record Transaction"):
            trans_id = str(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
            cust_id = st.text_input("Customr ID: ")
            trans_date = st.date_input("Trans Date: ")
            trans_amount = st.text_input("Enter the amount: ")
            trans_type = st.selectbox("Transaction Type", ("UPI", "Internet Banking", "Debit Card", "Credit Card"))
            
            btn6 = st.button("Record")
            
            if btn6:
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                
                c = mydb.cursor()
                c.execute("INSERT INTO transactions values(%s,%s,%s,%s,%s)", (trans_id, cust_id, trans_date, trans_amount, trans_type))
                
                mydb.commit()
                st.header("Transaction Recorded Successfully!")
        #-------------View All Transactions------------
        elif(choice2 == "View All Transaction"):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
            df = pd.read_sql("select * from transactions", mydb)
            df_no_index = df.to_records(index=False)
            
            st.dataframe(df_no_index)
            if st.button("Export Data to CSV"):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="transactions.csv",
                    mime="text/csv",
                )
        #-------------View All Admin-------------------
        elif(choice2 == "View All Admin"):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
            df = pd.read_sql("select * from admin", mydb)
            df_no_index = df.to_records(index=False)
            
            st.dataframe(df_no_index)
            if st.button("Export Data to CSV"):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="admins.csv",
                    mime="text/csv",
                ) 
        #-------------Analytics Dashboard--------------        
        elif(choice2 == "Analytics Dashboard"):
            st.header("Analytics Dashboard")
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database='cms')
            
            st.subheader("Transaction Trends")
            # Query to get transaction counts per day
            query_trans = """
                SELECT DATE(trans_date) AS trans_date, COUNT(*) AS transaction_count 
                FROM transactions 
                GROUP BY DATE(trans_date) 
                ORDER BY DATE(trans_date)
            """
            df_trans = pd.read_sql(query_trans, mydb)
            if not df_trans.empty:
                fig_trans = px.line(df_trans, x="trans_date", y="transaction_count",
                                    title="Transactions Over Time",
                                    labels={"trans_date": "Date", "transaction_count": "Number of Transactions"})
                st.plotly_chart(fig_trans, use_container_width=True)
            else:
                st.info("No transaction data available.")
                
           
            st.subheader("Revenue Analytics")
            # Query to calculate total revenue per day (assumes trans_amount is numeric)
            query_rev = """
                SELECT DATE(trans_date) AS trans_date, SUM(trans_amount) AS revenue 
                FROM transactions 
                GROUP BY DATE(trans_date) 
                ORDER BY DATE(trans_date)
            """
            df_rev = pd.read_sql(query_rev, mydb)
            if not df_rev.empty:
                fig_rev = px.bar(df_rev, x="trans_date", y="revenue",
                                 title="Revenue Over Time",
                                 labels={"trans_date": "Date", "revenue": "Total Revenue"})
                st.plotly_chart(fig_rev, use_container_width=True)
            else:
                st.info("No revenue data available.")
        #-------------Pending Service Requests---------
        elif(choice2 == "Pending Service Requests"):
            st.subheader("Pending Service Requests")
            # Query to get pending service requests
            # Connect to the database
            mydb = mysql.connector.connect(
                host="localhost", user="root", password="Piyush@2002", database="cms"
            )
            # Fetch pending service requests
            df_requests = pd.read_sql("SELECT * FROM service_requests WHERE status='Pending'", mydb)

            if df_requests.empty:
                st.info("No pending service requests.")
            else:
                st.dataframe(df_requests)
                # Iterate over each pending request
                for index, row in df_requests.iterrows():
                    st.write(f"**Request ID:** {row['request_id']}")
                    st.write(f"**Customer ID:** {row['cust_id']}")
                    st.write(f"**Request Type:** {row['request_type']}")
                    st.write(f"**Description:** {row['description']}")
                    st.write(f"**Requested Date:** {row['request_date']}")
                    #Optionally show any existing
                    # Create two columns for Approve and Reject buttons
                    col1, col2 = st.columns(2)

                    #Approve section: allow admin to optionally add a comment
                    approve_comment = col1.text_input(
                        f"Add comment (optional) for Approving Request {row['request_id']}:",
                        key=f"approve_comment_{row['request_id']}"
                    )
                    # Approve button
                    if col1.button(f"Approve {row['request_id']}", key=f"approve_{row['request_id']}"):
                        c = mydb.cursor()
                        c.execute(
                            "UPDATE service_requests SET status='Approved', admin_comments=%s WHERE request_id=%s",
                            (approve_comment, row['request_id'],)
                        )
                        mydb.commit()
                        st.success(f"Request {row['request_id']} approved.")

                    # Reject section: allow admin to optionally add a comment
                    reject_comment = col2.text_input(
                        f"Add comment (optional) for Rejecting Request {row['request_id']}:",
                        key=f"reject_comment_{row['request_id']}"
                    )
                    # Reject button
                    if col2.button(f"Reject {row['request_id']}", key=f"reject_{row['request_id']}"):
                        c = mydb.cursor()
                        c.execute(
                            "UPDATE service_requests SET status='Rejected', admin_comments=%s WHERE request_id=%s",
                            (reject_comment, row['request_id'])
                        )
                        mydb.commit()
                        st.error(f"Request {row['request_id']} rejected.")
        #-------------View All Service Requests--------
        elif(choice2 == "View All Service Requests"):
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
            df = pd.read_sql("select * from service_requests", mydb)
            df_no_index = df.to_records(index=False)
            #Display dataframe
            st.dataframe(df_no_index)
            
            if st.button("Export Data to CSV"):
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="service_requests.csv",
                    mime="text/csv",
                ) 
        #-------------Logout---------------------------        
        elif(choice2 == "Logout"):
            st.session_state['alogin'] = False
            st.session_state.pop("admin_email", None)  # Remove stored admin email if needed
            st.success("Logged out successfully!")
            time.sleep(2)  # Wait for 2 seconds to show the message
            st.rerun()  # Refresh UI after delay                      

#-------------------User Section----------------------------------------#
elif("User"):
    action = st.radio("Select an Action", ["Login", "Register"])
    
    if action == "Login":
        if 'login' not in st.session_state:
            st.session_state['login'] = False
        if 'forgot_password' not in st.session_state:
            st.session_state['forgot_password'] = False
        if 'otp_verified' not in st.session_state:
            st.session_state['otp_verified'] = False 
            
                  
        email_id = st.text_input("Enter user Email ID: ")
        user_pass = st.text_input("Enter user Password: ", type="password")
        
        # Display buttons side-by-side
        col1, col2 = st.columns(2)
        login_btn = col1.button("Login")
        forgot_btn = col2.button("Forgot Password?")
        
        
        if login_btn:
            mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
            c = mydb.cursor()
            c.execute("SELECT * FROM user")
            for r in c:
                if(r[0] == email_id and r[1] == user_pass):
                    st.session_state['login'] = True
                    st.session_state['email_id'] = email_id
                    break
            if(not st.session_state['login']):
                st.write("Incorrect ID or password!")
            else:
                st.success("Login Successfull!")
                
        #----------------Forgot Password--------------------
        if forgot_btn or st.session_state['forgot_password']:
            st.session_state['forgot_password'] = True  # Ensure the forgot flow is active
            st.subheader("Password Reset") 
            
            # Step 1: Ask for registered email
            reset_email = st.text_input("Enter your registered email for password reset:", key="reset_email")
            send_link = st.button("Send Reset Link")
            
            if send_link:
                # Check if the email exists in the user table
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                c = mydb.cursor()
                c.execute("SELECT * FROM user WHERE email_id = %s", (reset_email,))
                user_exists = c.fetchone()
                if not user_exists:
                    st.error("Email not registered!")
                else:
                    # Generate an OTP using PyOTP (valid for 5 minutes)
                    secret = pyotp.random_base32()
                    totp = pyotp.TOTP(secret, interval=300)  # 300 seconds = 5 minutes
                    otp_code = totp.now()
                    
                    # Store secret and expiration time in session state
                    st.session_state['reset_secret'] = secret
                    st.session_state['reset_expires'] = datetime.datetime.now() + datetime.timedelta(minutes=5)
                    
                    # In production, send an email with a reset link or OTP.
                    # For demo, we display the OTP.
                    st.success(f"A password reset link has been sent to your email. (Demo OTP: {otp_code})")
            
            # Step 2: OTP Verification
            if 'reset_secret' in st.session_state and st.session_state.get('reset_email'):
                entered_otp = st.text_input("Enter the OTP received in your email:", key="entered_otp")
                verify_otp = st.button("Verify OTP")
                if verify_otp:
                    # Check if the reset link has expired
                    if datetime.datetime.now() > st.session_state['reset_expires']:
                        st.error("Reset link has expired. Please try again.")
                        st.session_state['forgot_password'] = False
                        st.session_state.pop('reset_secret', None)
                        st.session_state.pop('reset_email', None)
                        st.session_state.pop('reset_expires', None)
                    else:
                        totp = pyotp.TOTP(st.session_state['reset_secret'], interval=300)
                        if totp.verify(entered_otp):
                            st.success("OTP Verified! You can now reset your password.")
                            st.session_state['otp_verified'] = True
                        else:
                            st.error("Incorrect OTP. Please try again.")
            
            # Step 3: Reset Password Form (only if OTP is verified)
            if st.session_state.get('otp_verified'):
                new_password = st.text_input("Enter new password:", type="password", key="new_pass")
                confirm_password = st.text_input("Confirm new password:", type="password", key="confirm_pass")
                reset_pass_btn = st.button("Reset Password")
                if reset_pass_btn:
                    if new_password != confirm_password:
                        st.error("Passwords do not match!")
                    else:
                        mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                        c = mydb.cursor()
                        c.execute("UPDATE user SET user_pass = %s WHERE email_id = %s", (new_password, st.session_state['reset_email']))
                        mydb.commit()
                        st.success("Password reset successful! You can now log in with your new password.")
                        # Clear the reset-related session state variables
                        st.session_state['forgot_password'] = False
                        st.session_state['otp_verified'] = False
                        st.session_state.pop('reset_secret', None)
                        st.session_state.pop('reset_email', None)
                        st.session_state.pop('reset_expires', None)
                        
                        time.sleep(2)  # Wait for 2 seconds to show the message
                        st.rerun()  # Refresh UI after delay 
                   
                
        if(st.session_state['login']):
            st.write("Login Successfull!")   
            choice3 = st.selectbox("Features", ("None", "View All Transactions", "View Profile", "Edit Profile", "Service Request", "Status of Service Requestion", "Logout"))
            #----------View All Transactions---------------
            if(choice3 == "View All Transactions"):
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                
                # Date range selection
                start_date = st.date_input("Start Date", value=datetime.date.today() - datetime.timedelta(days=30))  # Default: last 30 days
                end_date = st.date_input("End Date", value=datetime.date.today())
                # Transaction Type Filter
                trans_type_options = ["All", "UPI", "Internet Banking", "Debit Card", "Credit Card"]
                selected_trans_type = st.selectbox("Transaction Type", trans_type_options)
                if start_date > end_date:
                    st.error("Start date cannot be after end date. Please select a valid date range.")
                else:
                    query = """
                        SELECT 
                            t.trans_id AS Transaction_ID,
                            t.trans_date AS Transaction_Date,
                            t.trans_amount AS Amount,
                            t.trans_type AS Payment_Option
                        FROM transactions t
                        INNER JOIN customers c ON t.cust_id = c.cust_id
                        INNER JOIN user u ON u.email_id = c.email_id
                        WHERE u.email_id = %s AND t.trans_date BETWEEN %s AND %s
                    """
                    params = [email_id, start_date, end_date]

                    if selected_trans_type != "All":
                        query += " AND t.trans_type = %s"
                        params.append(selected_trans_type)
                        
                    df = pd.read_sql(query, mydb, params=tuple(params))

                    if df.empty:
                        st.warning("No transactions found for the selected date range.")
                    else:
                        st.dataframe(df)
                    if st.button("Export Data to CSV"):
                        csv_data = df.to_csv(index=False)
                        st.download_button(
                            label="Download CSV",
                            data=csv_data,
                            file_name="my_transaction.csv",
                            mime="text/csv",
                        )    
            #----------View Profile------------------------
            elif(choice3 == "View Profile"):
                # Connect to the database
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                c = mydb.cursor()

                # Execute query to fetch customer details based on email_id
                c.execute("SELECT * FROM customers WHERE email_id = %s", (email_id,))
                r = c.fetchone()

                if r:
                    st.header("Customer Profile")  # Add a header
                    st.subheader("Personal Information")  # Section title for personal info

                    
                    # Display customer information with better styling
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Customer ID:** {r[0]}")
                        st.write(f"**First Name:** {r[1]}")
                        st.write(f"**Last Name:** {r[2]}")
                        st.write(f"**Age:** {r[3]}")
                        st.write(f"**Gender:** {r[4]}")
                        st.write(f"**Phone Number:** {r[5]}")
                        st.write(f"**Address:** {r[6]}")
                        st.write(f"**Email ID:** {r[7]}")
                    with col2:
                       if r[8]:  # Check if profile picture exists
                           
                           profile_pic_path = r[8]
                           
                           if os.path.exists(profile_pic_path):
                                profile_pic = Image.open(profile_pic_path)
                                profile_pic.thumbnail((15000, 15000))
                                st.image(profile_pic, caption=f"{r[1]}", use_column_width=True)
                       else:
                           st.write("No profile picture uploaded.") 
                    
                else:
                    st.error("No customer found with the given email ID.")  # Display error if no record is found
            #----------Edit Profile------------------------        
            elif(choice3 == "Edit Profile"):  
                # Ensure 'profile_pics' directory exists
                if not os.path.exists("profile_pics"):
                    os.makedirs("profile_pics")

                # Connect to the database   
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                c = mydb.cursor()

                # Fetch user details
                c.execute("SELECT first_name, last_name, age, phone, address, profile_pic FROM customers WHERE email_id = %s", (email_id,))
                user_data = c.fetchone()

                if user_data:
                    first_name, last_name, age, phone, address, profile_pic = user_data

                    # Pre-fill form fields with existing data
                    first_name = st.text_input("First Name", first_name)
                    last_name = st.text_input("Last Name", last_name)
                    age = st.number_input("Age", min_value=18, max_value=100, value=age)
                    phone = st.text_input("Phone Number", phone)
                    address = st.text_input("Address", address)
                    new_password = st.text_input("New Password (Leave blank if unchanged)", type="password")

                    # Profile Picture Upload
                    uploaded_file = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])


                    # Update button
                    if st.button("Update Profile"):
                        if uploaded_file:
                            # Save uploaded file
                            file_extension = os.path.splitext(uploaded_file.name)[1]
                            file_name = f"{email_id}{file_extension}"
                            file_path = os.path.join("profile_pics", file_name)
                            with open(file_path, "wb") as f:
                                f.write(uploaded_file.getbuffer())

                            # Update profile picture path in DB
                            c.execute("UPDATE customers SET profile_pic = %s WHERE email_id = %s", (file_path, email_id))

                        if new_password:
                            c.execute("UPDATE user SET user_pass = %s WHERE email_id = %s", (new_password, email_id))

                        # Update other fields
                        c.execute("UPDATE customers SET first_name = %s, last_name = %s, age = %s, phone = %s, address = %s WHERE email_id = %s",
                                (first_name, last_name, age, phone, address, email_id))

                        mydb.commit()
                        st.success("Profile Updated Successfully!")
            #----------Service Request---------------------
            elif(choice3 == "Service Request"):
                st.subheader("Submit a Service Request")  
                if "email_id" not in st.session_state:
                    st.error("Please login first to submit request!")
                request_type = st.selectbox("Request Type", ["Refund", "Maintenance", "Additional Service", "Other"])
                description = st.text_area("Describe your request:")
                request_date = st.date_input("Preferred Date", datetime.date.today()) 
                if st.button("Submit Request"):
                    mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                    c = mydb.cursor()
                    # Fetch cust_id using the email stored in session state (assumes it's stored as 'email_id')
                    c.execute("SELECT cust_id FROM customers WHERE email_id = %s", (st.session_state["email_id"],))
                    result = c.fetchone()
                    if result is None:
                        st.error("Customer not found. Please ensure you are logged in correctly.")
                    else:
                        cust_id = result[0]
                        query = """
                            INSERT INTO service_requests (cust_id, request_type, description, request_date)
                            VALUES (%s, %s, %s, %s)
                        """
                        c.execute(query, (cust_id, request_type, description, request_date))
                        mydb.commit()
                        st.success("Your service request has been submitted and is pending approval.")
            #----------Status of Service Requestion--------
            elif(choice3 == "Status of Service Requestion"):
                st.subheader("Status of Service Requestion")

                # Check if the user is logged in by verifying that 'email_id' is in session state
                if "email_id" not in st.session_state:
                    st.error("Please log in to view your service request status.")
                else:
                    # Fetch cust_id using the logged-in email
                    mydb = mysql.connector.connect(
                        host="localhost", user="root", password="Piyush@2002", database="cms"
                    )
                    c = mydb.cursor()
                    c.execute("SELECT cust_id FROM customers WHERE email_id = %s", (st.session_state["email_id"],))
                    result = c.fetchone()
                    if result:
                        cust_id = result[0]
                    else:
                        st.error("Customer not found. Please ensure you are logged in correctly.")
                        

                    st.write("Your Customer ID is:", cust_id)

                    # Now query the service_requests table for this customer
                    query = """
                        SELECT cust_id, request_id, request_type, status, admin_comments, request_date 
                        FROM service_requests 
                        WHERE cust_id = %s 
                        ORDER BY request_date DESC
                    """
                    df_status = pd.read_sql(query, mydb, params=(cust_id,))

                    st.write("Number of Service Requests found:", df_status.shape[0])

                    if df_status.empty:
                        st.info("No service requests found.")
                    else:
                        st.dataframe(df_status) 
            #-----------------Logout-----------------------
            elif(choice3 == "Logout"):
                st.session_state['login'] = False
                st.session_state.pop("email_id", None)  # Remove stored admin email if needed
                st.success("Logged out successfully!")
                time.sleep(2)  # Wait for 2 seconds to show the message
                st.rerun()  # Refresh UI after delay 
    
    
    #-----------Register-------------------------------------#    
    elif action == "Register":
        st.subheader("User Registration")

        first_name = st.text_input("Enter First Name: ")
        last_name = st.text_input("Enter Last Name: ")    
        age = st.number_input("Enter Age: ", min_value=18, max_value=100, step=1, format='%d')     
        gender = st.selectbox("Enter Gender (M/F): ", ['M', 'F'])
        phone = st.text_input("Enter Phone No.: ")
        address = st.text_area("Enter Address: ")
        email_id = st.text_input("Enter Email: ")
        user_pass = st.text_input("Set Password: ", type="password")
        register_btn = st.button("Register")

        if register_btn:
            if first_name and last_name and age and gender and phone and address and email_id and user_pass:
                mydb = mysql.connector.connect(host="localhost", user="root", password="Piyush@2002", database="cms")
                c = mydb.cursor()

                # Check if email already exists
                c.execute("SELECT * FROM user WHERE email_id=%s", (email_id,))
                if c.fetchone():
                    st.error("User already exists with this email!")
                else:
                    # Auto-generate Customer ID (Increment from last ID)
                    c.execute("SELECT MAX(cust_id) FROM customers")
                    last_id = c.fetchone()[0]
                    cust_id = last_id + 1 if last_id else 1

                    # Insert into user table
                    c.execute("INSERT INTO user (email_id, user_pass) VALUES (%s, %s)", (email_id, user_pass))

                    # Insert into customers table
                    c.execute("INSERT INTO customers (cust_id, first_name, last_name, age, gender, phone, address, email_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                              (cust_id, first_name, last_name, age, gender, phone, address, email_id))

                    mydb.commit()
                    st.success(f"Registration Successful! Your Customer ID is {cust_id}")
                    time.sleep(2)  # Wait for 3 seconds to show the message
                    st.rerun()  # Refresh UI after delay 
            else:
                st.error("Please fill all fields!")

                 
    