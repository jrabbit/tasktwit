import os


def directory(name='tasktwit'):
    """Construct a directory from os name"""
    home = os.path.expanduser('~')
    if platform.system() == 'Linux':
        app_dir = os.path.join(home, '.' + name)
    elif platform.system() == 'Darwin':
        app_dir = os.path.join(home, 'Library', 'Application Support',
         name)
    elif platform.system() == 'Windows':
        app_dir = os.path.join(os.environ['appdata'], name)
    else:
        app_dir = os.path.join(home, '.' + name)
    if not os.path.isdir(app_dir):
        os.mkdir(app_dir)
    return app_dir
