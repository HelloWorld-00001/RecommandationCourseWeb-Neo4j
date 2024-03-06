import pandas as pd
from DataConnector.connector import DatabaseConnector

class BaseModel():
    connector = DatabaseConnector()
    driver = connector.getConnection()

    def __init__(self):
        pass

    def queryToDataFrame(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            columns = result.keys()
            data = [record for record in result]

        return pd.DataFrame(data, columns=columns)

    
