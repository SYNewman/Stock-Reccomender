from Strategies import Strategy
import models.Stock

class RSI_Strategy(Strategy):
    
    def __init__(self, strategy, stats, price):
        super().__init__(strategy, stats)
        self.time_period = 14
        self.stats = stats
        self.price = price
        self.price_changes = []
        self.gains = []
        self.losses = []
        self.average_gain = 0
        self.average_loss = 0
        self.second_average_gain = 0
        self.second_average_loss = 0
        self.rs_value = 0
        self.rsi_value = 0
    
    def calculate_daily_price_change(self):
        for i in range(len(self.stats-1)):
            price_change = self.stats[i] - self.stats[i+1]
            self.price_changes.append(price_change)
    
    def separate_gains_and_losses(self):
        for i in self.price_changes:
            if i > 0:
                self.gains.append(i)
                self.losses.append(0)
            elif i < 0:
                self.gains.append(0)
                self.losses.append(i*-1)
            else:
                self.gains.append(0)
                self.losses.append(0)
    
    def calculate_average_gain(self):
        total_gain = 0
        for i in self.gains:
            total_gain += i
        self.average_gain = total_gain / self.time_period
    
    def calculate_average_loss(self):
        total_loss = 0
        for i in self.losses:
            total_loss += i
        self.average_loss = total_loss / self.time_period
    
    def calculate_second_average_gain(self): # To smooth out the values
        current_gain = self.price - self.stats[-1]
        if current_gain < 0:
            current_gain = 0
        previous_average_gain = average_gain * (self.time_period - 1)
        self.second_average_gain = (previous_average_gain + current_gain) / self.time_period
        
    def calculate_second_average_loss(self): # To smooth out the values
        current_loss = self.price - self.stats[-1]
        if current_loss < 0:
            current_loss = 0
        previous_average_loss = average_loss * (self.time_period - 1)
        self.second_average_loss = (previous_average_loss + current_loss) / self.time_period
    
    def calculate_relative_strength(self):
        if self.second_average_loss == 0:
            self.rs_value = float('inf')
        self.rs_value = self.second_average_gain / self.second_average_loss
    
    def calculate_rsi_value(self):
        self.rsi_value = 100 - (100 / (self.rs+1))
    
    def generate_signal(self):
        stock_field = Stock.objects.get(ticker=i)
        stock_id = stock_field.stock_id
        
        if self.rsi_value < 30:
            Stock.add_indicator("rsi", stock_id, "Buy")
            print("Buy")
        elif self.rsi_value > 70:
            Stock.add_indicator("rsi", stock_id, "Sell")
            print("Sell")
        else:
            Stock.add_indicator("rsi", stock_id, "Hold")
            print("Hold")
            
    def apply_strategy(self):
        calculate_daily_price_change(self)
        separate_gains_and_losses(self)
        calculate_average_gain(self)
        calculate_average_loss(self)
        calculate_second_average_gain(self)
        calculate_second_average_loss(self)
        calculate_relative_strength(self)
        calculate_rsi_value(self)
        generate_signal(self)