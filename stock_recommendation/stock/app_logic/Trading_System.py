from datetime import date, datetime
from collections import deque
from . import Strategies
from .Stock_Class import Stock_Class
from .strategies.moving_averages import Moving_Average_Strategy
from .strategies.rsi import RSI_Strategy
from .strategies.bollinger_bands import Bollinger_Bands_Strategy

class Trading_System:
    
    def __init__(self):
        self.list_of_operations = deque()
    
    def compile_queue(self):
        from stock.models import Stock
        list_of_stocks = Stock.objects.prefetch_related("stock_data", "strategies", "recommendations").values('ticker')[0:101]
        for i in list_of_stocks.values():
            try:
                #Update db with new data
                ticker = i.ticker
                stock_object = Stock_Class(ticker)
                self.list_of_operations.append(lambda i=i: stock_object.update_data(i))
                
                # Get strategy objects
                moving_average_strategy = Moving_Average_Strategy(ticker)
                rsi_strategy = RSI_Strategy(ticker)
                bollinger_band_strategy = Bollinger_Bands_Strategy(ticker)
                
                # Add strategies to the queue
                self.list_of_operations.append(lambda:moving_average_strategy.apply_strategy())
                self.list_of_operations.append(lambda:rsi_strategy.apply_strategy())
                self.list_of_operations.append(lambda:bollinger_band_strategy.apply_strategy())
                    
                self.list_of_operations.append(lambda:stock_object.set_recommendations(i))
            except Exception as e:
                print(f"(Trading_System.py) The required actions for {i} could not be run due to Error: {e}")
        print(list_of_stocks)
    
    def run_operations(self):
        try:
            while self.list_of_operations:  # Runs all operations from the queue & then removes them
                operations = self.list_of_operations.popleft()
                operations()
        except Exception as e:
            print(f"(Trading_System.py) The operations could not be executed due to Error: {e}")