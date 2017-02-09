'''new reddit stuff'''

from controller import Controller


def build():
    '''start the build process'''
    controller = Controller()
    controller.build()
    controller.display_db()

build()
