import sqlite3
import smtplib
from email.mime.text import MIMEText

# Initialize database
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

    cursor.execute('''CREATE TABLE IF NOT EXISTS Waitlist (
                        waitlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        family_id INTEGER,
                        timestamp TEXT NOT NULL,
                        FOREIGN KEY (family_id) REFERENCES Families (family_id)
                      )''')

    conn.commit()
    conn.close()

# Send email notification
def send_email(to_email, subject, message):
    try:
        from_email = 'your_email@example.com'
        password = 'your_password'

        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        # SMTP settings (update with your provider's settings)
        smtp_server = 'smtp.example.com'
        smtp_port = 587

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()

        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", e)

# Example functions for adding families and participants
def add_family(name, email):
    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Families (name, email) VALUES (?, ?)', (name, email))
    family_id = cursor.lastrowid
    conn.commit()
    conn.close()

    print(f"Family added: {name}, {email}")
    return family_id

def add_participant(family_id, name, age, status):
    conn = sqlite3.connect('summer_camp.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO Participants (family_id, name, age, status) VALUES (?, ?, ?, ?)',
                   (family_id, name, age, status))
    conn.commit()
    conn.close()

    print(f"Participant added: {name}, Age: {age}, Status: {status}")

# Main
if __name__ == "__main__":
    initialize_database()

    # Add a new family
    family_id = add_family("Smith Family", "smithfamily@example.com")

    # Add a participant
    add_participant(family_id, "John Smith", 15, "Active")

    # Notify family about their registration
    send_email("smithfamily@example.com", "Summer Camp Registration",
               "Welcome to the Summer Camp! Your registration is confirmed.")