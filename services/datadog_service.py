from handlers.synthetic_test_importer import SyntheticTestImporter
from handlers.synthetic_test_exporter import SyntheticTestExporter


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

    def import_synthetic_tests(self):
        if not self.importer.already_imported():
            self.importer.import_synthetic_tests()

    def export_synthetic_tests(self):
        self.exporter.export_synthetic_tests()
