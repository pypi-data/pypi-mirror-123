from urllib.parse import urlparse


class URL:

    def __init__(self, url: str):
        parsed = urlparse(url)
        # `params` are old asf and there is like nooooo resources on them
        # im just gonna append it to the end of path and hope for the best
        # (not the same as query string params)
        # `anchor` should never matter for an api so it's not going to be supported
        self._protocol = parsed.scheme
        self._domain = parsed.netloc
        self._path = parsed.path + parsed.params

        # parse to dict
        query = parsed.query
        self._query = {}
        for param in query.split("&"):
            # sometimes param can be "" :shrug:
            if param:
                key, value = param.split("=", maxsplit=1)
                self._query[key] = value

    def __repr__(self):
        return f"<URL protocol={self.protocol} domain={self.domain} path={self.path}>"

    def __str__(self):
        return f"{self.protocol}://{self.domain}{self.path}"

    @property
    def protocol(self) -> str:
        return self._protocol

    @property
    def domain(self) -> str:
        return self._domain

    @property
    def path(self) -> str:
        return self._path

    @property
    def query(self) -> dict:
        return self._query
