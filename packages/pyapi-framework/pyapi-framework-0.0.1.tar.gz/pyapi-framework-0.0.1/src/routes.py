class GetRoutesHandler():
    def invalid_route(self):
        data = {"error": "Invalid Route",
                "method": "GET"}
        return data

    def text_path(self):
        data = {"text": "hello",
                "method": "GET"}
        return data

    def main_path(self):
        data = {"main": "hello",
                "method": "GET"}
        return data


class PostRoutesHandler():
    def invalid_route(self):
        data = {"error": "Invalid Route",
                "method": "POST"}
        return data

    def text_path(self):
        data = {"text": "hello",
                "method": "POST"}
        return data

    def main_path(self):
        data = {"main": "hello",
                "method": "POST"}
        return data


class PutRoutesHandler():
    def invalid_route(self):
        data = {"error": "Invalid Route",
                "method": "PUT"}
        return data

    def text_path(self):
        data = {"text": "hello",
                "method": "PUT"}
        return data

    def main_path(self):
        data = {"main": "hello",
                "method": "PUT"}
        return data


class DeleteRoutesHandler():
    def invalid_route(self):
        data = {"error": "Invalid Route",
                "method": "DELETE"}
        return data

    def text_path(self):
        data = {"text": "hello",
                "method": "DELETE"}
        return data

    def main_path(self):
        data = {"main": "hello",
                "method": "DELETE"}
        return data
