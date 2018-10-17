#  here is where you will be able to be redirected to the page you are looking for instead you mispelled something 



from flask import render_template
from . import main

@main.app_errorhandler(404)
def four04(error):
    '''
    Function to render the 404 error page
    '''
    return render_template('four04.html'),404