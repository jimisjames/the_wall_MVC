from flask import Flask, render_template, request, redirect, session, flash
from the_wall_MVC.config.mysqlconnection import connectToMySQL
from the_wall_MVC import bcrypt

class Message():

    def add_user(self):
        myDb = connectToMySQL('walldb')
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, now(), now());"
        data = {
            "first_name" : request.form["first_name"],
            "last_name" : request.form["last_name"],
            "email" : request.form["email"],
            "password" : bcrypt.generate_password_hash(request.form["password"] + "melon")
        }
        newUserId = myDb.query_db(query, data)
        newUserCreated_at = myDb.query_db("SELECT created_at FROM users WHERE id = %s" % (newUserId))
        newUserCreated_at = newUserCreated_at[0]["created_at"]
        return [newUserId, newUserCreated_at]


    def checkEmail(self):
        myDb = connectToMySQL('walldb')
        for user in myDb.query_db("SELECT email FROM users;"):
            if request.form["email"] == user["email"]:
                return True
        return False


    def getInfo(self):
        myDb = connectToMySQL('walldb')
        query = "SELECT first_name, last_name, email, created_at FROM users WHERE id = %(id)s;"
        data = {
            "id" : session["user_id"]
        }
        user_info = myDb.query_db(query, data)
        messages = myDb.query_db("SELECT messages.id, user_id, message, messages.created_at, CONCAT(first_name, ' ', last_name) AS name FROM messages JOIN users ON messages.user_id = users.id;")
        return [user_info, messages]


    def logIn(self):
        myDb = connectToMySQL('walldb')
        query = "SELECT first_name, last_name, id, password, created_at FROM users WHERE email = %(email)s;"
        data = {
            "email" : request.form["email"]
        }
        users = myDb.query_db(query, data)

        for user in users:
            if bcrypt.check_password_hash(user["password"], request.form["password"] + "melon"):
                return user
        return False


    def post(self):
        myDb = connectToMySQL('walldb')
        query = "INSERT INTO messages (user_id, message, created_at, updated_at) VALUES (%(user_id)s, %(message)s, now(), now());"
        data = {
            "user_id" : session["user_id"],
            "message" : request.form["message"]
        }
        myDb.query_db(query, data)
        return


    def delete(self, id):
        myDb = connectToMySQL('walldb')
        myDb.query_db("DELETE FROM messages WHERE id = %s;" % (id))
        return
