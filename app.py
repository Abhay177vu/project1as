from flask import Flask, render_template, request, session, redirect, url_for
import os
import webbrowser

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_secret_key')  # Secret key for session management

# Define the directories to store the data files
data_directory = os.environ.get('DATA_DIRECTORY', 'form_data')
blocked_users_directory = os.environ.get('BLOCKED_USERS_DIRECTORY', 'blocked_users_data')

# Ensure the data directories exist
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

if not os.path.exists(blocked_users_directory):
    os.makedirs(blocked_users_directory)

@app.route('/')  # Root URL
def index():
    return render_template('project1.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Initialize the counter if it doesn't exist in the session
    if 'failed_attempts' not in session:
        session['failed_attempts'] = 0

    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']

    # Perform validation
    name_valid = name.isalpha()
    email_valid = '@' in email and '.' in email
    phone_valid = phone.isdigit() and len(phone) == 10

    # Increment failed attempts if validation fails
    if not (name_valid and email_valid and phone_valid):
        session['failed_attempts'] += 1

        # If 3 failed attempts, block further submissions
        if session['failed_attempts'] >= 3:
            # Move the user data to blocked users directory
            with open(os.path.join(blocked_users_directory, 'blocked_user_data.txt'), 'a') as f:
                f.write(f"Name: {name}, Email: {email}, Phone: {phone}\n")
            return render_template('submit.html', message='You have exceeded the maximum number of attempts. Further submissions are blocked.')

        attempts_left = 3 - session['failed_attempts']
        return render_template('submit.html', message=f'Invalid input. You have {attempts_left} attempts left.')

    # Reset failed attempts counter if validation succeeds
    session['failed_attempts'] = 0

    # Store data in text files
    with open(os.path.join(data_directory, 'names.txt'), 'a') as f:
        f.write(name + '\n')
    with open(os.path.join(data_directory, 'emails.txt'), 'a') as f:
        f.write(email + '\n')
    with open(os.path.join(data_directory, 'phones.txt'), 'a') as f:
        f.write(phone + '\n')

    # Return success message
    return render_template('submit.html', message='Form submitted successfully!')

@app.route('/submit', methods=['GET'])  # Route for GET requests to /submit
def submit_page():
    # Redirect GET requests to /submit to the home page
    return redirect(url_for('index'))

# Add a route to handle GET requests to /submit.html directly
@app.route('/submit.html', methods=['GET'])
def submit_html():
    return render_template('submit.html', message='')  # Render the submit.html template without any message

if __name__ == '__main__':
    # Open project1.html in the default web browser when the Flask app starts
    if os.environ.get('FLASK_ENV') == 'development':
        webbrowser.open('http://127.0.0.1:5000/')
    app.run(debug=False, host='0.0.0.0')
