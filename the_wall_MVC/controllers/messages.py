from flask import Flask, render_template, request, redirect, session, flash, jsonify
from the_wall_MVC.models.message import Message
import re
from the_wall_MVC import bcrypt
import datetime
import time
from datetime import timedelta, datetime

message = Message()

class Messages():

    def add_comment(self):

        if len(request.form["comment"]) < 1:
            return redirect("/dashboard")
        message.add_comment()
        return redirect("/dashboard")


    def dashboard(self):

        if not "user_id" in session.keys():
            flash("Please log in to view this page", "login")
            return redirect("/")  #failure
        else:

            info = message.getInfo()
            session["messages"] = info[1]
            for post in session["messages"]:
                post["date"] = datetime.strftime(post["created_at"],'%B %d, %Y')
                for comment in post["comments"]:
                    comment["date"] = datetime.strftime(comment["created_at"],'%B %d, %Y')
            session["messages_count"] = len(session["messages"])
            session["user"] = info[0][0]
            session["cutoff_time"] = datetime.now() - timedelta(minutes=30)

            if "secret_hash" in session.keys() and bcrypt.check_password_hash(session["secret_hash"], str(session["user"]["created_at"]) + "melon"):
                return render_template("wall_dashboard.html")   #success
            else:
                flash("Don't hack my site you jerk", "login")
                return redirect("/") #failure
        return render_template("index.html")


    def delete(self, id):

        message.delete(id)
        return redirect("/dashboard")


    def delete_comment(self, comment_id):

        message.delete_comment(comment_id)
        return redirect("/dashboard")


    def home(self):

        session.pop("user_id", None)
        session.pop("secret_hash", None)
        return render_template("index.html")


    def logIn(self):

        user = message.logIn()
        if user:
            session["user_id"] = user["id"]
            session["secret_hash"] = bcrypt.generate_password_hash(str(user["created_at"]) + "melon")
            return redirect("/dashboard")#success

        session["email2"] = request.form["email"]
        flash("Incorrect email or password", "login")
        return redirect("/")#failure


    def logOut(self):

        session.clear()
        return redirect("/")


    def post(self):

        if len(request.form["message"]) < 1:
            flash("Please enter a message to post", "post")
            return redirect("/dashboard")

        message.post()
        return redirect("/dashboard")


    def reg(self):

        if len(request.form["first_name"]) < 2:
            flash("Please enter a valid first name", "first_name")
        elif not request.form["first_name"].isalpha():
            flash("First names may only contain letters", "first_name")

        if len(request.form["last_name"]) < 2:
            flash("Please enter a valid last name", "last_name")
        elif not request.form["last_name"].isalpha():
            flash("Last names may only contain letters", "last_name")

        emailRegEx = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(request.form["email"]) <= 1:
            flash("Plese enter a valid email", "email")
        elif not emailRegEx.match(request.form["email"]):
            flash("Plese enter a valid email", "email")

        if message.checkEmail():
            flash("That email address is already registered!", "email")

        if len(request.form["password"]) < 2:
            flash("Please enter a valid password", "password")
        elif len(request.form["password"]) < 8:
            flash("Passwords must be at least 8 characters", "password")
        
        if len(request.form["confirm_password"]) < 2:
            flash("Please confirm your password", "confirm_password")
        elif request.form["confirm_password"] != request.form["password"]:
            flash("Your password must match", "password")
            flash("Your password must match", "confirm_password")

        today = datetime.now()

        if len(request.form["birth"]) < 2:
            flash("Please enter your date of birth", "birth")
        elif datetime.strptime(request.form["birth"], "%m/%d/%Y").year > today.year - 18:
            flash("Sorry you must be 18 to use this site", "birth")

        if "_flashes" in session.keys():
            session["first_name"] = request.form["first_name"]
            session["last_name"] = request.form["last_name"]
            session["email"] = request.form["email"]
            session["birth"] = request.form["birth"]
            return redirect("/") #failure
        else:
            userIdCreated = message.add_user()
            session["user_id"] = userIdCreated[0]
            created_at = userIdCreated[1]
            session["secret_hash"] = bcrypt.generate_password_hash(str(created_at) + "melon")
            return redirect("/dashboard") #success