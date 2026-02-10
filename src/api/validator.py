from typing import Dict, List, Tuple, Set

class MarketValidator:
    """Класс для работы с допустимыми комбинациями engine-market"""
    
    def __init__(self):
        self._valid_combinations = {
            "stock": ["shares", "bonds", "index", "ndmsec", "currency"],
            "currency": ["selt", "fixing", "indices"],
            "futures": ["forts", "options", "futures"],
            "commodity": ["commodity", "standard"],
            "state": ["agriculture", "exchange"],
            "repo": ["repo", "deposit"],
            "bonds": ["bonds", "main"],
            "offboard": ["qnv", "main"],
        }
    
    @property
    def valid_combinations(self) -> Dict[str, List[str]]:
        """Возвращает словарь допустимых комбинаций"""
        return self._valid_combinations.copy()
    
    def get_all_engines(self) -> List[str]:
        """Возвращает список всех допустимых engine"""
        return list(self._valid_combinations.keys())
    
    def get_markets_for_engine(self, engine: str) -> List[str]:
        """Возвращает список market для конкретного engine"""
        if engine not in self._valid_combinations:
            valid_engines = self.get_all_engines()
            raise ValueError(
                f"Недопустимый engine: '{engine}'. "
                f"Допустимые: {valid_engines}"
            )
        return self._valid_combinations[engine].copy()
    
    def validate_market(self, engine: str, market: str) -> Tuple[bool, str]:
        """Проверяет, допустима ли комбинация engine-market"""
        if engine not in self._valid_combinations:
            valid_engines = self.get_all_engines()
            raise ValueError(
                f"Недопустимый engine: '{engine}'. "
                f"Допустимые: {valid_engines}"
            )
        
        if market not in self._valid_combinations[engine]:
            valid_markets = self.get_markets_for_engine(engine)
            raise ValueError(
                f"Market '{market}' не доступен для engine '{engine}'. "
                f"Доступные: {valid_markets}"
            )
        
        return True, "Комбинация допустима"
    
    def get_combinations_table(self) -> str:
        """Возвращает таблицу всех комбинаций в виде строки"""
        table_lines = []
        for engine, markets in self._valid_combinations.items():
            markets_str = ", ".join(markets)
            table_lines.append(f"{engine:15} -> {markets_str}")
        
        header = "ENGINE          -> MARKETS"
        separator = "-" * 50
        return "\n".join([header, separator] + table_lines)