from neo4j import GraphDatabase


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnector(metaclass=SingletonMeta):

    def __init__(self, uri= "bolt://localhost:7687", username= "neo4j", password= "12345678"):
        self.uri = uri
        self.username = username
        self.password = password

    
    def getConnection(self):
        return GraphDatabase.driver(self.uri, auth=(self.username, self.password))
    

