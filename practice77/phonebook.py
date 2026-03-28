import psycopg2
import csv

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='@qWerty1234',
    host='localhost',
    port='5432'
)

cur = conn.cursor()

def insert_contact():
    name = input('Name: ')
    phone = input('Phone: ')
    cur.execute('INSERT INTO phonebook(name, phone) VALUES (%s, %s)', (name, phone))
    conn.commit()
    print('Added!')


def insert_from_csv():
    with open('contacts.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            cur.execute('INSERT INTO phonebook(name, phone) VALUES (%s, %s)', (row[0], row[1]))
    conn.commit()
    print('CSV uploaded!')

def show_contacts():
    cur.execute('SELECT * FROM phonebook')
    for row in cur.fetchall():
        print(row)

def search():
    key = input('Enter name or phone number: ')
    cur.execute('SELECT * FROM phonebook WHERE name LIKE %s OR phone LIKE %s', (f"%{key}%", f"%{key}%"))
    results = cur.fetchall()
    if results:
        for row in results:
            print(row)
    else:
        print('No contacts found.')


def update():
    name = input('Who to update: ')
    new_phone = input('New phone: ')
    cur.execute('UPDATE phonebook SET phone=%s WHERE name=%s', (new_phone, name))
    conn.commit()
    print('Updated!')


def delete():
    name = input('Who to delete: ')
    cur.execute('DELETE FROM phonebook WHERE name=%s', (name,))
    conn.commit()
    print('Deleted!')


while True:
    print("\n1-Add\n2-From CSV\n3-Show\n4-Search\n5-Update\n6-Delete\n7-Exit")
    choice = input('Choice: ')

    if choice == '1':
        insert_contact()
    elif choice == '2':
        insert_from_csv()
    elif choice == '3':
        show_contacts()
    elif choice == '4':
        search()
    elif choice == '5':
        update()
    elif choice == '6':
        delete()
    elif choice == '7':
        break
    else:
        print('Something went wrong! Please, try again with numbers 1-7.')

cur.close()
conn.close()