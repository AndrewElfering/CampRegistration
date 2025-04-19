import sqlite3

conn = sqlite3.connect('summer_camp.db')
cursor = conn.cursor()

# Clear the Families table to reset spots
cursor.execute('DELETE FROM Families')
conn.commit()
conn.close()

print("Database reset! Spots should now correctly display 2 at start.")
