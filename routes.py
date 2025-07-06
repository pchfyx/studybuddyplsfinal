from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, User, StudyGroup, StudyMaterial, GroupPost
import os
from datetime import datetime

# Blueprint definitions
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
groups = Blueprint('groups', __name__)

# Main routes
@main.route('/')
def home():
    return render_template('home.html')

# Authentication routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=remember)
        return redirect(url_for('main.home'))
    
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

# Study group routes
@groups.route('/groups')
@login_required
def all_groups():
    search_query = request.args.get('search', '').strip().lower()
    filter_type = request.args.get('filter', 'all')
    created_groups = current_user.created_groups
    joined_groups = current_user.joined_groups
    if filter_type == 'created':
        groups = created_groups
    elif filter_type == 'joined':
        groups = joined_groups
    else:
        groups = list(set(created_groups + joined_groups))
    if search_query:
        groups = [g for g in groups if search_query in g.name.lower() or search_query in g.subject.lower()]
    return render_template('groups.html', groups=groups, search_query=search_query, filter_type=filter_type)

@groups.route('/groups/create', methods=['GET', 'POST'])
@login_required
def create_group():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        subject = request.form.get('subject')
        
        if not name or not subject:
            flash('Group name and subject are required!')
            return redirect(url_for('groups.create_group'))
        
        new_group = StudyGroup(
            name=name,
            description=description,
            subject=subject,
            creator_id=current_user.id
        )
        
        # Add user as both creator and member
        new_group.members.append(current_user)
        
        db.session.add(new_group)
        db.session.commit()
        
        return redirect(url_for('groups.view_group', group_id=new_group.id))
    
    return render_template('create_group.html')

@groups.route('/groups/<int:group_id>')
@login_required
def view_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    
    # Check if user is a member
    if current_user not in group.members and current_user.id != group.creator_id:
        flash('You are not a member of this group')
        return redirect(url_for('groups.all_groups'))
    
    return render_template('group.html', group=group)

@groups.route('/groups/<int:group_id>/invite')
@login_required
def invite_link(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    return render_template('invite.html', group=group)

@groups.route('/groups/<int:group_id>/join')
@login_required
def join_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    
    if current_user in group.members:
        flash('You are already a member of this group')
    else:
        group.members.append(current_user)
        db.session.commit()
        flash(f'You have joined {group.name}')
    
    return redirect(url_for('groups.view_group', group_id=group.id))

@groups.route('/groups/<int:group_id>/leave', methods=['POST'])
@login_required
def leave_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    # Don't allow the creator to leave their own group
    if current_user.id == group.creator_id:
        flash("You can't leave a group you created.")
        return redirect(url_for('groups.view_group', group_id=group_id))
    if current_user in group.members:
        group.members.remove(current_user)
        db.session.commit()
        flash('You have left the group.')
    else:
        flash('You are not a member of this group.')
    return redirect(url_for('groups.all_groups'))

@groups.route('/groups/<int:group_id>/delete', methods=['POST'])
@login_required
def delete_group(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    if current_user.id != group.creator_id:
        flash('Only the group creator can delete this group.')
        return redirect(url_for('groups.view_group', group_id=group.id))
    # Delete related materials and posts first (to prevent foreign key issues)
    StudyMaterial.query.filter_by(group_id=group.id).delete()
    GroupPost.query.filter_by(group_id=group.id).delete()
    db.session.delete(group)
    db.session.commit()
    flash('Group deleted successfully.')
    return redirect(url_for('groups.all_groups'))

@groups.route('/groups/<int:group_id>/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(group_id, post_id):
    post = GroupPost.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash("You can only edit your own posts.")
        return redirect(url_for('groups.view_group', group_id=group_id))
    if request.method == 'POST':
        new_content = request.form.get('content')
        if new_content:
            post.content = new_content
            db.session.commit()
            flash("Post updated successfully.")
            return redirect(url_for('groups.view_group', group_id=group_id))
        else:
            flash("Post content cannot be empty.")
    return render_template('edit_post.html', post=post, group_id=group_id)

@groups.route('/groups/<int:group_id>/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(group_id, post_id):
    post = GroupPost.query.get_or_404(post_id)
    if post.author_id != current_user.id:
        flash("You can only delete your own posts.")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted.")
    return redirect(url_for('groups.view_group', group_id=group_id))

@groups.route('/groups/<int:group_id>/upload', methods=['POST'])
@login_required
def upload_material(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    # Ensure user is a member
    if current_user not in group.members:
        flash('You are not a member of this group.')
        return redirect(url_for('groups.view_group', group_id=group_id))
    file = request.files.get('material')
    if file:
        filename = secure_filename(file.filename)
        upload_dir = os.path.join('static', 'uploads', str(group_id))
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        material = StudyMaterial(
            filename=filename,
            filepath=filepath,
            group_id=group.id,
            uploader_id=current_user.id
        )
        db.session.add(material)
        db.session.commit()
        flash('File uploaded successfully!')
    else:
        flash('No file selected.')
    return redirect(url_for('groups.view_group', group_id=group_id))

@groups.route('/groups/<int:group_id>/post', methods=['POST'])
@login_required
def add_post(group_id):
    group = StudyGroup.query.get_or_404(group_id)
    # Check if user is a member
    if current_user not in group.members and current_user.id != group.creator_id:
        flash('You are not a member of this group')
        return redirect(url_for('groups.all_groups'))
    content = request.form.get('content')
    if not content:
        flash('Post content cannot be empty.')
        return redirect(url_for('groups.view_group', group_id=group_id))
    new_post = GroupPost(
        content=content,
        group_id=group.id,
        author_id=current_user.id
    )
    db.session.add(new_post)
    db.session.commit()
    flash('Post added successfully!')
    return redirect(url_for('groups.view_group', group_id=group_id))