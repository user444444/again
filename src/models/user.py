from flask import session

from src.common.database import Database
import uuid
#import bcrypt
from src.models.utils import Utils

class User(object):
    def __init__(self,email,password,_id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id==None else _id

    @classmethod
    def get_by_email(cls,email):
        data = Database.find_one("users",{"email":email})
        if data is not None:
            return cls(**data)

    #Somewhere here you would also need to call Employee class

    @staticmethod
    def user_exists(email):
        if Database.find(collection="users",query={"email":email}).count() == 0:
            return False

    @classmethod
    def get_by_id(cls,_id):
        data = Database.find_one("users", {"_id": _id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,pass_prov):
        #static so that we can say User.login_valid("given_email","1234")
        user = User.get_by_email(email)
        if user is not None:
            pass_in_db = user.password#act pass provided by the user
            print("RIGHTY")
            print(pass_in_db)

            #return (bcrypt.hashpw(pass_prov.encode('utf-8'),pass_in_db)== pass_in_db)
            #return bcrypt.checkpw(pass_prov.encode('utf8'),pass_in_db)
            #return pass_prov==pass_in_db
            return Utils.check_hashed_password(pass_prov,pass_in_db)

            #pass_correct_hashed = bcrypt.hashpw(pass_prov,bcrypt.gensalt())
            #print("I am here and its bad ")
            #print(pass_correct_hashed == pass_prov)
            #print(pass_correct_hashed)
            #print(pass_prov)
            #return pass_correct_hashed==pass_prov
        else:
            return False

    @staticmethod
    def register(email,password):
        user = User.get_by_email(email)
        if user is not None:
            return False
        else:
            hashed_password = Utils.hash_password(password)
            #hashed_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
            new_usr = User(email,hashed_password)
            new_usr.save_to_mongo()
            session['email']=email
            return True
    @staticmethod
    def login(user_email):
        #login_valid has already been called
        session['email'] = user_email

    @staticmethod
    def logout(email):
        session[email] = None


    def json(self):
        return{
            "email":self.email,
            "_id":self._id,
            "password":self.password
        }



    def save_to_mongo(self):
        Database.insert("users",self.json())

    """
    def get_blogs(self):
        return Blog.find_by_author_id(self._id)
        
    
    def new_blog(self,title,description):
        blog = Blog(author=self.email,
                    title=title,
                    description = description,
                    author_id=self._id)
        blog.save_to_mongo()
        
    
    def new_post(self,blog_id,title,content):
        blog = Blog.get_from_mongo(blog_id)
        blog.new_post(title=title,
                      content =content) 
        
        
    """

