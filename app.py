import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Load users data from JSON file
with open('users.json', 'r') as json_file:
    users = json.load(json_file)

@app.route('/')
def index():
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        # Basic form validation
        if not fullname or not email or not password1 or not password2:
            message = 'All form fields are required.'
            return render_template('index.html', message=message)

        if password1 != password2:
            message = 'Passwords do not match.'
            return render_template('index.html', message=message)

        # Simulate storing user data (replace with your storage mechanism)
        new_user = {
            'fullname': fullname,
            'email': email,
            'password': password1
        }
        users.append(new_user)

        # Save updated user data back to JSON file (optional step)
        with open('users.json', 'w') as json_file:
            json.dump(users, json_file, indent=4)

        message = f'Registration successful for {fullname}.'
        return render_template('index.html', message=message)

    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check credentials against loaded JSON data
        for user in users:
            if user['email'] == email and user['password'] == password:
                # Redirect to logged_in.html with email as parameter
                return redirect(f'/logged_in/{email}')

        message = 'Invalid credentials. Please try again.'
        return render_template('login.html', message=message)

    return render_template('login.html')

@app.route('/logged_in/<email>')
def logged_in(email):
    return render_template('logged_in.html', email=email)

@app.route('/signout')
def signout():
    # You may add additional logic here to clear session data or perform other actions
    return render_template('signout.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
