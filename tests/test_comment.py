from app.models import Comment,Admin
from app import db
import unittest

class CommentTest(unittest.TestCase):
    '''
    Test Class to test the behaviour of the blog class
    '''
    def setUp(self):
        self.admin_Dunco = Admin(username = 'Dunco',password = 'dunco', email = 'aruncodunco@gmail.com')
        self.new_comment = Comment(blog_id=12345,blog_title='Review for movies',image_path="https://image.tmdb.org/t/p/w500/jdjdjdjn",movie_review='best series ever watched',admin = self.user_Dunco ) 

    def tearDown(self):
        Comment.query.delete()
        Admin.query.delete()

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.blog_id,12345)
        self.assertEquals(self.new_comment.blog_title,'Review for movies')
        self.assertEquals(self.new_comment.image_path,"https://image.tmdb.org/t/p/w500/jdjdjdjn")
        self.assertEquals(self.new_comment.blog_comment,'one of the best blogs')
        self.assertEquals(self.new_comment.user,self.user_Dunco) 

    def test_save_comment(self): 
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_get_comment_by_id(self):

        self.new_comment.save_comment()
        got_comments = Comment.get_comments(12345)
        self.assertTrue(len(got_comments) == 1)
