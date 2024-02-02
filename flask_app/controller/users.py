from flask_app import app
from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask_app.model.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def loginpage():
    return render_template('login.html')

@app.route('/register')
def registerPage():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    session['passwordConfirm'] = request.form['passwordConfirm']
    
    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    
    if not User.validateUser(request.form):
        return redirect('/register')
    
 
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'email': request.form['email'],
        'text': request.form['text'],
        'reservationDate':request.form['reservationDate'],
        'reservationTime':request.form['reservationTime'],
        'password': pw_hash
    }  
    
    user_in_db = User.get_by_email(data)

    if user_in_db and user_in_db.email == request.form['email']:
        flash("This email already exists", 'emailexist')
        return redirect(request.referrer)

  
    user_id = User.save(data)
    session['user_id'] = user_id
    
    return redirect('/userinfo/' + str(user_id))


@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)

    if not user_in_db:
        flash("Invalid Email", 'loginemailerror')
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password", 'loginpassworderror')
        return redirect('/login')
    
    session['user_id'] = user_in_db.id
    return redirect(url_for("personal_detail", id=user_in_db.id))


@app.route('/userinfo/<int:id>')
def personal_detail(id):
    if  'user_id'not in session:
        return redirect('/login')
    
    data = {
        'id': id
            
            }
    oneuser = User.get_one(data)
    return render_template('userinformation.html', oneuser=oneuser)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')  

@app.route('/deleteone/<int:id>')
def deleteone(id):
    data={
        'id':id
    }
    User.delete(data)
    return redirect('/')

