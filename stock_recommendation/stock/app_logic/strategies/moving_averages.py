from Strategies import Strategy
import models.Stock

class Moving_Average_Strategy(Strategy):
    
    def __init__(self, strategy, stats, price):
        super().__init__(strategy, stats)
        self.short_term_moving_average = 0
        self.long_term_moving_average = 0
        self.stats = stats
        self.price = price
        
    def calculate_short_term_moving_average(self):
        total_close_prices = 0
        for i in self.stats[151:200]:
            total_close_prices += i
        self.short_term_moving_average = total_close_prices/50
        
    def calculate_long_term_moving_average(self):
        total_close_prices = 0
        for i in self.stats:
            total_close_prices += i
        self.long_term_moving_average = total_close_prices/200
    
    def generate_signal(self):
        stock_field = Stock.objects.get(ticker=i)
        stock_id = stock_field.stock_id
        
        if self.price > self.short_term_moving_average and self.short_term_moving_average > self.long_term_moving_average:
            Stock.add_indicator("moving averages", stock_id, "Buy")
        elif self.price < self.short_term_moving_average and self.short_term_moving_average < self.long_term_moving_average:
            Stock.add_indicator("moving averages", stock_id, "Sell")
        else:
            Stock.add_indicator("moving averages", stock_id, "Hold")
            
    def apply_strategy(self):
        calculate_short_term_moving_average(self)
        calculate_long_term_moving_average(self)
        generate_signal(self)