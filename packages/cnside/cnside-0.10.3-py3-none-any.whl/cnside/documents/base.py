class Document(dict):
    __version__ = "1.0.0"
    __doc_type__ = "BaseDocument"

    def __getattribute__(self, item):
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        self[key] = value
