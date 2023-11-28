from typing import List, Optional
from pydantic import BaseModel

from phi.agent.duckdb import DuckDbAgent

from workspace.settings import ws_settings
from utils.log import logger


class OceanTable(BaseModel):
    name: str
    columns: Optional[List[str]] = None
    description: str
    path: str


class Relationship(BaseModel):
    name: str
    type: str
    keys: List[str]
    description: str


ocean_tables = [
    OceanTable(
        name="predictoor",
        columns=[
            "PredictionID",
            "Epoch",
            "Timestamp",
            "Stake",
            "Wallet",
            "Payout",
            "TrueValue",
            "PredictedValue",
            "TradingPair",
            "TimeFrame",
            "Exchange",
        ],
        description="Contains information about predictions.",
        path=str(ws_settings.ws_root.joinpath("data/ocean/predictoor.csv")),
    ),
    OceanTable(
        name="trading_data",
        columns=[
            "timestamp",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "TradingPair",
            "TimeFrame",
            "ExchangeExample",
        ],
        description="Contains information about Trading_Data.",
        path=str(ws_settings.ws_root.joinpath("data/ocean/trading_data.csv")),
    ),
]

ocean_table_relationships = [
    Relationship(
        name="predictoor-trading_data",
        type="One-to-One",
        keys=["TradingPair (in predictoor)", "TradingPair (in trading_data)"],
        description="Links TradingPair between predictoor and trading_data.",
    ),
]
