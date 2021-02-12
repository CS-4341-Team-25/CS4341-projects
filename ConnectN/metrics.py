import time

class Metrics():

# Class constructor. 
    def __init__(self):
        self.nodesChecked = 0 
        self.start_time = 0
        self.end_time = 0
        self.total_time = 0
        
    # Start timer, record current time from perf_counter()  
    def start_timer():
        self.start_time = time.perf_counter()
        
    # End timer and get time elapsed since you started the timer
    # RETURN [float]: time since start_timer() was called 
    def end_timer():
        self.end_time = time.perf_counter()
        elapsed = self.end_time - self.start_time
        self.total_time += elapsed
        return elapsed
    
    
    def count():
        self.nodesChecked += 1
        