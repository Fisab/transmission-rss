import shelve


class DatabaseClient:
    def __init__(self, file_name: str):
        self._database = shelve.open(file_name)

    def __del__(self):
        self._database.close()

    def get_series_by_name(self, name: str):
        return self._database.get(name, [])

    def remember_series_name(self, name: str, series: list[int]):
        self._database[name] = self._database.get(name, []) + series
