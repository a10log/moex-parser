import logging
import datetime

from src.api.reference.engines import EnginesApi
from src.api.reference.markets import MarketsApi
from api.history import HistoryApi

logging.basicConfig(
	level=logging.INFO,
	format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

START_DATE = datetime.datetime.strptime("2016-01-01", '%Y-%m-%d')
END_DATE = datetime.datetime.strptime("2026-01-01", '%Y-%m-%d')


def main():

	engines_api = EnginesApi()
	engines_api.get_data()

	markets_api = MarketsApi()
	markets_api.get_data()

	history_api = HistoryApi()
	history_api.get_data(
		market_name="shares",
		engine_name="stock",
		start_date=START_DATE,
		end_date=END_DATE
	)

	history_api.get_data(
		market_name="bonds",
		engine_name="stock",
		start_date=START_DATE,
		end_date=END_DATE
	)

	history_api.get_data(
		market_name="index",
		engine_name="stock",
		start_date=START_DATE,
		end_date=END_DATE
	)


if __name__ == "__main__":
	main()