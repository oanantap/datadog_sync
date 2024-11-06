class SyntheticTest:
    def __init__(self, client):
        self.client = client

    def download(self):
        raise NotImplementedError("This method should be overridden by subclasses")