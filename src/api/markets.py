import requests
import pandas as pd

from src.api.utils import parse_xml
from src.api.base import BaseApi
from src.config import DataPath


BASE_URL = "https://iss.moex.com/iss/engines/{engine}/markets.xml"


class MarketsApi(BaseApi):

	def __init__(self):
		super().__init__()

	def extract_data(self, response: requests.Response):
		return parse_xml(response.content)

	def get_data(self):
		all_data: list = []
		for i, row in pd.read_csv(DataPath.ENGINES_DATA_PATH).iterrows():
			data = self._get_data_single(row["name"])
			all_data.append(data)
		return all_data

	def get_url(self, engine: str):
		return BASE_URL.format(engine=engine)
	
	def _get_data_single(self, engine: str):
		data = self.get_paginated_data(url=self.get_url(engine))
		return data
	
__all__ = [
	MarketsApi
]