from phi.agent.duckdb import DuckDbAgent
from typing import Optional, Tuple, List

try:
    import duckdb
except ImportError:
    raise ImportError("`duckdb` not installed. Please install it using `pip install duckdb`.")


class OceanDEAgent(DuckDbAgent):
    def __init__(
        self,
        db_path: str = ":memory:",
        connection: Optional[duckdb.DuckDBPyConnection] = None,
        init_commands: Optional[List] = None,
    ):
        super().__init__(
            name="ocean_de_agent",
            db_path=db_path,
            connection=connection,
            init_commands=init_commands,
            run_queries=False,
        )
        self.register(self.run_db_query)

    def run_db_query(self, query: str) -> str:
        """Function to run SQL queries against a duckdb database

        :param query: SQL query to run
        :return: Result of the query
        """
        pass
