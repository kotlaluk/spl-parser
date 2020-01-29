class SplResource:

    def view_command(self, command):
        print(command)

    def generate_grammar(self, outfile):
        print(outfile)


class LocalSplResource(SplResource):
    def __init__(self, file):
        self.file = file


class RemoteSplResource(SplResource):
    def __init__(self, url):
        self.url = url
