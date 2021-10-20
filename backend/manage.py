import os
from app import create_app, db
from app.models import User, Post, Comment
from flask_script import Server, Shell, Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.environ.get('FLASK_CONFIG') or 'default')

manager = Manager(app)

def make_shell_context():
    return dict(api=app, db=db, User=User, Post=Post, Comment=Comment)

migrate = Migrate()
migrate.init_app(app)

port = int(os.environ.get('PORT', 5000))
server = Server(port=port)

manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('runserver', server)

@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    manager.run()