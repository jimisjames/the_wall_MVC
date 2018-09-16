from the_wall_MVC import app
from the_wall_MVC.controllers.messages import Messages

messages = Messages()


@app.route("/")
def home():

    return messages.home()


@app.route("/add/comment", methods=["POST"])
def addComment():

    return messages.add_comment()


@app.route("/dashboard")
def dashboard():

    return messages.dashboard()


@app.route("/delete/<id>")
def delete(id):

    return messages.delete(id)


@app.route("/delete/comment/<comment_id>")
def deleteComment(comment_id):

    return messages.delete_comment(comment_id)


@app.route("/login", methods=["POST"])
def logIn():

    return messages.logIn()


@app.route("/logout")
def logOut():

    return messages.logOut()


@app.route("/post", methods=["POST"])
def post():

    return messages.post()


@app.route("/reg", methods=["POST"])
def reg():

    return messages.reg()