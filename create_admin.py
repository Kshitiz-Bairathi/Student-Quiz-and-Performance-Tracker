from FlaskMIS import app, db, bcrypt
from FlaskMIS.models import Admins

with app.app_context():
    pw = bcrypt.generate_password_hash("Bairathi").decode("utf-8")
    admin = Admins(username="Kshitiz", password=pw)

    db.session.add(admin)
    db.session.commit()
    print("✅ Admin created: username=admin, password=admin123")
