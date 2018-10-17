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


# class SubForm(FlaskForm):
#     email = StringField('Your Email Address',validators=[Required(),Email()])
#     title = StringField('Entre Your Name' ,validators=[Required()])
#     submit = SubmitField('Subscribe')    

#     def validate_email(self,data_field):
#                 if Subscribe.query.filter_by(email =data_field.data).first():
#                     raise ValidationError('Sorry!, there is an account with that email')



# class LikeForm(FlaskForm):
#     '''
#     Class to create a wtf form for liking a blog
#     '''
#     submit = SubmitField('Like')