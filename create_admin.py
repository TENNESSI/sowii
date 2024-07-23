from app import User, db, app

with app.app_context():
	username = "superadmin"
	password = "stariybog2025"
	isadmin = True
	try:
		user = User(username=username, isadmin=isadmin)
		user.set_password(password)
		db.session.add(user)
		db.session.commit()
		print("успех")
	except Exception as e:
		print(f'Ошибка при регистрации пользователя: {e}')