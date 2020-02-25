from flask import Flask, render_template, request
import psycopg2
from psycopg2.extras import RealDictCursor #Used for accesing data using column name
app = Flask(__name__)

#DB Connection
conn = psycopg2.connect("dbname='onlineshop' host='localhost' user='postgres' password='!p@ssword1234' port='5432'")

#Load Records from database
@app.route('/')
def index():
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    psql = "select * from customers"
    cursor.execute(psql)
    customers = cursor.fetchall()
    return render_template('index.html', customers=customers)

#Creating Account
@app.route('/create', methods=['POST'])
def create():
    fname = request.form['fname'];
    lname = request.form['lname'];
    gender = request.form['gender'];
    birthday = request.form['birthday'];
    email_address = request.form['email_address'];
    username = request.form['username'];
    password = request.form['password'];
    contact = request.form['contact'];
    cursor = conn.cursor()
    psql = '''INSERT INTO customers (first_name, last_name, gender, birthday, email_address, username, password, contact) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
    data = (fname, lname, gender, birthday, email_address, username, password, contact)
    cursor.execute(psql, data)
    conn.commit()
    cursor.close()
    #conn.close()
    return "<script>alert('Register Successfully!');window.location.href='/';</script>"

#Editing Account
@app.route('/edit/<id>', methods=['POST', 'GET'])
def edit(id):
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    psql = "select * from customers where customer_id=%s"
    cursor.execute(psql, id)
    customers = cursor.fetchone()
    return render_template('edit.html', customers=customers)

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    fname = request.form['fname'];
    lname = request.form['lname'];
    gender = request.form['gender'];
    birthday = request.form['birthday'];
    email_address = request.form['email_address'];
    username = request.form['username'];
    password = request.form['password'];
    contact = request.form['contact'];
    cursor = conn.cursor()
    psql = "update customers set first_name=%s,last_name=%s, gender=%s, birthday=%s, email_address=%s, username=%s, password=%s, contact=%s where customer_id=%s"
    data = (fname, lname, gender, birthday, email_address, username, password, contact, id)
    cursor.execute(psql,data)
    return "<script>alert('Updated Successfully!');window.location.href='/';</script>"

#Deleting Account
@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    cursor = conn.cursor()
    psql = "delete from customers where customer_id=%s"
    cursor.execute(psql,id)
    return "<script>alert('Deleted Successfully!');window.location.href='/';</script>"

#Search Account
@app.route('/search', methods=['POST'])
def search():
    filter = request.form['filter'];
    keyword = request.form['keyword'];
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    psql = "select * from customers where "+filter+" like '%"+keyword+"%'"
    cursor.execute(psql)
    customers = cursor.fetchall()
    return render_template('index.html', customers=customers, keyword=keyword)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
