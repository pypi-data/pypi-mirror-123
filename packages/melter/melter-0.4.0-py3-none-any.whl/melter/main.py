import typer

from melter import __version__, __title__

app = typer.Typer()


@app.callback()
def callback():
    """
    melter - Identifies which cases that should be analyzed again
    """

@app.command()
def version():
    """
    Print the version
    """
    typer.echo("%s, version %s" % (__title__, __version__))


@app.command("get-monitored-cases")
def get_monitored_cases():
    """
    Retrieve all monitored cases
    """
    typer.echo("Requesting cases marked for monitoring in scout")
