class SystemCallFault(Exception):

    def __init__(self):
        pass

    def __str__(self):
        return 'System not give expect response.'

class NecessaryLibraryNotFound(Exception):

    def __init__(self,value = '?'):
        self.value = value

    def __str__(self):
        return 'Necessary library \'%s\' not found.'%self.value