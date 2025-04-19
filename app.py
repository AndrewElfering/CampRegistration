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
    conn = sqlite3.connect('summer_camp.db')  # Connect to SQLite database (or create one if it doesn't exist)
    cursor = conn.cursor()  # Create a cursor to execute SQL queries

    # Create Families table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Families (
                        family_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Auto-incrementing unique identifier
                        name TEXT NOT NULL,  # Family name (required)
                        email TEXT NOT NULL  # Email address (required)
                      )''')

    # Create Participants table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Participants (
                        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Auto-incrementing unique identifier
                        family_id INTEGER,  # Foreign key linking to Families table
                        name TEXT NOT NULL,  # Participant's name (required)
                        age INTEGER NOT NULL,  # Age (required)
                        status TEXT NOT NULL,  # Status (e.g., "registered", "canceled") (required)
                        FOREIGN KEY (family_id) REFERENCES Families (family_id)  # Ensures referential integrity
                      )''')

    conn.commit()  # Commit changes to the database
    conn.close()  # Close the connection

# Function to send an email notification
def send_email(to_email, subject, message):
    try:
        print("Sending email to:", to_email)  # Debugging print statements
        print("Subject:", subject)

        # Email credentials and server settings
        from_email = 'regentcsci450@gmail.com'  # Sender email address
        password = 'rfzz foex ygob vsso'  # Password for SMTP authentication
        smtp_server = 'smtp.gmail.com'  # SMTP server for Gmail
        smtp_port = 587  # Port for TLS encryption

        # Constructing the HTML email message
        html_message = f"""
        <html>
            <body>
                <h2>Registration Confirmation</h2>
                <p>Dear {to_email},</p>
                <p>Thank you for signing up for the <strong>Summer Camp</strong>!</p>
                <p>We’re excited to have you join us. If you have any questions, feel free to reply to this email.</p>
                <br>
                <p>Best regards,</p>
                <p><strong>Regent University Summer Camp Team</strong></p>
            </body>
        </html>
        """

        # Formatting email as HTML
        msg = MIMEText(html_message, 'html')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg['X-Mailer'] = 'Python SMTP Script'
        msg['Reply-To'] = from_email

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Start TLS encryption
        server.login(from_email, password)  # Log in to the email account
        server.sendmail(from_email, to_email, msg.as_string())  # Send email
        server.quit()  # Close connection

        print("HTML Email sent successfully!")  # Confirmation message
    except Exception as e:
        print("Failed to send email:", e)  # Handle errors gracefully

# Define Flask routes

# Homepage route
@app.route('/')
def index():
    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Count registered families
    cursor.execute('SELECT COUNT(*) FROM Families')
    current_signups = cursor.fetchone()[0]
    remaining_spots = max(0, 2 - current_signups)

    # Count waitlisted users
    cursor.execute('SELECT COUNT(*) FROM Waitlist')
    waitlist_size = cursor.fetchone()[0]

    conn.close()
    return render_template('index.html', remaining_spots=remaining_spots, waitlist_size=waitlist_size)

# Route for signing up new families
@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']  # Retrieve name from form submission
    email = request.form['email']  # Retrieve email from form submission

    conn = sqlite3.connect('summer_camp.db')  # Open database connection
    cursor = conn.cursor()

    # Insert new family into the database
    cursor.execute('INSERT INTO Families (name, email) VALUES (?, ?)', (name, email))
    family_id = cursor.lastrowid  # Get ID of the newly added family
    conn.commit()
    conn.close()  # Close connection

    # Send confirmation email
    send_email(email, "Registration Confirmation", "Thank you for signing up for the Summer Camp!")

    flash("Registration successful! A confirmation email has been sent.")  # Notify user
    return redirect(url_for('index'))  # Redirect to homepage

# Route for canceling a registration
@app.route('/cancel', methods=['POST'])
def cancel():
    email = request.form['email']

    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Remove the family from the database
    cursor.execute('DELETE FROM Families WHERE email = ?', (email,))
    conn.commit()

    # Check if there’s anyone on the waitlist
    cursor.execute('SELECT waitlist_id, name, email FROM Waitlist ORDER BY timestamp LIMIT 1')
    waitlisted_user = cursor.fetchone()

    if waitlisted_user:  # If someone is on the waitlist, move them into the Families table
        waitlist_id, name, waitlist_email = waitlisted_user
        cursor.execute('INSERT INTO Families (name, email) VALUES (?, ?)', (name, waitlist_email))
        cursor.execute('DELETE FROM Waitlist WHERE waitlist_id = ?', (waitlist_id,))
        conn.commit()

        send_email(waitlist_email, "Waitlist Promotion", "A spot has opened up! You're now registered for the camp.")
        flash(f"{name} has been moved from the waitlist to the camp!")
    
    conn.close()
    flash("Your registration has been canceled.")
    return redirect(url_for('index'))

# Entry point: starts the Flask application
if __name__ == "__main__":
    initialize_database()  # Ensure database is set up
    app.run(debug=True)  # Run Flask server with debugging enabled