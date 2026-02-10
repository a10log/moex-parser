import os
from dataclasses import dataclass

@dataclass
class Config:

	METADATA_PATH: str = "data/metadata"
	DATA_PATH: str = "data"
	

@dataclass
class DataPath:

	ENGINES_DATA_PATH: str = os.path.join(Config.METADATA_PATH, "engines") + ".csv"
	MARKETS_DATA_PATH: str = os.path.join(Config.METADATA_PATH, "markets") + ".csv"