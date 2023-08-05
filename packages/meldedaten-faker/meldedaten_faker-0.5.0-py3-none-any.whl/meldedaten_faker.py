import click
from app import application

@click.group()
def cli():
    pass

@cli.command()
@click.argument('records', type=int, default=1)
@click.argument('path', type=click.Path(exists=True))
def generate(records, path):
    """Generates fake census data"""
    application.generate(records, path)