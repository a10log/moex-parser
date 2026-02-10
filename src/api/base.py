import os
import requests
import datetime
import pandas as pd
from typing import Optional, Union, Dict, Any
from abc import ABC, abstractmethod
import logging

class BaseApi(ABC):
    """Базовый класс для API-клиентов."""
    
    def __init__(
        self,
        filepath: Optional[str] = None,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Args:
            filepath: Путь для сохранения данных
            timeout: Таймаут запросов в секундах
            max_retries: Максимальное количество попыток повторного запроса
        """
        self.filepath = filepath
        self.data_df: Optional[pd.DataFrame] = None
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def get_data(self, *args, **kwargs) -> pd.DataFrame:
        """Абстрактный метод для получения данных."""
        pass    
    
    def send_request(
        self, 
        url: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> bytes:
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url=url, 
                    params=params, 
                    timeout=self.timeout
                )
                response.raise_for_status()
                return response.content
                
            except requests.Timeout:
                self.logger.warning(f"Таймаут запроса (попытка {attempt + 1}/{self.max_retries})")
                if attempt == self.max_retries - 1:
                    raise
            except requests.RequestException as e:
                self.logger.error(f"Ошибка запроса: {e}")
                if attempt == self.max_retries - 1:
                    raise
    
    def save_data(self, filepath: str) -> None:        
        if self.data_df is None or self.data_df.empty:
            raise ValueError("Нет данных для сохранения")
    
        try:
            filepath = self.validate_filepath(filepath)
            self.data_df.to_csv(filepath, index=False, encoding='utf-8')
            self.logger.info(f"Данные сохранены в {filepath}")
            
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении данных: {e}")
            raise
    
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
    def validate_filepath(filepath: str):
        if filepath is None:
            raise AttributeError("Не указан путь для сохранения данных")
        elif not filepath.endswith(".csv"):
            return filepath + ".csv"
        else:
            return filepath 
            
    @staticmethod
    def generate_date_range(
        start_date: Union[str, datetime.datetime, datetime.date],
        end_date: Union[str, datetime.datetime, datetime.date]
    ) -> list[datetime.date]:
        start = BaseApi.validate_date(start_date)
        end = BaseApi.validate_date(end_date)
        
        if start > end:
            raise ValueError(f"Начальная дата ({start}) должна быть раньше конечной ({end})")
        
        days_diff = (end - start).days + 1
        return [start + datetime.timedelta(days=i) for i in range(days_diff)]
    
__all__ = [
	BaseApi
]

