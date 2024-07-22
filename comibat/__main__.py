import click

from . import comibat

@click.group()
def cli():
    pass

cli.add_command(comibat.main)
