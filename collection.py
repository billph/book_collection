from app import create_app, db
from app.models import User, Book, User_Book, Friendship

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, "Book": Book, "User_Book": User_Book, "Friendship": Friendship}