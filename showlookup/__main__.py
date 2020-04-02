from .events import *
from .model import *
from .plot import *

import click


@click.command()
@click.option("--id", prompt="Lookup ID", help="ID of the lookup instance to visualize.")
@click.argument('filename')
def view(filename, id):
    events = filter_lookup(load_file(filename), id)
    model = lookup_from_events(events)
    plot(model)


if __name__ == '__main__':
    view()
