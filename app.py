# Import required modules
from flask import Flask, render_template, request, redirect, url_for, flash  # Flask components for handling web requests
import sqlite3  # Database management using SQLite
import smtplib  # Email handling using the SMTP protocol
from email.mime.text import MIMEText  # Formatting emails as MIME messages

# Initialize Flask application
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Used for session-based flash messages

# Function to initialize the database and create tables
def initialize_database():
    conn = sqlite3.connect('summer_camp.db')  # Store DB in /tmp folder
    cursor = conn.cursor()

    # Create Families table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Families (
            family_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    ''')

    # Create Participants table with Registration ID
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Participants (
            participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            family_id INTEGER,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            status TEXT NOT NULL,
            registration_id TEXT UNIQUE NOT NULL,
            FOREIGN KEY (family_id) REFERENCES Families (family_id)
        )
    ''')

    # Create Waitlist table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Waitlist (
            waitlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

# Function to send an email notification
def send_email(to_email, subject, message):
    try:
        from_email = 'regentcsci450@gmail.com'
        password = 'rfzz foex ygob vsso'
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        # Create email message dynamically
        msg = MIMEText(message, 'plain')  # Ensure the message comes from signup/cancellation
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # Connect to SMTP and send email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")  # Debugging output
    
    except Exception as e:
        print("Failed to send email:", e)

# Define Flask routes

# Homepage route
@app.route('/')
def index():
    try:
        conn = sqlite3.connect('summer_camp.db')
        cursor = conn.cursor()

        # Count registered families
        cursor.execute('SELECT COUNT(*) FROM Families')
        current_signups = cursor.fetchone()[0]
        remaining_spots = max(0, 5 - current_signups)

        # Count waitlisted users
        cursor.execute('SELECT COUNT(*) FROM Waitlist')
        waitlist_size = cursor.fetchone()[0]

        conn.close()
        return render_template('index.html', remaining_spots=remaining_spots, waitlist_size=waitlist_size)
    
    except Exception as e:
        return f"Error: {str(e)}", 500  # Display error message instead of crashing
    
# Route for signing up new families
import random
import string

def generate_registration_id():
    """Generate a unique registration ID."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # Example: "AB12CD34"

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']
    registration_id = generate_registration_id()  # Generate unique Registration ID

    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Count current signups
    cursor.execute('SELECT COUNT(*) FROM Families')
    current_signups = cursor.fetchone()[0]
    remaining_spots = max(0, 2 - current_signups)

    if remaining_spots > 0:  # Register participant
        cursor.execute('INSERT INTO Families (name, email) VALUES (?, ?)', (name, email))
        family_id = cursor.lastrowid  # Get family ID

        # Insert participant into database
        cursor.execute('INSERT INTO Participants (family_id, name, age, status, registration_id) VALUES (?, ?, ?, ?, ?)',
                       (family_id, name, 10, 'registered', registration_id))
        conn.commit()

        # Fetch the Registration ID from the database (making sure it was inserted correctly)
        cursor.execute('SELECT registration_id FROM Participants WHERE family_id = ?', (family_id,))
        stored_registration_id = cursor.fetchone()[0]  # Correctly retrieve stored ID

        # Send confirmation email with the correct Registration ID
        send_email(email, "Registration Confirmation",
                   f"Thank you for signing up for the Summer Camp!\nYour Registration ID: {stored_registration_id}\nUse this ID if you wish to cancel.")

        flash(f"Registration successful! Your Registration ID: {stored_registration_id}. A confirmation email has been sent.")
    
    else:  # Add user to the waitlist with Registration ID
        cursor.execute('INSERT INTO Waitlist (name, email, registration_id) VALUES (?, ?, ?)', (name, email, registration_id))
        conn.commit()

        send_email(email, "Waitlist Confirmation",
                   f"You’ve been added to the Summer Camp waitlist!\nYour Waitlist Registration ID: {registration_id}\nUse this ID if you wish to cancel.")

        flash(f"Registration is full. You've been added to the waitlist with Registration ID: {registration_id}.")

    conn.close()
    return redirect(url_for('index'))

# Route for canceling a registration
@app.route('/cancel', methods=['POST'])
def cancel():
    registration_id = request.form['registration_id']  # Get Registration ID input

    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Find participant with this Registration ID
    cursor.execute('SELECT family_id FROM Participants WHERE registration_id = ?', (registration_id,))
    family_record = cursor.fetchone()

    if family_record:
        family_id = family_record[0]

        # Remove participant from Participants table
        cursor.execute('DELETE FROM Participants WHERE registration_id = ?', (registration_id,))
        conn.commit()

        # Remove family record if no participants remain
        cursor.execute('SELECT COUNT(*) FROM Participants WHERE family_id = ?', (family_id,))
        remaining_participants = cursor.fetchone()[0]

        if remaining_participants == 0:
            cursor.execute('DELETE FROM Families WHERE family_id = ?', (family_id,))
            conn.commit()

        send_email("Your registered email", "Registration Cancellation",
                   f"Your registration (ID: {registration_id}) has been canceled.")
        flash("Your registration has been canceled.")
    
    else:
        flash("Invalid Registration ID. Please try again.")

    conn.close()
    return redirect(url_for('index'))

# Entry point: starts the Flask application
if __name__ == "__main__":
    initialize_database()  # Ensure database is set up
    app.run(debug=True)  # Run Flask server with debugging enabled  
