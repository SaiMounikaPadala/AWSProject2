from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key in a production environment

# In-memory storage for user data (in a real app, use a database)
users = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']

        # Store user data (in-memory for this example)
        user_data = {
            'username': username,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
        }
        users.append(user_data)

        # Redirect to the next page
        return redirect(url_for('display_info', user_id=len(users)))

    return render_template('register.html')

@app.route('/display_info/<int:user_id>')
def display_info(user_id):
    # Retrieve user data based on user_id (index in the list)
    user_data = users[user_id - 1]
    return render_template('display_info.html', user_data=user_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']

        for user_data in users:
            if user_data['username'] == entered_username and user_data['password'] == entered_password:
                session['logged_in_user'] = user_data
                return redirect(url_for('profile'))

        # If login fails, redirect back to login page
        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'logged_in_user' in session:
        user_data = session['logged_in_user']
        return render_template('profile.html', user_data=user_data)
    else:
        # If not logged in, redirect to login page
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.pop('logged_in_user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

