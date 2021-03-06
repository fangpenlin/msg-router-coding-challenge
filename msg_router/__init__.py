from __future__ import unicode_literals
import os

from pyramid.config import Configurator

from .settings import default_settings


def load_pkg_file(pkg_filename, filename, default):
    """Load file content under package folder

    """
    pkg_dir = os.path.dirname(pkg_filename)
    filepath = os.path.join(pkg_dir, filename)
    try:
        with open(filepath, 'rt') as pkg_file:
            return pkg_file.read().strip()
    except IOError:
        return default


__version__ = load_pkg_file(__file__, 'version.txt', '0.0.0')
__git_revision__ = load_pkg_file(__file__, 'git_revision.txt', 'Unknown')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.

    """
    app_settings = default_settings.copy()
    app_settings.update(settings)

    # setup database
    # app_settings = setup_database(global_config, **app_settings)
    config = Configurator(
        settings=app_settings,
    )
    # add api headers
    config.add_tween('.tweens.api_headers_tween_factory')
    # provides api views
    config.include('.api')
    # use our prettify json renderer
    config.include('.renderers')

    config.scan(categories=('pyramid', ))
    return config.make_wsgi_app()
