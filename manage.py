from flask.ext.script import Manager, Server, prompt_bool, prompt, prompt_pass

from ecahack import app, db
from ecahack.users.models import User
from ecahack.users.constants import ADMIN


manager = Manager(app)
manager.add_command('runserver', Server())


@manager.command
def create_db():
    """Creates database tables based on SQLAlchemy models"""

    db.create_all()
    print 'Database tables created.'

@manager.command
def create_admin():
    """Creates an admin for the app"""

    username = prompt('Enter admin username', default='admin')
    password = prompt_pass('Enter admin password', default='admin')

    user = User(rfid='00000000000000',
                username=username,
                password=password,
                role=ADMIN)
    db.session.add(user)
    db.session.commit()
    print 'Admin added.'

@manager.command
def drop_db():
    """Drops database tables"""

    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()
    print 'Database tables dropped.'

@manager.command
def recreate_db():
    """Drops database tables, creates them and prompts for an admin"""

    drop_db()
    create_db()
    create_admin()

@manager.command
def test():
    """Runs tests for application"""

    import nose

    nose.main(argv=[''])


if __name__ == '__main__':
    manager.run()
