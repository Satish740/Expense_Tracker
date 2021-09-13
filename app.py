import flask
import pymysql
from flask import render_template,request,redirect

app=flask.Flask(__name__)

app.config["DEBUG"]=True


def add_user_info_to_database(name,mail,password):
    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor()
    insert_query= "INSERT INTO User1_info (Name,email_id,Password) VALUES (%s,%s,%s);"
    cur.execute(insert_query,(name,mail,password))
    con.commit()
    cur.close()        
    con.close()
  
    
def verify(mail,password):
    global gmail
    gmail=mail
    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor()
    insert_query= "Select Password FROM User1_info where email_id= %s;"
    data=cur.execute(insert_query,(mail,))
    if data==0:
       cur.close()
       con.close()
       return 0;
    else:
       data1=cur.fetchone()
       cur.close()
       con.close()
       if data1[0]==password:
          return 1;
       else:
          return 0;
          
def verify_sign_up(mail,password):

    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor()
    insert_query= "Select Password FROM User1_info where email_id= %s;"
    data=cur.execute(insert_query,(mail,))
    if data==0:
       cur.close()
       con.close()
       return 1;
    
def Enter_data(date,rent,transport,food,medical,personal):
    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor()
    insert_query= "INSERT INTO user_expense (Mail_id ,Date_of_Expense,Housing_Utilities,Transportation ,Food,Medical,Personal) values (%s,%s,%s,%s,%s,%s,%s)"
    cur.execute(insert_query,(gmail,date,rent,transport,food,medical,personal))
    con.commit()
    cur.close()
    con.close()
      
def Fetch_db():
    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor()
    insert_query= "Select Date_of_Expense,Housing_Utilities,Transportation ,Food,Medical,Personal,sid FROM user_expense where Mail_id = %s;"
    data1=cur.execute(insert_query,(gmail,))
    data=cur.fetchall()
    cur.close()
    con.close()
    return data1,data

def each_sum():
    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor()
    insert_query1= "Select SUM(Personal)FROM user_expense where Mail_id = %s;"
    insert_query2= "Select SUM(Housing_Utilities) FROM user_expense where Mail_id = %s;"
    insert_query3= "Select SUM(Transportation) FROM user_expense where Mail_id = %s;"
    insert_query4= "Select SUM(Food) FROM user_expense where Mail_id = %s;"
    insert_query5= "Select SUM(Medical) FROM user_expense where Mail_id = %s;"
    cur.execute(insert_query1,gmail)
    data_personal=cur.fetchall()
    cur.execute(insert_query2,gmail)
    data_rent=cur.fetchall()
    cur.execute(insert_query3,gmail)
    data_transport=cur.fetchall()
    cur.execute(insert_query4,gmail)    
    data_food=cur.fetchall()
    cur.execute(insert_query5,gmail)
    data_medical=cur.fetchall()    
    cur.close()
    con.close()
    return data_rent,data_transport,data_food,data_medical,data_personal
    
    
def delete_data_from_db(id):
    con = pymysql.connect(host="localhost", user="root", password="", database="expense_update")
    cur = con.cursor() 
    delete_query="delete from user_expense where sid=%s"
    cur.execute(delete_query,(id,))
    con.commit()
    cur.close()
    con.close()
    

    
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        form_data=request.form
        data= verify(form_data['Email'],form_data['Pass'])
        if data==1:
            return render_template("enter_tracker.html")
        else:
            return render_template("expense.html")
    else:
        return render_template("expense.html") 

        
@app.route("/sign_up/", methods=['GET','POST'])
def add_user():
    if request.method == "POST":
        form_data=request.form
        data= verify_sign_up(form_data['mail'],form_data['pw'])
        if(data!=1):
            return render_template("sign_up.html")
        else:
            add_user_info_to_database(form_data['sname'],form_data['mail'],form_data['pw'])
            return redirect("/")
    else:
        return render_template("sign_up.html")
        
@app.route("/enter_expenses/",methods=['GET','POST'])
def user_data_entry():
    if request.method == "POST":
        form_data=request.form
        Enter_data(form_data['date_expense'],form_data['Housing'],form_data['Transporting'],form_data['Food'],form_data['Medical'],form_data['Personal_spending'])
        return render_template("enter_expense.html")
    else:
        return render_template("enter_expense.html")        
        
@app.route("/view_expenses/",methods=['GET','POST'])

def user_view():
    count,data=Fetch_db()
    data=list(data)
    overall_total=0
    for i in range(0,count):
        total=0
        data[i]=list(data[i])
        total=int(data[i][1])+int(data[i][2])+int(data[i][3])+int(data[i][4])+int(data[i][5])
        data[i].insert(6,total)
        overall_total= overall_total + total 
    data1,data2,data3,data4,data5=each_sum()
    sum_of_data=[]
    sum_of_data.append(data1[0][0])
    sum_of_data.append(data2[0][0])
    sum_of_data.append(data3[0][0])
    sum_of_data.append(data4[0][0])
    sum_of_data.append(data5[0][0])
    return render_template("Expense_view.html",task_data=data,task_data1=overall_total,task_data2=sum_of_data) 

@app.route("/update_expenses/")
def user_updated_view():
    count,data=Fetch_db()
    data=list(data)
    for i in range(0,count):
        data[i]=list(data[i])     
    return render_template("Update_expense.html",task_data=data)
    
@app.route("/delete",methods=['GET'])
def user_delete():
    id = request.args.get("id")
    delete_data_from_db(id)
    return redirect("/update_expenses/")
        
app.run()
 
 
  # create table User1_info(Name VARCHAR(60) NOT NULL,email_id VARCHAR(60),Password VARCHAR(100));
  # create table user_expense (Mail_id varchar(30),Date_of_Expense DATE,Housing_Utilities VARCHAR(30),Transportation VARCHAR(30),Food VARCHAR(30),Medical VARCHAR(30),Personal VARCHAR(30),sid INT PRIMARY KEY AUTO_INCREMENT);