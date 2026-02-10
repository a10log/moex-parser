from src.api.reference.engines import EnginesApi
from src.api.reference.markets import MarketsApi

def main():

	engines_api = EnginesApi()
	engines_api.get_data()

	markets_api = MarketsApi()
	markets_api.get_data()

if __name__ == "__main__":
	main()