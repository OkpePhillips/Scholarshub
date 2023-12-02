from flask import render_template, flash, redirect, url_for, request, send_from_directory
from app import app
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm,ContactForm, PostForm, RegionForm, CVReviewForm, SOPReviewForm, SearchForm, ResourcesForm
from flask_login import logout_user, login_required, login_user, current_user
from app.models import User, Region, Post, Service, Resources, cv_uploads, sop_uploads, resource_uploads
from sqlalchemy import or_
from app import db


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = SearchForm()
    regions = Region.query.all()
    if request.method == 'POST':
        if form.validate_on_submit():
            search_query = form.search_query.data
            posts = Post.query.filter(
            or_(
                    Post.title.ilike(f"%{search_query}%"),
                    Post.description.ilike(f"%{search_query}%"),
                    Post.region.has(Region.name.ilike(f"%{search_query}%")),
                    Post.benefit.ilike(f"%{search_query}%"),
                    Post.requirement.ilike(f"%{search_query}%"),
                    Post.deadline.ilike(f"%{search_query}%"),
                )
            ).all()
            return render_template('home.html', posts=posts, form=form, regions=regions)
    else:
        posts = Post.query.all()
        return render_template('home.html', posts=posts, form=form, regions=regions)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
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
        cv_path = cv_uploads.save(form.cv.data)
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
    if form.validate_on_submit():
        sop_filename = secure_filename(form.sop.data.filename)
        sop_path = sop_uploads.save(form.sop.data)
        service = Service(
            user_id=current_user.id,
            sop=sop_filename,
            name=form.name.data
        )
        db.session.add(service)
        db.session.commit()
        flash('Service request submitted successfully!')
        return redirect(url_for('home'))
    return render_template('sop_review.html', form=form)

@app.route('/resources', methods=['GET', 'POST'])
@login_required
def resource_upload():
    form = ResourcesForm()
    if form.validate_on_submit():
        resource_filename = secure_filename(form.resource.data.filename)
        file_path = resource_uploads.save(form.resource.data)
        resource = Resources(
            user_id=current_user.id,
            resource=resource_filename,
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(resource)
        db.session.commit()
        flash('Resource uploaded successfully!')
        return redirect(url_for('home'))
    return render_template('resource_upload.html', form=form)

@app.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@app.route('/posts/<region_name>')
def posts_by_region(region_name):
    region = Region.query.filter_by(name=region_name).first()
    if region:
        posts = Post.query.filter_by(region_id=region.id).all()
        return render_template('posts_by_region.html', posts=posts)