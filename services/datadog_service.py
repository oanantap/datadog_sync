from handlers.synthetic_test_importer import SyntheticTestImporter
from handlers.synthetic_test_exporter import SyntheticTestExporter
from handlers.global_variables_handler import GlobalVariablesHandler
from config.config import (
    SOURCE_GLOBAL_VARIABLES_API, DESTINATION_GLOBAL_VARIABLES_API
)


class DatadogService:
    def __init__(self, config):
        self.importer = SyntheticTestImporter(
            config['api_key'],
            config['app_key']
        )
        self.exporter = SyntheticTestExporter(
            config['api_key'],
            config['app_key']
        )
        self.global_variables = GlobalVariablesHandler(
            config['api_key'],
            config['app_key'],
            SOURCE_GLOBAL_VARIABLES_API,
            DESTINATION_GLOBAL_VARIABLES_API
        )

    def import_global_variables(self):
        self.global_variables.download_global_variables()

    def import_synthetic_tests(self):
        if not self.importer.already_imported():
            self.importer.import_synthetic_tests()
        self.import_global_variables()

    def export_synthetic_tests(self):
        self.global_variables.create_missing_global_variables()
        self.exporter.init_exporter()
        self.exporter.export_synthetic_tests()
