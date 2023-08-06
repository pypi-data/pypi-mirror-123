import click

from melter import __version__, __title__

VERSION = __version__


@click.group(invoke_without_command=True)
@click.version_option(__version__, prog_name=__title__)
def base():
    print("Running melter, version %s" % VERSION)

if __name__ == '__main__':
    base()
