import click
from .core import FeastSchema

@click.group()
def cli():
    pass

@cli.command()
@click.argument("path", type=click.STRING, required=False)
@click.argument("skip_meta", type=click.BOOL, required=False)
@click.argument("feature_table", type=click.STRING, required=False)
def show(path: str = ".", skip_meta: bool = False, feature_table: str = None):
    if feature_table:
        FeastSchema(path).show_table_schema(feature_table,skip_meta)
    else:
        FeastSchema(path).show_schema(skip_meta)

if __name__ == "__main__":
    cli()


