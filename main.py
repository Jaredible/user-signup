from flask import Flask, request, redirect, render_template
import cgi
import re

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too

@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    username = request.args.get("username")
    return render_template('welcome.html', username=username)

@app.route("/")
def index():
    return render_template('signup.html')

@app.route("/", methods=['POST'])
def login():
    username = cgi.escape(request.form['username'].strip())
    password = cgi.escape(request.form['password'].strip())
    verify = cgi.escape(request.form['verify'].strip())
    email = cgi.escape(request.form['email'].strip())
    username_error = ''
    password_error = ''
    verify_error = ''
    email_error = ''

    if (not username) or username == "" or " " in username or len(username) < 3 or len(username) > 20:
        username_error = "That's not a valid username"

    if (not password) or password == "" or " " in password or len(password) < 3 or len(password) > 20:
        password_error = "That's not a valid password"

    if ((not verify) or verify == "" or (password and verify != password)) and password:
        verify_error = "Passwords don't match"

    # TODO regex string length
    if re.match("/\S+@\S+\.\S+/", email) or len(email) < 3 or len(email) > 20:
        email_error = "That's not a valid email"

    if username_error == '' and password_error == '' and verify_error == '' and email_error == '':
        return redirect("/welcome?username=" + username)

    return render_template('signup.html', username=username, email=email, username_error=username_error, password_error=password_error, verify_error=verify_error, email_error=email_error)

app.run()
