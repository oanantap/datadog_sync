import click
from services.datadog_service import DatadogService
from config.config import SOURCE_API_KEY, SOURCE_APPLICATION_KEY


@click.group()
def cli():
    pass


@click.command()
@click.option('--source-url', required=True, help='The source URL for importing synthetic tests.')
@click.option('--destination-url', required=True, help='The destination URL for importing synthetic tests.')
def import_tests(source_url, destination_url):
    source_config = {
        'api_key': SOURCE_API_KEY,
        'app_key': SOURCE_APPLICATION_KEY,
        'source_url': source_url,
        'destination_url': destination_url
    }
    datadog_service = DatadogService(source_config)
    datadog_service.import_synthetic_tests()


@click.command()
@click.option('--source-url', required=True, help='The source URL for importing synthetic tests.')
@click.option('--destination-url', required=True, help='The destination URL for exporting synthetic tests.')
def export_tests(source_url, destination_url):
    source_config = {
        'api_key': SOURCE_API_KEY,
        'app_key': SOURCE_APPLICATION_KEY,
        'source_url': source_url,
        'destination_url': destination_url
    }
    datadog_service = DatadogService(source_config)
    datadog_service.export_synthetic_tests()


cli.add_command(import_tests)
cli.add_command(export_tests)

if __name__ == "__main__":
    """
    datadog_sync_cli import --source-url <source_url> --destination-url <destination_url>
    datadog_sync_cli export --source-url <source_url> --destination-url <destination_url>
    """
    cli(prog_name='datadog_sync_cli')
