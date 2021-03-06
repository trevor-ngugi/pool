from flask import render_template,redirect,url_for,abort ,request #Takes in the name of the template.
from flask_login import login_required,current_user
from ..models import User,Book
from .. import db,photos
from . import main
from .forms import UpdateProfile,BookForm


from flask_bootstrap import Bootstrap

@main.route('/')
def index():
     

    return render_template ('index.html')

@main.route('/book',methods=['GET','POST'])
@login_required
def book():
    form=BookForm()
    if form.validate_on_submit():
        name=form.name.data
        tday=form.tday.data
        user_id=current_user

        new_book= Book(name=name,tday=tday,user_id=current_user._get_current_object().id)
        
        new_book.save_book()
        return redirect(url_for('main.index'))
    return render_template('book/book.html',form=form)

@main.route('/gallery')
@login_required
def gallery():

    return render_template('gallery.html')

@main.route('/about_us')
def about():

    return render_template('about-us.html')


# @main.route('/book')
# @login_required
# def book():

#     return render_template('book.html')

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))
