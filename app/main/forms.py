from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,SelectField
from wtforms.validators import Required ,DataRequired

class ArticleForm(FlaskForm):
    title = StringField('Title')
    category = SelectField('Category', choices=[('Behavioral Psychology','Behavioral Psychology'),('Decision Making','Decision Making'),('Habits','Habits'),('Health','Health')])
    article = TextAreaField('Your Article')
    submit = SubmitField('Post')


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Say something about yourself')
    submit = SubmitField('Update')


class CommentForm(FlaskForm):
    comment = StringField('Write a comment')
    submit = SubmitField(('comment'))