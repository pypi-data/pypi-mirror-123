class Request:
    def __init__(self, **kwargs):
        self.url = None
        self.method = None
        self.data = None
        self.json = None
        self.headers = None
        self.cookies = None
        self.allow_redirects = None
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '<Request {}>'.format(self.url)
