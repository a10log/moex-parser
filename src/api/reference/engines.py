import requests
import pandas as pd

from src.parsers.xml import parse_xml
from src.api.base import BaseApi
from src.core.config import DataPath


url = "https://iss.moex.com/iss/engines.xml"


class EnginesApi(BaseApi):

	def __init__(
		self,
		data_path: str = DataPath.ENGINES_DATA_PATH
	):
		super().__init__(data_path)

	def get_data(self):
		data_xml = self.send_request(url)
		data = parse_xml(data_xml)
		self.data_df = pd.DataFrame(data)
		self.save_data()
		return self.data_df

__all__ = [
	EnginesApi
]