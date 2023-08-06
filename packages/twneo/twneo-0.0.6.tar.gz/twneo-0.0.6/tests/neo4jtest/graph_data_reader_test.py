import unittest
import os

class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        if 'twneo_config_path' not in os.environ:
            os.environ['twneo_config_path'] = r'/Users/pankaj/dev/git/twneo/twneo/config/config.yaml'
        import twneo.neo4j.graph_data_reader as graph_data_reader

        self.graph_reader=  graph_data_reader.GraphDataReader()

    def test_get_query_results(self):
        cypher = """
                     match(u:User) -[r:lives_in]-(l:Location) return count(u) as  count , l.location as location order by count desc;
                     """
        results  = self.graph_reader.read_query_resulrs(cypher)
        self.assertTrue(len(results)>0)


if __name__ == '__main__':
    unittest.main()
