import re
import sys


class Rerouting:
    def __init__(self):
        match = re.match('([^:]+://[^/]+)(/.*)', sys.argv[0] + sys.argv[2])
        self._baseurl = match.group(1)
        self._pathquery = match.group(2)
        self._routemap = {}

    def route(self, pattern):
        """
        Registers a view function.

        :param pattern: A pattern to match.
        :return: A decorator.
        """

        def decorator(func):
            self._map_route(func, pattern)
            return func

        return decorator

    def run(self):
        """
        Executes the view function.

        :return: Returns True if a view function is found else None.
        """
        for (func, patterns) in self._routemap.items():
            for pattern in patterns:
                match = re.fullmatch(pattern, self._pathquery)

                if match is not None:
                    try:
                        func(**match.groupdict())
                        return True
                    except TypeError:
                        pass

        return False

    def url_for(self, pathquery):
        """
        Constructs a URL for the addon using the path and the query.

        :param pathquery: A path with query.
        """
        return self._baseurl + pathquery if pathquery.startswith('/') else '/' + pathquery

    def _map_route(self, func, pattern):
        """
        Binds a pattern to the function.

        :param func: The function.
        :param pattern: A pattern.
        """
        if func not in self._routemap:
            self._routemap[func] = []

        self._routemap[func].append(pattern)
