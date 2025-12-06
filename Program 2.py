#Mark Nyagaka
#Phonebook Database
#12-05-25

import sqlite3

DB_NAME = 'phonebook.db'

def get_connection():
    """Return a connection to the phonebook database."""
    return sqlite3.connect(DB_NAME)

# ---------- READ FUNCTIONS ----------

def show_all_entries():
    """Display all rows in the Entries table."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT Name, Phone FROM Entries ORDER BY Name')
    results = cur.fetchall()

    if not results:
        print("\nThe phone book is empty.")
    else:
        print("\nPhone Book Entries:")
        print(f"{'Name':25}Phone")
        print("-" * 40)
        for name, phone in results:
            print(f"{name:25}{phone}")

    conn.close()

def look_up_entry():
    """Look up a person's phone number by name."""
    name = input("Enter the name to look up: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute('SELECT Name, Phone FROM Entries WHERE Name = ?', (name,))
    results = cur.fetchall()

    if not results:
        print("No entry found with that name.")
    else:
        print("\nMatching entries:")
        print(f"{'Name':25}Phone")
        print("-" * 40)
        for n, phone in results:
            print(f"{n:25}{phone}")

    conn.close()

# ---------- UPDATE FUNCTION ----------

def update_entry():
    """Change a person's phone number."""
    name = input("Enter the name whose phone number you want to change: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    # Check if the name exists
    cur.execute('SELECT Name, Phone FROM Entries WHERE Name = ?', (name,))
    results = cur.fetchall()

    if not results:
        print("No entry found with that name.")
        conn.close()
        return

    print("\nCurrent entries for that name:")
    print(f"{'Name':25}Phone")
    print("-" * 40)
    for n, phone in results:
        print(f"{n:25}{phone}")

    new_phone = input("\nEnter the new phone number: ").strip()
    if not new_phone:
        print("Phone number cannot be empty.")
        conn.close()
        return

    cur.execute('UPDATE Entries SET Phone = ? WHERE Name = ?', (new_phone, name))
    conn.commit()

    print(f"Updated {cur.rowcount} row(s).")

    conn.close()

# ---------- DELETE FUNCTION ----------

def delete_entry():
    """Delete rows from the Entries table by name."""
    name = input("Enter the name of the entry to delete: ").strip()

    conn = get_connection()
    cur = conn.cursor()

    # Check if it exists
    cur.execute('SELECT Name, Phone FROM Entries WHERE Name = ?', (name,))
    results = cur.fetchall()

    if not results:
        print("No entry found with that name.")
        conn.close()
        return

    print("\nEntries that will be deleted:")
    print(f"{'Name':25}Phone")
    print("-" * 40)
    for n, phone in results:
        print(f"{n:25}{phone}")

    confirm = input("\nAre you sure you want to delete these row(s)? (y/n): ").lower()
    if confirm != 'y':
        print("Delete cancelled.")
        conn.close()
        return

    cur.execute('DELETE FROM Entries WHERE Name = ?', (name,))
    conn.commit()

    print(f"Deleted {cur.rowcount} row(s).")

    conn.close()

# ---------- MENU LOOP ----------

def main():
    while True:
        print("\nPhone Book Manager")
        print("1. Show all entries (READ)")
        print("2. Look up an entry (READ)")
        print("3. Update a phone number (UPDATE)")
        print("4. Delete an entry (DELETE)")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            show_all_entries()
        elif choice == '2':
            look_up_entry()
        elif choice == '3':
            update_entry()
        elif choice == '4':
            delete_entry()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

if __name__ == '__main__':
    main()