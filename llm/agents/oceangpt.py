from phi.agent.duckdb import DuckDbAgent
from phi.agent.file import FileAgent
from workspace.settings import ws_settings

oceangpt_duckdb_agent = DuckDbAgent()
oceangpt_file_agent = FileAgent(base_dir=ws_settings.ws_root.joinpath("oceangpt/op"))
