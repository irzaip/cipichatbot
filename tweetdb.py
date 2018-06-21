import sqlite3



# Create a database in RAM
db = sqlite3.connect(':memory:')
# Creates or opens a file called mydb with a SQLite3 DB
db = sqlite3.connect('mydb-tweet')

# Get a cursor object
#cursor = db.cursor()
#cursor.execute('''
#    CREATE TABLE following(id INTEGER PRIMARY KEY, username TEXT,
#                       following TEXT)
#''')
#db.commit()

def db_insert_follower(username, follower_list):
    cursor = db.cursor()
    # Insert user 1
    for i in range(len(follower_list)):
        follower=follower_list[i]
        cursor.execute('''INSERT INTO follower(username, follower)
                          VALUES(?,?)''', (username, follower))
    db.commit()
    
def db_insert_following(username, following_list):
    cursor = db.cursor()
    # Insert user 1
    for i in range(len(following_list)):
        following=following_list[i]
        cursor.execute('''INSERT INTO following(username, following)
                          VALUES(?,?)''', (username, following))
    db.commit()

def db_get_follower(username):
    cursor = db.cursor()
    cursor.execute('''SELECT username, follower FROM follower WHERE username=?''',(username,))
    #user1 = cursor.fetchone() #retrieve the first row
    #print(user1[1]) #Print the first column retrieved(user's name)
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}'.format(row[0], row[1]))

def db_get_following(username):
    cursor = db.cursor()
    cursor.execute('''SELECT username, following FROM following WHERE username=?''',(username,))
    #user1 = cursor.fetchone() #retrieve the first row
    #print(user1[1]) #Print the first column retrieved(user's name)
    all_rows = cursor.fetchall()
    for row in all_rows:
        # row[0] returns the first column in the query (name), row[1] returns email column.
        print('{0} : {1}'.format(row[0], row[1]))

def update():
    # Update user with id 1
    newphone = '3113093164'
    userid = 1
    cursor.execute('''UPDATE users SET phone = ? WHERE id = ? ''',
     (newphone, userid))

def db_del_follower(username):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM follower WHERE username = ? ''', (username,))
    db.commit()

def db_del_following(username):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM following WHERE username = ? ''', (username,))
    db.commit()

def db_is_replied(msg_id):
    cursor = db.cursor()
    cursor.execute('''SELECT msg_id, my_id FROM replymsg WHERE msg_id=?''',(msg_id,))
    msg1 = cursor.fetchone() #retrieve the first row
    if msg1:
        return True
    else:
        return False

def db_user_follower_data(user_id):
    cursor = db.cursor()
    cursor.execute('''SELECT follower FROM follower WHERE username=?''',(user_id,))
    msg1 = cursor.fetchone() #retrieve the first row
    if msg1:
        return True
    else:
        return False

def db_user_following_data(user_id):
    cursor = db.cursor()
    cursor.execute('''SELECT following FROM following WHERE username=?''',(user_id,))
    msg1 = cursor.fetchone() #retrieve the first row
    if msg1:
        return True
    else:
        return False

def db_replied_this_id(msg_id,my_id):
    cursor = db.cursor()
    cursor.execute('''INSERT INTO replymsg(msg_id,my_id)
                    VALUES(?,?)''',(msg_id,my_id))
    db.commit()
