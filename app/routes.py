from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm,ContactForm, PostForm, RegionForm, CVReviewForm, SOPReviewForm
from flask_login import logout_user, login_required, login_user
from app.models import User, Region, Post, Service, cv_uploads, sop_uploads
from app import db


@app.route('/')
@app.route('/home')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        if user.email == 'okpegodwinfather@gmail.com':
            user.role = 'admin'
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required 
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)

@app.route('/services', methods=['GET', 'POST'])
def services():
    return render_template('services.html')

@app.route('/resources')
@login_required
def resources():
    return render_template('resources.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('contact.html', form=form)

@app.route('/region', methods=['GET', 'POST'])
def region():
    form = RegionForm()
    if form.validate_on_submit():
        region = Region(name=form.name.data)
        db.session.add(region)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('region.html', form=form)

@app.route('/posts', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    form.region.choices = [(region.id, region.name) for region in Region.query.all()]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            description=form.description.data,
            requirement=form.requirement.data,
            benefit=form.benefit.data,
            deadline=form.deadline.data,
            how_to_apply=form.how_to_apply.data,
            region_id=form.region.data
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

@app.route('/cv_review', methods=['GET', 'POST'])
@login_required
def cv_review():
    form = CVReviewForm()
    if form.validate_on_submit():
        cv_filename = secure_filename(form.cv.data.filename)
        cv_path = cv.uploads.save(form.cv.data)
        service = Service(
            user_id=current_user.id,
            cv=cv_filename,
            name=form.name.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('home'))
    return render_template('cv_review.html', form=form)

@app.route('/sop_review', methods=['GET', 'POST'])
@login_required
def sop_review():
    form = SOPReviewForm()
    print('gotten')
    if form.validate_on_submit():
        sop_filename = secure_filename(form.sop.data.filename)
        sop_path = sop.uploads.save(form.sop.data)
        service = Service(
            user_id=current_user.id,
            sop=sop_filename,
            name=form.name.data
        )
        print('got here')
        db.session.add(service)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('home'))
    return render_template('sop_review.html', form=form)

