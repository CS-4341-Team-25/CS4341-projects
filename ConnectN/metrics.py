import time

class Metrics():

# Class constructor. 
    def __init__(self):
        self.nodesChecked = 0 
        self.total_nodes_checked = 0
        self.start_time = 0
        self.end_time = 0
        self.total_time = 0
        self.elapsed = 0
        self.moves = 0
        self.debug = False
        self.max_elapsed = 0
        
    # Start timer, record current time from perf_counter()  
    def start_timer(self):
        self.start_time = time.perf_counter()
        self.total_nodes_checked += self.nodesChecked
        self.nodesChecked = 0
        self.moves += 1
        
    # End timer and get time elapsed since you started the timer
    # RETURN [float]: time since start_timer() was called 
    def end_timer(self):
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time
        self.max_elapsed = max(self.elapsed, self.max_elapsed)
        self.total_time += self.elapsed
        return self.elapsed

    def lap(self):
        start_timer()
        return self.elapsed
    
    #Keeps track of the total nodes visited
    def count(self):
        self.nodesChecked += 1

        if(self.debug and not self.nodesChecked%1000):
            print("Nodes Checked: " + str(self.nodesChecked))

    #Gets the averages nodes checked per second
    def getNodePerSec(self):
        return self.total_nodes_checked / self.total_time
    
    # 
    def getAvgTimePerMove(self):
        return self.moves / self.total_time