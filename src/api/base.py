import os
import requests
import pandas as pd

from abc import ABC, abstractmethod

class BaseApi(ABC):

	def __init__(
		self,
		data_path: str = None
	):
		self.data_path = data_path
		self.data_df = None
	
	def send_request(self, url):
		response = requests.get(url=url)
		return response.content
	
	@abstractmethod
	def get_data(self):
		pass

	def save_data(self) -> None:
		if self.data_df is not None:
			if self.data_path is None:
				raise AttributeError
			else:
				self.data_df.to_csv(self.data_path, index=False)
		else:
			raise FileNotFoundError


		





