from . import db
from datetime import datetime
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import UserMixin 
from . import login_manager

class Admin (UserMixin , db.Model):
    __tablename__ = 'admin'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255) , unique = True , index = True )
    pass_secure = db.Column(db.String(255))
    bio = db.Column(db.String)
    profile_pic_path = db.Column(db.String())

    articles = db.relationship('Article',backref = 'author',lazy="dynamic")
    

    def __repr__(self):
        return f'User {self.username}'

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
        
    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def save_author(self):
        db.session.add(self)
        db.session.commit()


@login_manager.user_loader 
def load_user(user_id):
    return Admin.query.get(int(user_id))


'''
Article modelDUNCO
 . Defines our articles' table . Creates a relationship between the table and our Admin . 
We need a way to query authors' details . 
'''
class Article (db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String)
    article = db.Column(db.String)
    posted = db.Column(db.DateTime,index=True,default=datetime.utcnow)
    admin_id = db.Column(db.Integer,db.ForeignKey("admin.id"))
    category = db.Column(db.String)
    
    comments = db.relationship('Comment',backref = 'article',lazy="dynamic")

    def save_article(self):
        db.session.add(self)
        db.session.commit()


    def delete_article(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_articles(cls,id):
        articles = Article.query.filter_by(id = id).all()

        return articles

    @classmethod
    def fetch_by_category(cls,cat):
        articles = Article.query.filter_by(category = cat).all()

        return articles


'''
Comment model . Defining our comments' table . Linking comments table with articles, table . 
'''
class Comment (db.Model):
    __tablename__ = 'comments'

    id = db.Column (db.Integer , primary_key = True)
    comment = db.Column(db.String)
    article_id =  db.Column(db.Integer,db.ForeignKey("articles.id"))


    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    def delete_comment(self):
        db.session.delete(self)
        db.session.commit()

'''
We need to store subscribed readers into our database 
'''
class Subscriber(db.Model):
    __tablename__ = 'subscribers'

    id = db.Column (db.Integer , primary_key = True)
    email = db.Column(db.String(255) , unique = True , index = True )

    #  ********* saving to database new subscriber **********
    def new_reader(self):
        db.session.add(self)
        db.session.commit()

    # ***** querying all subscribers ***************
    @classmethod
    def fetch_readers(cls):
        readers = Subscriber.query.all()

        return readers