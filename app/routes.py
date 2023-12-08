from flask import render_template, flash, redirect, url_for, request, send_from_directory, send_file, abort
from app import app, mail
from werkzeug.utils import secure_filename
from app.forms import LoginForm, RegistrationForm,ContactForm, PostForm, RegionForm, CVReviewForm, SOPReviewForm, SearchForm, ResourcesForm, EditPostForm, EditProfileForm, ReviewedForm
from flask_login import logout_user, login_required, login_user, current_user
from app.models import User, Region, Post, Service, Resources, cv_uploads, sop_uploads, resource_uploads, reviewed_uploads
from sqlalchemy import or_
from app import db
import os
from flask_mail import Message


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
    services = Service.query.filter_by(user_id=user.id).all()
    return render_template('user.html', user=user, services=services)

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
        email_sender = form.email.data
        msg = Message(form.subject.data,
                      sender='okpegodwinfather@gmail.com',
                      recipients=['okpegodwin18@yahoo.com'])
        msg.body = f"Name: {form.email.data}\nSubject: {form.email.data}\nMessage:\n{form.message.data}"
        
        try:
            mail.send(msg)
            flash('Your message has been sent. Thank you!')
            return redirect(url_for('home'))
        except Exception as e:
            flash(f'Error: {e}', 'error')
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
            link=form.link.data,
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

@app.route('/resource_upload', methods=['GET', 'POST'])
@login_required
def resource_upload():
    form = ResourcesForm()
    if form.validate_on_submit():
        resource_filename = secure_filename(form.resource.data.filename)
        file_path = resource_uploads.save(form.resource.data)
        resource = Resources(
            user_id=current_user.id,
            resource=file_path,
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

@app.route('/resources')
@login_required
def resources():
    resources = Resources.query.all()
    return render_template('resources.html', resources=resources)

@app.route('/download_resource/<int:resource_id>')
@login_required
def download_resource(resource_id):
    resource = Resources.query.get_or_404(resource_id)
    base_directory = 'C:\\Users\\APINPC\\Desktop\\scholarshub\\uploads'
    file_path = os.path.join(base_directory, 'resource', resource.resource)
    return send_file(file_path, as_attachment=True)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.set_password(form.password.data)
        db.session.commit()
        
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user'))
    elif request.method == 'GET':
        form.email.data = current_user.email
    return render_template('edit_profile.html', form=form)

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    users = User.query.all()
    posts = Post.query.all()
    services = Service.query.all()
    posts_count = 0
    users_count = 0
    services_count = 0

    for user in users:
        users_count += 1

    for post in posts:
        posts_count += 1

    for service in services:
        services_count += 1
    
    return render_template('admin_dashboard.html', users_count=users_count, posts_count=posts_count, services_count=services_count)

@app.route('/admin/view_users')
@login_required
def view_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('view_users'))

@app.route('/admin/view_services')
@login_required
def all_services():
    services = Service.query.all()
    return render_template('admin_services.html', services=services)

@app.route('/admin/view_users')
@login_required
def all_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/admin/delete_posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EditPostForm()
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted successfully!')
        return redirect(url_for('home'))
    return render_template('delete_post.html', post=post, form=form)

@app.route('/admin/posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = EditPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.requirement = form.requirement.data
        post.benefit = form.benefit.data
        post.deadline = form.deadline.data
        post.how_to_apply = form.how_to_apply.data
        post.link = form.link.data
        db.session.commit()

        flash('Your profile has been updated!', 'success')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.requirement.data = post.requirement
        form.benefit.data = post.benefit
        form.deadline.data = post.deadline
        form.how_to_apply.data = post.how_to_apply
        form.link.data = post.link
    return render_template('edit_post.html', form=form)


@app.route('/admin/upload_reviewed/<int:user_id>/<int:service_id>', methods=['GET', 'POST'])
@login_required
def upload_reviewed_cv(user_id, service_id):
    if not current_user.is_admin():
        abort(403) 
    user = User.query.get_or_404(user_id)
    service = Service.query.get_or_404(service_id)
    username = user.username
    form = ReviewedForm()

    if form.validate_on_submit():
        file_path = reviewed_uploads.save(form.reviewed.data)
        service.reviewed_file = file_path
        service.status = "Completed"
        db.session.commit()

        flash('Reviewed CV uploaded successfully!')
        return redirect(url_for('user', username=username))

    return render_template('upload_reviewed_cv.html', form=form, user=user)

@app.route('/download_reviewed/<int:user_id>/<int:service_id>')
@login_required
def download_reviewed(user_id, service_id):
    user = User.query.get_or_404(user_id)
    service = Service.query.filter_by(user_id=user_id, id=service_id).first()

    if not service or not service.reviewed_file:
        abort(404)

    base_directory = 'C:\\Users\\APINPC\\Desktop\\scholarshub\\uploads'
    file_path = os.path.join(base_directory, 'reviewed', service.reviewed_file)
    return send_file(file_path, as_attachment=True)

@app.route('/subscribe', methods=['GET', 'POST'])
def subscribe():
    form = SubscriptionForm()

    if form.validate_on_submit():
        email = form.email.data
    
        if Subscription.query.filter_by(email=email).first():
            flash('You are already subscribed!', 'info')
        else:
            new_subscription = Subscription(email=email)
            db.session.add(new_subscription)
            db.session.commit()

            send_confirmation_email(email)

            flash('Subscription successful! Check your email for confirmation.', 'success')

        return redirect(url_for('home'))

    return render_template('home.html', form=form)