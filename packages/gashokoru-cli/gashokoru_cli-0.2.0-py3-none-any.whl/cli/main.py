import click

from .commands import workshop as _ws
from .commands import template as _tm

"""
    App entrypoint
"""
@click.group(
                # invoke_without_command=True
            )
def run():
    """Template generator CLI -- Made with 'Click'"""
    pass

"""
    commands.workshop group
"""
@run.group()
def workshop():
    pass

@workshop.command()
def create():
    """Launches a workshop creation tool on a local server"""
    _ws.create.create()

"""
    commands.template group
"""
@run.group()
def template():
    pass

@template.command()
def list():
    """Shows a list of all available templates"""
    _tm.list.list()

run()