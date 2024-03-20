import sqlite3

# Set up
# Connect to the database
connection = sqlite3.connect('archives.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, highscore INTEGER)")
cursor.execute("CREATE TABLE IF NOT EXISTS privateUsers (username TEXT, account INTEGER)")
cursor.connection.commit()

# Methods
def getName(cursor, table):
    cursor.execute(f"SELECT username FROM {table}")
    results = cursor.fetchall()
    if len(results) == 0:
        print("No users detected.")
        return None
    # Print the names
    for x in range(len(results)):
        print(f"{x+1} - {results[x][0]}")
    choice = 0
    # Find a specific name
    while choice < 1 or choice > len(results):
        choice = int(input("Name ID: "))
    return results[choice - 1][0]

def getHighScore(cursor):
    cursor.execute("SELECT highscore FROM users")
    results = cursor.fetchall()
    if len(results) == 0:
        print("No users detected")
        return None
    for x in range(len(results)):
        print(f"{x+1} - {results[x][0]}")
    choice = 0
    while choice < 1 or choice > len(results):
        choice = int(input("Name ID: "))
    return results[choice - 1][0]

def joinTables(cursor):
    cursor.execute("SELECT * FROM users LEFT JOIN privateUsers")
    result = cursor.fetchall()

# Active Portion
choice = None
while choice != "8":
    # Loop through the options
    print("1: Display Table")
    print("2) Add User")
    print("3) Update User Highscore")
    print("4) Delete User")
    print("5) Calculate Average Highscore")
    print("6) Display # of Users")
    print("7) Swap Tables")
    print("8) Quit")
    choice = input("> ")
    print("")
    if choice == "1":
        # Display Table
        results = cursor.execute("SELECT * FROM users ORDER BY highscore DESC")
        print("{:>10}  {:>10}".format("Username", "Highscore"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}".format(record[0], record[1]))
        print("")
    elif choice == "2":
        # Add User
        try:
            username = input("Username: ")
            highscore = input("Highscore: ")
            values = (username, highscore)
            cursor.execute("INSERT INTO users VALUES (?,?)", values)
            connection.commit()
        except ValueError:
            print("Invalid Score")
    elif choice == "3":
        # Update User Highscore
        try:
            username = input("Username: ")
            highscore = input("Highscore: ")
            values = (highscore, username)
            cursor.execute("UPDATE users SET highscore = ? WHERE username = ?", values)
            connection.commit()
            if cursor.rowcount == 0:
                print("Invalid Username")
        except ValueError:
            print("Invalid Score")
    elif choice == "4":
        # Delete User
        table = input("Table Name: ")
        username = getName(cursor, table)
        if username == None:
            continue
        values = (username, )
        cursor.execute("DELETE FROM users WHERE username = ?", values)
        cursor.execute("DELETE FROM privateUsers WHERE username = ?", values)
        connection.commit()
    elif choice == "5":
        # Print result of the average highscore
        results = cursor.execute("SELECT avg(highscore) FROM users")
        print(results.fetchone())
    elif choice == "6":
        # Count number of users for a larger table
        results = cursor.execute("SELECT COUNT(*) FROM users")
        print(results.fetchone())
    elif choice == "7":
        # Swap tables to the private table
        choice = None
        while choice != "7" and choice != "6":
            print("1: Display Table")
            print("2) Add User")
            print("3) Update User Account #")
            print("4) Delete User")
            print("5) Display # of Users")
            print("6) Swap Tables")
            print("7) Quit")
            choice = input("> ")
            print("")
            if choice == "1":
                # Display Table
                results = cursor.execute("SELECT * FROM privateUsers ORDER BY account DESC")
                print("{:>10}  {:>10}".format("Username", "Account"))
                for record in cursor.fetchall():
                    print("{:>10}  {:>10}".format(record[0], record[1]))
                print("")
            elif choice == "2":
                # Add User
                try:
                    username = input("Username: ")
                    account = input("Account: ")
                    values = (username, account)
                    cursor.execute("INSERT INTO privateUsers VALUES (?,?)", values)
                    connection.commit()
                except ValueError:
                    print("Invalid Score")
            elif choice == "3":
                # Update User Account
                try:
                    username = input("Username: ")
                    account = input("Account: ")
                    values = (highscore, username)
                    cursor.execute("UPDATE users SET account = ? WHERE username = ?", values)
                    connection.commit()
                    if cursor.rowcount == 0:
                        print("Invalid Username")
                except ValueError:
                    print("Invalid Score")
            elif choice == "4":
                # Delete User
                username = getName(cursor)
                if username == None:
                    continue
                values = (username, )
                cursor.execute("DELETE FROM users WHERE username = ?", values)
                cursor.execute("DELETE FROM privateUsers WHERE username = ?", values)
                connection.commit()
            elif choice == "5":
                # Count number of users for a larger table
                results = cursor.execute("SELECT COUNT(*) FROM privateUsers")
                print(results.fetchone())

connection.close