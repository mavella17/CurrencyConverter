import git
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
app = Flask(__name__)
proxied = FlaskBehindProxy(app)  # add this line
app.config['SECRET_KEY'] = '5e3ed03ed43c30693e1a3d191463aaff'


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', subtitle='Home Page',
                           text='This is the home page')


@app.route("/convert")
def convert():
    return render_template('convert.html', subtitle='Conversion Page',
                           text='This is the conversion page')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # checks if entries are valid
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))  # if so - send to home page
    return render_template('register.html', title='Register', form=form)


@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/currency1converter/CurrencyConverter')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
