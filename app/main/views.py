
from flask import render_template , request , redirect , url_for , abort , flash, render_template_string
from . import main 
import markdown2 

from flask_login import login_required , current_user
from .forms import ArticleForm , UpdateProfile, CommentForm
from ..models import Admin ,Article , Comment , Subscriber
from .. import db , photos
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

'''
This routing function fires moment the app loads. 
'''
@main.route('/' ,methods=["GET","POST"])
def index():

    return render_template('index.html')

'''
A view that redirects to new_article.html . Should the admin wish to add a new article . 

'''

@main.route('/new-article',methods=["GET","POST"])
@login_required
def new_article():

    form = ArticleForm()
    
    if form.validate_on_submit():
        article = Article(title = form.title.data , article=form.article.data, author = current_user,admin_id=current_user, category=form.category.data)

        article.save_article()

        flash('Your blog has been published!')

        return redirect(url_for('.index'))


    return render_template ('new_article.html' , form = form)

# @main.route('/new/comment')
# def new_comment():
    


'''
The following routes will query the database and return articles respective to the route . 
A reader doesn't need to be logged in to access this route . 
'''
@main.route('/Behavioral-Psychology')
def behave():

    articles = Article.fetch_by_category('Behavioral Psychology')

    return render_template ('articles.html', articles = articles , category = "Behavioral Psychology" )



@main.route('/Habits')
def habits():
    articles = Article.fetch_by_category('Habits')
    return render_template ('articles.html', articles = articles ,category = 'Habits' )


# @main.route('/Creativity')
# def creativity():
#     articles = Article.query.filter_by(category = 'Creativity').all()
#     return render_template ('articles.html', articles = articles , category = 'Creativity')


@main.route('/Health')
def health():
    articles = Article.fetch_by_category('Health')

    return render_template ('articles.html', articles = articles , category = 'Health' )


@main.route('/Decision-Making')
def decision():
    articles = Article.fetch_by_category('Decision Making ')
    return render_template ('articles.html' , articles = articles , category = "Decision Making")


'''
A route to display a single article . Queries by id and formats it html from markdown . 
'''
@main.route('/article/<int:id>',methods=["GET","POST"])
def single_article(id):

    comment = CommentForm()
    article=Article.query.get(id)
    comments = Comment.query.filter_by(article_id=id)
    # reader = request.args.get('reader')

    if comment.validate_on_submit():
        new_comment = Comment(comment = comment.comment.data ,article_id = id ,article = article )
        new_comment.save_comment()

        return redirect (url_for('.single_article',id=id))

    if article is None:
        abort(404)
    format_article = markdown2.markdown(article.article,extras=["code-friendly", "fenced-code-blocks"])

    return render_template('readmore.html',comment_form = comment,comments=comments, article = article, format_article=format_article)



'''
a route to add new subscribers to the database . 
'''
@main.route('/subscribed')
def subscriber():
    flash('Successfully subscribed to our newsletter !')

    email = request.args.get('subscriber')

    new_subscriber = Subscriber(email = email)
    new_subscriber.new_reader()

    return redirect (url_for('.index'))



'''
A route to redirect you to a user's profile
'''
@main.route('/user/<username>')
def profile(username):
    user = Admin.query.filter_by(username = username).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<username>/update', methods = ["POST","GET"])
def update_profile(username):
    user = Admin.query.filter_by(username = username).first()

    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data 

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', username = user.username))

    return render_template("profile/update_profile.html", form = form)



@main.route('/profile/<username>/pic/upload',methods =["POST","GET"])
def profile_pic(username):

    user = Admin.query.filter_by(username = username).first()

    if 'photos' in request.files:
        filename = photos.save(request.files['photos'])
        path = f"photos/{filename}"
        user.profile_pic_path = path
        db.session.commit()

    return redirect(url_for("main.profile",username=username))

'''
A route to delete an Article from a category
'''
@main.route('/article/delete/<int:id>')
def delete_article(id):
    article = Article.query.filter_by(id=id).first()
    article.delete_article()
    flash('Article successfully deleted !')

    return redirect(url_for('.index'))


'''
A route to delete comments from a particular blog
'''
@main.route('/comment/delete/<int:id>')
def delete_comment(id):

    comment = Comment.query.filter_by(id=id).first()
    article = Article.query.filter_by(id = comment.article_id).first()
    comment.delete_comment()
    flash('Comment successfully deleted !')

    return redirect(url_for('.single_article',id=article.id))