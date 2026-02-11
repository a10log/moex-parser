import requests
from typing import Optional, List, Any

from src.api.utils import parse_xml
from src.api.base import BaseApi

BASE_URL = "https://iss.moex.com/iss/engines.xml"

class EnginesApi(BaseApi):

	def __init__(
		self,
		timeout: int = 30,
		max_retries: int = 3,
		use_pagination: bool = True,
		pagination_limit: int = 100
	):
		super().__init__(
			timeout=timeout,
			max_retries=max_retries,
			use_pagination=use_pagination,
			pagination_limit=pagination_limit
		)
	
	def get_data(self) -> List[Any]:
		return self.get_paginated_data(url=self.get_url())

	def extract_data(self, response: requests.Response) -> List[Any]:
		return parse_xml(response.content)
	
	def get_url(self) -> str:
		return BASE_URL

__all__ = [
	"EnginesApi"
]