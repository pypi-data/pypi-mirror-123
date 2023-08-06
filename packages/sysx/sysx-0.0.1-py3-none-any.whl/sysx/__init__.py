import click
import time


@click.group()
def cli():
    pass


@click.command()
def deploy():
    pass


cli.add_command(deploy)
