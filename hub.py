from app import app, db
from app.models import User, Post, Region, Service

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Region': Region, 'Service': Service}

if __name__ == '__main__':
    app.run(threaded=True, debug=True)