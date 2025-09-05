from FlaskMIS import app, db

with app.app_context():
    db.create_all()
    print("✅ Tables created in PostgreSQL")
