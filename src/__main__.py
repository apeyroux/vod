import click
import sys

from . import app

@click.command()
@click.option('-l', '--listen', default='127.0.0.1', help="IP d'écoute")
@click.option('-p', '--port', default=5000, help="Port d'écoute")
@click.option('-d', '--debug', is_flag=True, default=False, help="Debug")
@click.option('-c', '--config', default="youtd.cfg", help="Fichier de configuration")
@click.option('--start', is_flag=True, default=False, help="Start web app")
@click.option('--initdb', is_flag=True, default=False,
              help="Initialisation de la base.")
def main(listen, port, debug, config, start, initdb):

    try:
        # app.config.from_pyfile(config)
        pass
    except Exception as ex:
        click.echo(ex)

    if debug:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.jinja_env.auto_reload = True

    if start:
        app.run(listen,
                port,
                debug=debug,
                use_debugger=debug,
                use_reloader=debug)

    return 0


if __name__ == "__main__":
    sys.exit(main())
