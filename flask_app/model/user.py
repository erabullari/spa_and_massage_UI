from flask import Flask ,flash,session
from flask_app.config.mysqlconnection import connectToMySQL
import re	   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db_name='login_and_registration'
    def __init__(self,data):
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName=data['lastName']
        self.email=data['email']
        self.password=data['password']
        
    

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db_name).query_db(query, data)
        
        if result and isinstance(result, list) and len(result) > 0:
            return cls(result[0])
        else:
            return None 

                
    @classmethod
    def save(cls,data):
        query="INSERT INTO users (firstName,lastName ,email,password,text,reservationTime,reservationDate) VALUES (%(firstName)s, %(lastName)s, %(email)s,%(password)s ,%(text)s ,%(reservationTime)s,%(reservationDate)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
     
    @classmethod
    def delete(cls,data):
        query="DELETE FROM users WHERE id= %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
# user detail
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return (result[0])



    @staticmethod
    def validateUser(user):
        is_valid=True
        if len(user['firstName'])<2:
            flash("Enter your name" , 'nameerror')
            is_valid=False
        if len(user['lastName'])<2:
            flash('Enter you last name' , 'lastnameerror')
            is_valid=False
        if len(user['password'])<7:
            flash('Enter 8 character for pasword' , 'password')
            is_valid=False

        if user['password'] != session['passwordConfirm']:
            flash('password does not match' , 'passwordmatch')
            is_valid=False

        if len(user['text'] )<5:
            flash("Please write you'r rezervation" , 'texterror')
            is_valid=False
                

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!" ,'emailerror')
            is_valid = False
        return is_valid