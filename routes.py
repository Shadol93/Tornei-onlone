from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from .models import User, Game, Newsletter
from .forms import RegistrationForm, LoginForm

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Populate the games and newsletters choices
    form.games.choices = [(game.id, game.name) for game in Game.query.all()]
    form.newsletters.choices = [(newsletter.id, newsletter.name) for newsletter in Newsletter.query.all()]
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        
        # Add selected games and newsletters
        selected_games = Game.query.filter(Game.id.in_(form.games.data)).all()
        selected_newsletters = Newsletter.query.filter(Newsletter.id.in_(form.newsletters.data)).all()
        user.games = selected_games
        user.newsletters = selected_newsletters
        
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
        login_user(user, remember=True)
        return redirect(url_for('main.profile', username=user.username))
    return render_template('login.html', form=form)

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main
