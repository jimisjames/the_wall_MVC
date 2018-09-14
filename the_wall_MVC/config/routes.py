from the_wall_MVC import app
from the_wall_MVC.controllers.messages import Messages

messages = Messages()


@app.route("/")
def home():

    return messages.home()


@app.route("/dashboard")
def dashboard():

    return messages.dashboard()


@app.route("/reg", methods=["POST"])
def reg():

    return messages.reg()


@app.route("/login", methods=["POST"])
def logIn():

    return messages.logIn()


@app.route("/logout")
def logOut():

    return messages.logOut()


@app.route("/post", methods=["POST"])
def post():

    return messages.post()


@app.route("/delete/<id>")
def delete(id):

    return messages.delete(id)