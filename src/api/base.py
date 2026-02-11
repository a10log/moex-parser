import requests
import datetime
import logging

from tqdm import tqdm
from typing import Optional, Union, Dict, Any, List
from abc import ABC, abstractmethod


class BaseApi(ABC):   
	"""Базовый класс для API-клиентов."""
	
	def __init__(
		self,
		timeout: int = 30,
		max_retries: int = 3,
		use_pagination: bool = True,
		pagination_limit: int = 100
	):
		self.timeout = timeout
		self.max_retries = max_retries
		self.use_pagination = use_pagination
		self.pagination_limit = pagination_limit

		self.logger = logging.getLogger(self.__class__.__name__)
		
	@abstractmethod
	def get_data(self, *args, **kwargs) -> List[Any]:
		"""Абстрактный метод для получения данных."""
		pass

	@abstractmethod
	def extract_data(self, response: requests.Response) -> List[Any]:
		"""Абстрактный метод для парсинга данных."""
		pass
	
	@abstractmethod
	def get_url(self, *args, **kwargs) -> str:
		pass

	def get_paginated_data(
		self,
		url: str,
		base_params: Optional[Dict[str, Any]] = None,
	) -> List[Any]:
		
		if not self.use_pagination:
			response = self.send_request(url, params)
			page_data = self.extract_data(response)
			return [page_data]
		
		all_data = []
		start = 0
		page = 0
		params = base_params.copy() if base_params else {}

		while True:
			try:
				params['start'] = start
				params['limit'] = self.pagination_limit

				response = self.send_request(url, params)
				page_data = self.extract_data(response)

				all_data.extend(page_data)

				if len(page_data) < self.pagination_limit:
					break

				start += self.pagination_limit
				page += 1

			except Exception as e:
				self.logger.error(f"Ошибка при загрузке страницы {page + 1}: {e}")
				break

		return all_data

	def send_request(
		self, 
		url: str, 
		params: Optional[Dict[str, Any]] = None
	) -> requests.Response:
		for attempt in range(self.max_retries):
			try:
				response = requests.get(
					url=url, 
					params=params, 
					timeout=self.timeout
				)
				response.raise_for_status()
				return response
				
			except requests.Timeout:
				self.logger.warning(f"Таймаут запроса (попытка {attempt + 1}/{self.max_retries})")
				if attempt == self.max_retries - 1:
					raise
			except requests.RequestException as e:
				self.logger.error(f"Ошибка запроса: {e}")
				if attempt == self.max_retries - 1:
					raise

		
class BaseDynamicsApi(BaseApi, ABC):
	
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
	
	@abstractmethod
	def get_data_single_date(
		self,
		date: Union[str, datetime.datetime, datetime.date],
		*args,
		**kwargs
	) -> List[Any]:
		pass

	@abstractmethod
	def extract_data(self, response: requests.Response) -> List[Any]:
		"""Абстрактный метод для парсинга данных."""
		return 

	def get_data(
		self,
		start_date: Union[str, datetime.datetime, datetime.date],
		end_date: Union[str, datetime.datetime, datetime.date],
		*args,
		**kwargs
	) -> List[Any]:
		
		all_data = []
		for date in tqdm(
			self.generate_date_range(start_date, end_date)
		):
			data = self.get_data_single_date(
				date=date,
				*args, **kwargs
			)
			all_data.extend(data)
		return all_data
	  
	@staticmethod
	def validate_date(date: Union[str, datetime.datetime, datetime.date]) -> datetime.date:
		if isinstance(date, datetime.datetime):
			return date.date()
		elif isinstance(date, datetime.date):
			return date
		elif isinstance(date, str):
			try:
				return datetime.datetime.strptime(date, '%Y-%m-%d').date()
			except ValueError:
				for fmt in ('%Y%m%d', '%d.%m.%Y', '%d/%m/%Y'):
					try:
						return datetime.datetime.strptime(date, fmt).date()
					except ValueError:
						continue
				raise ValueError(f"Неверный формат даты: {date}. Ожидается 'YYYY-MM-DD'")
		else:
			raise TypeError(f"Неподдерживаемый тип даты: {type(date)}")
		
	@staticmethod
	def generate_date_range(
		start_date: Union[str, datetime.datetime, datetime.date],
		end_date: Union[str, datetime.datetime, datetime.date]
	) -> List[datetime.date]:
		
		start = BaseDynamicsApi.validate_date(start_date)
		end = BaseDynamicsApi.validate_date(end_date)

		if start > end:
			raise ValueError(f"Начальная дата ({start}) должна быть раньше конечной ({end})")

		days_diff = (end - start).days + 1
		return [
			start + datetime.timedelta(days=i) 
			for i in range(days_diff)
		]

__all__ = [
	"BaseApi",
	"BaseDynamicsApi"
]