import sys
import logging

logger = logging.getLogger('RUMMAGE')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)

logger.addHandler(ch)


def runserver():
    from api.app import create_app
    app = create_app()
    app.run(debug=False)


def populate():
    from utils import populate_db
    populate_db()


if __name__ == '__main__':
    commands = {
        'runserver': runserver,
        'populate': populate,
    }

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        command = commands.get(arg)
        if command:
            command()
        else:
            logger.warning('No such command found.')
