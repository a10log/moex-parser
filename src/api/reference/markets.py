import requests
import pandas as pd

from src.parsers.xml import parse_xml
from src.api.base import BaseApi
from src.core.config import DataPath


BASE_URL = "https://iss.moex.com/iss/engines/{}/markets.xml"


class MarketsApi(BaseApi):

	def __init__(
		self, 
		filepath: str = DataPath.MARKETS_DATA_PATH,
	):
		super().__init__(filepath)

	def _get_data_single(self, engine: str):
		url = BASE_URL.format(engine)
		data_xml = self.send_request(url)
		data = parse_xml(data_xml)
		data_df = pd.DataFrame(data)
		return data_df

	def get_data(self):
		dataframes: list = []
		for i, row in pd.read_csv(DataPath.ENGINES_DATA_PATH).iterrows():
			data_df_single = self._get_data_single(row["name"])
			data_df_single.insert(0, "engine_id", row["id"])
			data_df_single.insert(1, "engine_name", row["name"])
			data_df_single.insert(2, "engine_title", row["title"])

			dataframes.append(data_df_single)
		self.data_df = pd.concat(dataframes, ignore_index=True)
		self.save_data(self.filepath)
		return self.data_df
	
__all__ = [
	MarketsApi
]