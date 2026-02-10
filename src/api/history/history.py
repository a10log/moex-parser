import os
import pandas as pd
import datetime 
from tqdm import tqdm
from typing import Union

from src.api.base import BaseApi
from src.core.config import Config
from src.utils import parse_xml

from src.api.validator import MarketValidator


BASE_URL = "https://iss.moex.com/iss/history/engines/{engine}/markets/{market}/securities.xml"

class HistoryApi(BaseApi):

	def __init__(
		self,
	):	
		super().__init__()
		self.market_validator = MarketValidator()

	def _get_data_single_day(
		self, 
		market_name: str,
		engine_name: str,
		date: Union[str, datetime.datetime, datetime.date]
	):
		url = BASE_URL.format(
			engine=engine_name, 
			market=market_name
		)
		data_xml = self.send_request(
			url, params={"date": date}
		)
		data = parse_xml(data_xml)
		return pd.DataFrame(data)


	def get_data(
		self,
		start_date: Union[str, datetime.datetime, datetime.date],
		end_date: Union[str, datetime.datetime, datetime.date],
		market_name: str,
		engine_name: str = "stock",
	):
		start_date = self.validate_date(start_date)
		end_date = self.validate_date(end_date)
		self.market_validator.validate_market(
			engine=engine_name,
			market=market_name
		)

		self.logger.info(
            f"Получение данных: engine={engine_name}, "
            f"market={market_name}, start={start_date}, end={end_date}"
        )

		days_diff = (end_date - start_date).days + 1
		all_dates = [start_date + datetime.timedelta(days=i) for i in range(days_diff)]
		
		dataframes = []
		for date in tqdm(all_dates, total=days_diff):
			
			data_df_single = self._get_data_single_day(
				market_name=market_name,
				engine_name=engine_name,
				date=date,
		
			)
			dataframes.append(data_df_single)
			
		self.data_df = pd.concat(dataframes, ignore_index=True).sort_values(by="TRADEDATE", ascending=False)
		
		dirpath = os.path.join(Config.HISTORY_DATA_DIR_PATH, engine_name)
		os.makedirs(dirpath, exist_ok=True)

		filepath = os.path.join(dirpath, market_name)
		self.save_data(filepath)

		return self.data_df