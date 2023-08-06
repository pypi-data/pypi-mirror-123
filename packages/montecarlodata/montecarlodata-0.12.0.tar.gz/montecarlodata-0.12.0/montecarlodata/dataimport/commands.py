import click

from montecarlodata.dataimport.dbt import DbtImportService


@click.group(help='Import data.', name='import')
def import_subcommand():
    """
    Group for any import related subcommands
    """
    pass

@import_subcommand.command(help='Import DBT manifest.')
@click.option('--dbt-manifest-file', required=True, help='Path to DBT manifest.json.', type=click.Path(exists=True))
@click.pass_obj
def dbt_manifest(ctx, dbt_manifest_file):
    DbtImportService(config=ctx['config'], dbt_manifest_file=dbt_manifest_file).import_dbt_manifest()