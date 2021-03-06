from flask import Flask, render_template, redirect, url_for, request, session
from flask_login import LoginManager, login_required, login_user, logout_user
from user import User
from texts import Texts
from passwordhelper import PasswordHelper
from forms import RegistrationForm
from forms import LoginForm
from dbhelper import DBHelper as DBHelper
from grammar import Grammar
from wtf_tinymce import wtf_tinymce
import ProWritingAidSDK
import uuid
import datetime
from bs4 import BeautifulSoup

DB = DBHelper()
PH = PasswordHelper()

app = Flask(__name__)
login_manager = LoginManager(app)
wtf_tinymce.init_app(app)
app.secret_key = 'flkjsdfF7348503N=[F-0O3I4URasdfa7U8D54ferP4]WEOIEUPWc45u8O48DHOEkiwerRIGOQ'

configuration = ProWritingAidSDK.Configuration()
configuration.host = 'https://api.prowritingaid.com'
configuration.api_key['licenseCode'] = 'A17D00BF-3DF2-40DA-AE0F-0B8172F2CB1C'


@app.route("/")
def home():
    return render_template("home.html", loginform=LoginForm())


@app.route("/account")
@login_required
def account():
    return redirect(url_for("predashboard"))


@app.route("/login", methods=["POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        stored_user = DB.get_user(form.loginemail.data)
        if stored_user and PH.validate_password(form.loginpassword.data, stored_user['salt'], stored_user['hashed']):
            user = User(form.loginemail.data)
            login_user(user, remember=True)
            session['username'] = form.loginemail.data
            DB.click_login(user_id=session['username'], date=datetime.datetime.utcnow())
            return redirect(url_for('account'))
        form.loginemail.errors.append("Email or password invalid")
    return render_template("home.html", loginform=form)


@app.route("/predashboard")
def predashboard():
    user = DB.get_user(session['username'])
    return render_template("predashboard.html", user=user)


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


@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)
    if user_password:
        return User(user_id)


@app.route("/dashboardmon", methods=["GET"])
@login_required
def dashboardmon():
    texts = DB.get_texts(session['username'])
    return render_template("dashboardcontrol.html", texts=texts)


@app.route("/dashboardfri", methods=["GET"])
@login_required
def dashboardfri():
    texts = DB.get_texts(session['username'])
    return render_template("dashboard.html", texts=texts)


@app.route("/deletetext")
@login_required
def deletetext():
    text_id = request.args.get("text_id")
    DB.delete_text(text_id)
    return redirect(url_for("dashboardfri"))


@app.route("/deletetextcontrol")
@login_required
def deletetextcontrol():
    text_id = request.args.get("text_id")
    DB.delete_text(text_id)
    return redirect(url_for("dashboardmon"))


@app.route("/updatetext")
@login_required
def updatetext():
    text_id = request.args.get("text_id")
    text = request.args.get("text")
    DB.update_text(text_id, text)
    DB.click_save(user_id=session['username'], date=datetime.datetime.utcnow())
    DB.text_version(user_id=session['username'], date=datetime.datetime.utcnow(), text=text, status="saved")
    return redirect(url_for("dashboardfri"))


@app.route("/updatetextcontrol")
@login_required
def updatetextcontrol():
    text_id = request.args.get("text_id")
    text = request.args.get("text")
    DB.update_text(text_id, text)
    DB.click_save(user_id=session['username'], date=datetime.datetime.utcnow())
    DB.text_version(user_id=session['username'], date=datetime.datetime.utcnow(), text=text, status="saved")
    return redirect(url_for("dashboardmon"))


@app.route("/editor/<text_id>")
@login_required
def editor(text_id):
    text_id = DB.get_text(text_id)

    return render_template("editor.html", text=text_id)


@app.route("/basiceditor")
@login_required
def basiceditor():
    return render_template("basiceditor.html")


@app.route("/controleditor/<text_id>")
@login_required
def controleditor(text_id):
    text_id = DB.get_text(text_id)

    return render_template("controleditor.html", text=text_id)


@app.route("/summary/<text_id>", methods=["POST"])
@login_required
def summary(text_id):
    text = request.form["text"]
    DB.update_text(text_id, text)
    plaintext = BeautifulSoup(text)
    text_summary = Grammar.summary(plaintext.get_text())
    DB.click_summary(user_id=session['username'], date=datetime.datetime.utcnow())
    DB.text_version(user_id=session['username'], date=datetime.datetime.utcnow(), text=text, status="summary")

    return render_template("summary.html", text_summary=text_summary, text_id=text_id)


@app.route("/summarycontrol/<text_id>", methods=["POST"])
@login_required
def summarycontrol(text_id):
    text = request.form["text"]
    DB.update_text(text_id, text)
    plaintext = BeautifulSoup(text)
    text_summary = Grammar.summary(plaintext.get_text())
    DB.click_summary(user_id=session['username'], date=datetime.datetime.utcnow())
    DB.text_version(user_id=session['username'], date=datetime.datetime.utcnow(), text=text, status="summary")

    return render_template("summarycontrol.html", text_summary=text_summary, text_id=text_id)


@app.route("/newtext", methods=["GET", "POST"])
@login_required
def newtext():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['content']
        user = session['username']
        _id = uuid.uuid4().hex

        new_post = Texts(user, title, text, _id)
        new_post.save_to_db()

        text_summary = Grammar.summary(text)
        DB.text_version(user_id=session['username'], date=datetime.datetime.utcnow(), text=text, status="new")

        return render_template("summary.html", text_summary=text_summary, text_id=_id)
    else:
        return render_template("basiceditor.html")


@app.route("/newtextcontrol", methods=["GET", "POST"])
@login_required
def newtextcontrol():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        user = session['username']
        _id = uuid.uuid4().hex

        new_post = Texts(user, title, text, _id)
        new_post.save_to_db()

        return redirect(url_for("dashboardmon"))
    else:
        return render_template("controlbasiceditor.html")


@app.route("/submit", methods=["POST"])
def submit():
    text = request.form["text"]
    text_id = request.form["text_id"]
    DB.update_text(text_id, text)
    DB.submit_text(user_id=session['username'], text=text, date=datetime.datetime.utcnow())
    return redirect(url_for("dashboardfri"))


@app.route("/submitcontrol", methods=["POST"])
def submitcontrol():
    text = request.form["text"]
    text_id = request.form["text_id"]
    DB.update_text(text_id, text)
    DB.submit_text(user_id=session['username'], text=text, date=datetime.datetime.utcnow())
    return redirect(url_for("dashboardmon"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/tutorial")
def tutorial():
    return render_template("tutorial.html")


@app.route("/tutorialapp")
def tutorialapp():
    return render_template("tutorialapp.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
