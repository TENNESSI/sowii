from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'login'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = 'secretkey'
db = SQLAlchemy(app)

class Player(db.Model):
	__tablename__ = 'players'
	id = db.Column(db.Integer(), primary_key=True)
	nickname = db.Column(db.String(30), nullable=True)
	mmr = db.Column(db.String(20), nullable=True)
	dotaid = db.Column(db.String(20), nullable=True)
	created_on = db.Column(db.DateTime(), default=datetime.utcnow)

	def __repr__(self):
		return "<{}:{}>".format(self.id, self.nickname)

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(63), index=True, unique=True)
	password_hash = db.Column(db.String(127))

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return '<{}:{}>'.format(self.id, self.username)

@login.user_loader
def load_user(id):
	return db.session.get(User, int(id))

@app.route('/')
@app.route('/index')
def index():
	players = Player.query.order_by(desc(Player.created_on)).all()
	return render_template('index.html', players=players)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/reg', methods=['POST', 'GET'])
def reg():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		password2 = request.form['password2']

		if password2 != password2:
			flash('Пароли не совпадают!!')
			return render_template('reg.html')

		try:
			user = User(username=username)
			user.set_password(password)
			db.session.add(user)
			db.session.commit()
		except Exception as e:
			flash(f'Ошибка при регистрации пользователя: {e}')
			return render_template('reg.html')
		else:
			login_user(user)
			return redirect('index')

	return render_template('reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	if request.method == 'POST':
		user = db.session.query(User).filter(User.username == request.form['username']).first()

		if user is not None:
			if not user.check_password(request.form['password']):
				flash('Пароль неверный')
				return render_template('login.html')

			login_user(user)
			return redirect(url_for('index'))
		else:
			flash('Пользователя не существует.')

	return render_template('login.html')

@app.route('/profile/<username>')
def profile(username: str):
	user = db.session.query(User).filter(User.username == username).first()

	if user is None:
		return redirect('index')

	players = db.session.query(Player).filter(Player.nickname == username).order_by(desc(Player.created_on)).all()

	return render_template('profile.html', username=username, players=players)

@app.route('/cup')
def cup():
	players = Player.query.order_by(desc(Player.created_on)).all()
	return render_template('cup.html', players=players)

@login_required
@app.route('/new', methods=['GET', 'POST'])
def new_player():
	if not current_user.is_authenticated:
		return redirect('login')

	if request.method == 'POST':
		nickname = request.form['nickname']
		mmr =  request.form['mmr']
		dotaid = request.form['dotaid']

		if len(nickname) > 0 and len(mmr) < 256 and len(mmr) > 0:
			player = Player(nickname=nickname, mmr=mmr, dotaid=dotaid)
			
			try:
				db.session.add(player)
				db.session.commit()
			except Exception as e:
				flash(f'Возникла ошибка при записи в базу данных: {e}')
			else:
				return redirect('index')
		else:
			flash('Ошибка, длина никнейма не соответствует стандартам.')
			return render_template('newplayer.html')

	return render_template('newplayer.html')

if __name__ == '__main__':
	app.run(debug=True, port=5000)