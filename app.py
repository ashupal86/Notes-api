import datetime
from flask import Flask,jsonify,redirect,url_for,session
from flask_session import Session
from models import db,add_note,update_notes,delete_note,fetch_notes,create,is_strong_password
from werkzeug.routing import BuildError



app=Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
app.config['SECRET_KEY']='this is my secret'

Session(app)

@app.route('/')
def index():
   
    return jsonify({"msg":"WELCOME TO PRIVATE NOTES API",
                    'registration':'/register/username/password/email to register',
                    'login':'/username/password to login',
                    'get notes':'/api_key/notes to get all notes',
                    'add notes':'/api_key/notes/add/body/pinned/title to add a note',
                    'update notes':'/api_key/notes/update/note_id/body/date/pinned/title to update a note',
                    'delete notes':'/api_key/notes/delete/note_id to delete a note'})

@app.route('/<api_key>/notes')
def all(api_key):
    if session.get('login'):
        res=fetch_notes(api_key)
        return jsonify(res)
    else:
        return jsonify({"msg":"Please login","use to login":'/username_here/password_here'})
    
@app.route('/<api_key>/notes/add/<body>/<pinned>/<title>')
def add(api_key,body:str,pinned:bool,title:str):
    if session.get('login'):
        res=add_note(api_key,body,pinned,title)
        if res:
            return jsonify({"msg":"Note added"})
        else:
            return jsonify({"msg":"Some error occured"})
        
    else:
        return jsonify({"msg":"Please login","login using":'/username_here/password_here'})
    
@app.route('/<api_key>/notes/update/<note_id>/<body>/<pinned>/<title>')
def update(api_key,note_id,body:str,pinned:bool,title:str,date:str=datetime.datetime.now()):
    if session.get('login'):
        res=update_notes(api_key,note_id,body,date,pinned,title)
        if res:
            return jsonify({"msg":"Note updated"})
        else:
            return jsonify({"msg":"Some error occured"})
    else:
        return jsonify({"msg":"Please login","login using":'/username_here/password_here'})
    
@app.route('/<api_key>/notes/delete/<note_id>')
def delete(api_key,note_id:str):
    if session.get('login'):
        res=delete_note(api_key,note_id)
        if res:
            return jsonify({"msg":"Note deleted"})
        else:
            return jsonify({"msg":"Some error occured"})
    else:
        return jsonify({"msg":"Please login","login using":'/username_here/password_here'})
    
    

@app.route('/register/<username>/<password>/<email>')
def register(username:str,password:str,email:str):
    try:
        if not is_strong_password(password):
            return jsonify({"msg":"Password is weak",'password should contain': '1 digit and length should be greater than 8'})
        DB=db()
        res=DB.insertdb(username,email,password)
        if res!="Username already exists":
            __api_key=DB.get_api_key(username,password)   
            if __api_key=="User not found":
            # (__api_key)  
                return jsonify({"msg":"User not found"})
                
            else:
                user=create(__api_key,username)
                if user:
                    return jsonify({"msg":"User created","api_key":__api_key,'username':username,'password':password,'email':email})
        else:
            return jsonify({"msg":"Username already exists"})
    except Exception as e:
        return jsonify({"msg":str(e)})
    

@app.route('/<username>/<password>')
def login(username:str,password:str): 
    try:
        DB=db()
        res=DB.validate(username,password)
        __api_key=DB.get_api_key(username,password)[0][0]
        if res:
            session['login']=True
            return jsonify({"msg":f"Hello {username} your api_key is '{__api_key}' use this api_key to access your notes","notes":f"/{__api_key}/notes"})
        else:
            return jsonify({"msg":"Invalid Credentials"})
    except BuildError as e:
        return jsonify({"msg":e})   

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=9999)

