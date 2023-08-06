import pandas as pd
from twneo.config.config import TWNEO_CONFIG, get_graph_driver



class GraphDataReader:

    def __init__(self):
        self.db_name = TWNEO_CONFIG['TWNEO_CONFIG']['NEO4J']['database']
        self.driver = get_graph_driver()

    def read_query (self, tx, cypher ):
        result = tx.run(cypher)
        return list(result)

    def read_query_resulrs(self, cypher):
        with self.driver.session(database= self.db_name) as session:
            records = session.read_transaction(self.read_query, cypher)
            record_df = pd.DataFrame(records, columns=records[0].keys())
        return record_df
