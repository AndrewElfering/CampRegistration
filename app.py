from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

# Initialize the database
def initialize_database():
    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS Families (
                        family_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        email TEXT NOT NULL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Participants (
                        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        family_id INTEGER,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        status TEXT NOT NULL,
                        FOREIGN KEY (family_id) REFERENCES Families (family_id)
                      )''')

    conn.commit()
    conn.close()

# Send email notification
def send_email(to_email, subject, message):
    try:
        print("Sending email to:", to_email)
        print("Subject:", subject)

        from_email = 'regentcsci450@gmail.com'
        password = 'rfzz foex ygob vsso'  
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        
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

        # Construct MIMEText object with HTML content
        msg = MIMEText(html_message, 'html')  # Use 'html' as the content type
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        msg['X-Mailer'] = 'Python SMTP Script'  # Add this header for email tracking
        msg['Reply-To'] = from_email

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("HTML Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

     

# Flask Routes

@app.route('/')
def index():
    return render_template('index.html')  # Flask will look for this file in the 'templates' folder

@app.route('/signup', methods=['POST'])
def signup():
    name = request.form['name']
    email = request.form['email']

    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Add family to database
    cursor.execute('INSERT INTO Families (name, email) VALUES (?, ?)', (name, email))
    family_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Send confirmation email
    send_email(email, "Registration Confirmation", "Thank you for signing up for the Summer Camp!")

    flash("Registration successful! A confirmation email has been sent.")
    return redirect(url_for('index'))

@app.route('/cancel', methods=['POST'])
def cancel():
    email = request.form['email']

    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    # Delete family from the database
    cursor.execute('DELETE FROM Families WHERE email = ?', (email,))
    conn.commit()
    conn.close()

    # Send cancellation email
    send_email(email, "Registration Cancellation", "Your registration has been cancelled.")

    flash("Registration cancelled! A notification email has been sent.")
    return redirect(url_for('index'))

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)