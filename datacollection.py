from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_required, login_user, logout_user
from user import User
from passwordhelper import PasswordHelper
from forms import RegistrationForm
from forms import LoginForm
from dbhelper import DBHelper as DBHelper
from grammar import Grammar
from wtf_tinymce import wtf_tinymce

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
login_manager = LoginManager(app)
wtf_tinymce.init_app(app)
app.secret_key = 'flkjsdfF7348503N=[F-0O3I4URasdfa7U8D54ferP4]WEOIEUPWc45u8O48DHOEkiwerRIGOQ'


@app.route("/")
def home():
    return render_template("home.html", loginform=LoginForm())


@app.route("/account")
@login_required
def account():
    return redirect(url_for("dashboard"))


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invaild")
    return render_template("home.html", loginform=form)


@app.route("/logout", methods=["POST"])
def logout():
    logout_user()
    return render_template("home.html", loginform=LoginForm())


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        form = RegistrationForm(request.form)
        if form.validate_on_submit():
            if DB.get_user(form.email.data):
                form.email.errors.append("Email address already registered")
                return render_template("registration.html", registrationform=form)
            salt = PH.get_salt()
            hashed = PH.get_hash(form.password2.data + salt)
            DB.add_user(form.email.data, salt, hashed)
            return render_template("home.html", registrationform=form, onloadmessage="Registration successful. Please log in.", loginform=LoginForm())
        return render_template("registration.html", registrationform=form)
    registrationform = RegistrationForm()
    return render_template("registration.html", registrationform=registrationform)


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


#The error I'm getting says that text is none
@app.route("/summary", methods=["POST"])
def summary():
    text = request.form["text"]
    summary = Grammar.Summary(text)
    return summary


if __name__ == '__main__':
    app.run(port=5000, debug=True)