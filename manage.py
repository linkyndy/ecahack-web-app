from flask.ext.script import Manager, Server, prompt_bool

from ecahack import app, db


manager = Manager(app)
manager.add_command('runserver', Server())


@manager.command
def create_db():
    """Creates database tables based on SQLAlchemy models"""

    db.create_all()

@manager.command
def drop_db():
    """Drops database tables"""

    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()

@manager.command
def test():
    """Runs tests for application"""

    import nose

    nose.main(argv=[''])


if __name__ == '__main__':
    manager.run()
