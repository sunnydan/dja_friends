from flask import Flask, render_template, redirect, request
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'friendsdb')
# an example of running a query
print mysql.query_db("SELECT * FROM friends")

@app.route('/')
def index():
    friends = mysql.query_db("SELECT * FROM friends")
    return render_template("index.html", all_friends=friends);

@app.route('/friends', methods=["POST"])
def friends():
    query = "INSERT INTO friends (first_name, last_name, occupation, created_at, updated_at) VALUES (:first_name, :last_name, :occupation, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'],
             'last_name':  request.form['last_name'],
             'occupation': request.form['occupation']
           }
    mysql.query_db(query, data)
    return redirect("/")

@app.route('/remove_friend/<friend_id>', methods=['POST'])
def delete(friend_id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': friend_id}
    mysql.query_db(query, data)
    return redirect('/')

@app.route('/reset', methods=["POST"])
def reset():
    mysql.query_db("DELETE FROM friends WHERE id > 0")
    return redirect('/')

app.run(debug=True)
