import sqlite3

conn = sqlite3.connect('summer_camp.db')
cursor = conn.cursor()

# Delete the old Participants table
cursor.execute("DROP TABLE IF EXISTS Participants")

# Recreate Participants table with Registration ID
cursor.execute('''
    CREATE TABLE Participants (
        participant_id INTEGER PRIMARY KEY AUTOINCREMENT,
        family_id INTEGER,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        status TEXT NOT NULL,
        registration_id TEXT UNIQUE NOT NULL,
        FOREIGN KEY (family_id) REFERENCES Families (family_id)
    )
''')

conn.commit()
conn.close()

print("Database schema updated! Participants table now includes registration_id.")