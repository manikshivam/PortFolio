# main.py

from flask import Flask, render_template, request, redirect, url_for, session,flash
from model import create_table, insert_message, get_all_messages,delete_message
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

with open('config.json', 'r') as config_file:
    admin_credentials = json.load(config_file)

create_table()

@app.route('/')
def index():
    messages = get_all_messages()
    return render_template('index.html', messages=messages)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        email = request.form['email']
        mobile = request.form['mobile']
        message = request.form['message']

        insert_message(name, email, mobile, message)
        return redirect(url_for('index'))

    # If it's a GET request, render the contact form
    return render_template('contact.html')



@app.route('/admin')
def admin():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == admin_credentials['username'] and password == admin_credentials['password']:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')


@app.route('/dashboard')
def dashboard():
    if session.get('logged_in'):
        messages = get_all_messages()
        return render_template('dashboard.html', messages=messages)
    else:
        return redirect(url_for('index'))
    
@app.route('/delete/<int:message_id>', methods=['POST'])
def delete_entry(message_id):
    if session.get('logged_in'):
        if message_id:
            delete_message(message_id)
            flash('Message deleted successfully', 'success')
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

 

if __name__ == '__main__':
    app.run(debug=True)
