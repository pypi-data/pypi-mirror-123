import os

from dotenv import load_dotenv
from commands.cli import cli


# load env
load_dotenv(os.path.join(os.getcwd(), './.secret/.env'))


if __name__ == '__main__':
    cli()
