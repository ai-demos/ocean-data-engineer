from phi.tools.duckdb import DuckDbTools
from phi.tools.file import FileTools
from workspace.settings import ws_settings

oceangpt_duckdb_tools = DuckDbTools()
oceangpt_file_tools = FileTools(base_dir=ws_settings.ws_root.joinpath("oceangpt/op"))
