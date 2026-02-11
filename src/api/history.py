from typing import Optional, List, Any

from src.api.base import BaseDynamicsApi
from src.api.utils import parse_xml

BASE_URL = "https://iss.moex.com/iss/history/engines/{engine}/markets/{market}/securities.xml"

class HistoryApi(BaseDynamicsApi):

	def __init__(
		self,
		engine: str, 
		market: str,
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
		self.engine = engine
		self.market = market

	def get_data_single_date(self, date) -> List[Any]:
		return self.get_paginated_data(
			url=self.get_url(
				engine=self.engine,
				market=self.market
			),
			base_params={"date": date}
		)
		
	def extract_data(self, response) -> List[Any]:
		return parse_xml(response.content)
	
	def get_url(self, engine: str, market: str) -> str:
		return BASE_URL.format(engine=engine, market=market)
	
__all__ = [
	"HistoryApi"
]