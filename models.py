import json
import datetime
import traceback
import os
import sqlite3
import hashlib


class db:
    def __init__(self) -> None:
        """
        Function to initialize the database
        """
        self.conn=sqlite3.connect('./users.db')
        self.conn.execute('CREATE TABLE  IF NOT EXISTS USERS (username TEXT NOT NULL PRIMARY KEY, email TEXT NOT NULL, pass TEXT NOT NULL,key TEXT)')
        self.conn.commit

    def insertdb(self,username:str,email:str,passw:str):
        """
        Function to insert the user in the database
        :param username: str
        :param email: str
        :param passw: str
        :return: str
        """
        try:
            if self.username_exists(username):
                return "Username already exists"
            import uuid
            __api_key=uuid.uuid4()
            
            self.conn.execute("INSERT INTO USERS(username,email,pass,key)values(?,?,?,?)",(username,email,hashlib.sha256(passw.encode()).hexdigest(),str(__api_key)))
            self.conn.commit()
            return "User added successfully"
        except Exception as e:
            (traceback.format_exc())
            return "Something went wrong"
        
    def validate(self,username:str,passw:str):
        """
        Function to validate the user for login
        :param username: str
        :param passw: str
        :return: bool
        """

        try:
            res=self.conn.execute("SELECT username,pass from USERS WHERE (username,pass)=(?,?) ",(username,hashlib.sha256(passw.encode()).hexdigest()))
            r=res.fetchall()

            if len(r)==0:
                return False
            return True
        except Exception as e:
            (traceback.format_exc())
            return False
        
    def get_api_key(self,username:str,passw:str):
        """
        Function to get the api key of the user
        :param username: str
        :return: str
        """
        try:
          
            res=self.conn.execute("SELECT key from USERS WHERE (username,pass)=(?,?)",(username,hashlib.sha256(passw.encode()).hexdigest()))
            
            r=res.fetchall()
            
            if len(r)==0:
                return "User not found"
            
            return r
        except Exception as e:
            
            return traceback.format_exc()
        
    def username_exists(self,username:str):
        """
        Function to check if the username exists
        :param username: str
        :return: bool
        """
        try:
            res=self.conn.execute("SELECT * from USERS WHERE username=?",(username,))
            r=res.fetchone()
            return r is not None
        except Exception as e:
            print(traceback.format_exc())
            return True
        






        
        
        
        
# DB=db()
# (DB)
# DB.insertdb('ashu','ashu@gmail.com','ashuashu')
# DB.insertdb('ashu1','ashu1@gmail.com','ashuashu1')
# DB.insertdb('ashu2','ashu2@gmail.com','ashuashu2')
# (DB.insertdb('ashu2','ashu2@gmail.com','ashuashu2'))


# (DB.get_api_key('ashu','ashuashu')[0][0])
# (hashlib.sha256('ashuashu'.encode()).hexdigest())



wdir=os.getcwd()

def create(api_key:str,username:str):
    """
    Create a new user
    :param api_key: str
    :param username: str
    :return: bool | exception

    """
    try:
        directory = './data'
    
    # Check if the directory exists, create it if it does not
        if not os.path.exists(directory):
            os.makedirs(directory)
    
        filepath = f"{directory}/{api_key[0][0]}.json"
        data = {
            "username": username,
            "notes": {
                "count": "0",
                "note": {}
            },
            "reminders": {
                "count": "0",
                "reminder": {}
            }
        }
        with open(filepath, 'a') as file:
            json.dump(data, file)
        return True
    except Exception as e:
        (traceback.format_exc())
        return False

# r=create('fa14263c-b79d-4fa7-a6e7-d8a5d1cd5565','ashu')
# (r)

def open_file(filename):
    """
    Open a file and return the contents
    :param filename: str
    :return: str
    """
    try:
        with open(f"./data/{filename}.json", 'r') as file:
            (file)
            return json.load(file)
    except Exception as e:
        (traceback.format_exc())
        return False
    


def save_file(filename,data):
    try:
        with open(f"./data/{filename}.json", 'w') as file:
            json.dump(data, file, indent=4)
        return True
    except Exception as e:
        return False,e
    

def add_note(api_key:str,body:str, pinned:bool=False, title:str = "Enter Title", date:str=datetime.datetime.now()):
    """
    Add a note to the notes file
    :param api_key: str
    :param body: str
    :param pinned: bool
    :param title: str
    :param date: str

    :return: bool | exception
    
    """
    try:
        notes = open_file(api_key)
        count=int(notes['notes']['count'])+1

        note = {

            'title': str(title),
            'body': str(body),
            'date': str(date),
            'pinned': str(pinned)

        }
        notes['notes']['note'][str(count)] = note
        notes['notes']['count'] = str(count)

        r=save_file(api_key,notes)
        # (r)
        return True
    except Exception as e:
        (traceback.format_exc()  )
        return False
    
# r=add_note('api_key',"hello world",pinned=True)
# (r)


def update_notes(api_key:str,note_id:str,body:str, date:str, pinned:bool=False, title:str = "Enter Title"):
    """
    Update a note in the notes file
    :param api_key: str
    :param note_id: str count
    :param body: str
    :param date: str
    :param pinned: bool
    :param title: str
    :return: bool | exception | str
    
    """
    try:
        notes = open_file(api_key)
        count=int(notes['notes']['count'])
        if int(note_id)>count:
            # (note_id,count)
            return "note not present"
        # note_id=notes['notes']['note'][note_id]
        # (note_id)
        else:
            note = {

            'title': str(title),
            'body': str(body),
            'date': str(date),
            'pinned': str(pinned),
            "last_change":str(datetime.datetime.now())

                }
            notes = open_file(api_key)
            notes['notes']['note'][note_id] = note
            
            r=save_file(api_key,notes)
            (r)
            return True
    except Exception as e:
        ("update notes :",traceback.format_exc())
        return False
    
# r=update_notes('api_key_here','3',"helo world","2024-06-21 14:56:32.215340",pinned=True)
# (r)


def delete_note(api_key:str,note_id:str):
    """
    Delete a note in the notes file
    :param api_key: str
    :param note_id: str count
    :return: bool | exception | str
    
    """
    try:
        notes = open_file(api_key)
        count=int(notes['notes']['count'])
        if int(note_id)>count:
            return "note not present"
        else:
            notes['notes']['note'].pop(note_id)
            notes['notes']['count'] = str(int(notes['notes']['count'])-1)
            r=save_file(api_key,notes)
            return True
    except Exception as e:
        ("delete notes :",traceback.format_exc())
        return False
    
# r=delete_notes('api_key_here','3')
# (r)

def fetch_notes(api_key:str):
    """
    Fetch all notes in the notes file
    :param api_key: str
    :return: dict | exception
    
    """
    try:
        notes = open_file(api_key)
        (notes)
        note=notes['notes']['note']
        return note
    except Exception as e:
        ("fetch notes :",traceback.format_exc())
        return False

# r=fetch_notes('api_key_here')
# (r)


def is_strong_password(password):
    import re
    # Minimum length of 8 characters
    if len(password) < 8:
        return False



    # At least one digit
    if not re.search(r'\d', password):
        return False

    # If all conditions are met
    return True