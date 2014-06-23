"""
Cookie Clicker Simulator
"""

# import simpleplot
import matplotlib.pyplot as plt
import math, random

# Used to increase the timeout, if necessary
# import codeskulptor
# codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_number_of_cookies = 0.0
        self._current_number_of_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        results = "\n\nTime: %s\nCurrent number of cookies: %s\nCPS: %s\nTotal number of cookies: %s\n" \
            % (str(self.get_time()), \
               str(self.get_cookies()), \
               str(self.get_cps()), \
               str(self.get_total_cookies()))
        return results
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """ 
        return self._current_number_of_cookies

    def get_total_cookies(self):
        """
        Return the total number of cookies
        """ 
        return self._total_number_of_cookies
   
    def get_cps(self):
        """
        Get current CPS (cookies per second)

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        if cookies > self.get_cookies():
            return math.ceil((cookies - self.get_cookies()) / self.get_cps())
        else:
            return 0.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._total_number_of_cookies += time * self.get_cps()
            self._current_number_of_cookies += time * self.get_cps()
            self._current_time += time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self.get_cookies() >= cost:
            self._current_number_of_cookies -= cost
            self._current_cps += additional_cps
            self._history_list += [(self.get_time(), item_name, cost, self.get_total_cookies())]
        else:
            return None
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    new_build_info = build_info.clone()
    clicker_state = ClickerState() 
    
    while clicker_state.get_time() <= duration:

        if clicker_state.get_time() > duration or strategy(clicker_state.get_cookies(), 
                    clicker_state.get_cps(),
                    duration - clicker_state.get_time(), 
                    new_build_info) == None:
            break
        # The item to buy next
        next_item = strategy(clicker_state.get_cookies(), 
                        clicker_state.get_cps(),
                        duration - clicker_state.get_time(), 
                        new_build_info)

        # Cost of the next item to buy and
        # the time to wait before buying the next item
        cost = new_build_info.get_cost(next_item)
        wait_time = clicker_state.time_until(cost)

        if wait_time + clicker_state.get_time() > duration:
            break
            
        # Wait until we have enough cookies to buy the next item, then buy it
        clicker_state.wait(wait_time)
        clicker_state.buy_item(next_item, cost, new_build_info.get_cps(next_item))
      
        # Update the item build info
        new_build_info.update_item(next_item)
 
    # Wait until the end of the duration    
    clicker_state.wait(duration - clicker_state.get_time())

    return clicker_state

def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    return "Cursor"

def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, time_left, build_info):
    """
    Always buy the cheapest item
    """
    cheapest = ['', float('inf')]
    for strategy in build_info.build_items():
        if build_info.get_cost(strategy) < cheapest[1]:
            cheapest[0] = strategy
            cheapest[1] = build_info.get_cost(strategy)
    if (time_left + cookies) / build_info.get_cost(cheapest[0]) >= 1:
        return cheapest[0]
    else:
        return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    Always return the most expensive item
    """
    affordable_items = []
    for production_method in build_info.build_items(): 
        if (time_left * cps + cookies) >= build_info.get_cost(production_method):
            affordable_items.append([production_method, build_info.get_cost(production_method), cps])
    
    retval = ['', float('-inf'), 0] 
    if len(affordable_items) > 0:
        for item in affordable_items: 
            if item[1] > retval[1]:
                retval = [item[0], item[1], item[2]]
    else:
        return None
    return retval[0]

def strategy_best(cookies, cps, time_left, build_info):
    """
    The best strategy I can come up with
    """
    items = []
    for item in build_info.build_items():
        items.append(item)
    choice = random.choice(items)  
    return choice
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)
    plt.plot(history)
    plt.title(strategy_name)
    plt.show()

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()

# Unit testing
#import poc_cookie_clicker_testsuite
#poc_cookie_clicker_testsuite.run_test(ClickerState)

import poc_cookie_clicker_testsuite2 as testsuite
testsuite.run_tests(ClickerState,simulate_clicker,strategy_cursor, strategy_cheap, strategy_expensive, strategy_best)
