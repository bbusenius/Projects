"""
Test suite for Cookie Clicker
"""

import poc_simpletest

def run_test(Test_Class):

    # Test the initial state of ClickerState
    print "Testing Phase 1: ClikerState initialization"
    print "methods tested: __init__"
    print "---------------------------------"
    
    suite0 = poc_simpletest.TestSuite()    
    test_state0 = Test_Class()
    
    suite0.run_test(test_state0.get_cookies(), 0.0, "1. Initial amount of cookies:")
    suite0.run_test(test_state0.get_cps(), 1.0, "2. Initial cps:")
    suite0.run_test(test_state0.get_time(), 0.0, "3. Initial time:")
    suite0.run_test(test_state0.get_history(), [(0.0, None, 0.0, 0.0)], "4. Initial history:")
    suite0.report_results()

    # Test the wait method
    print "Testing Phase 1: wait method"
    print "methods tested: wait"
    print "---------------------------------"

    suite2 = poc_simpletest.TestSuite()    
    test_state2 = Test_Class()
    
    test_state2.wait(0.0)
    print "wait for 0 s \n", test_state2
    suite2.run_test(test_state2.get_time(), 0.0, "1. time:")
    suite2.run_test(test_state2.get_cookies(), 0.0, "2. cookies")
    
    test_state2.wait(3.52)
    print "wait for 3.52 s \n", test_state2
    suite2.run_test(test_state2.get_time(), 3.52, "3. time:")
    suite2.run_test(test_state2.get_cookies(), 3.52, "4. cookies")
    
    test_state2.wait(1.48)
    print "wait for another 1.48 s \n", test_state2
    suite2.run_test(test_state2.get_time(), 5, "5. time:")
    suite2.run_test(test_state2.get_cookies(), 5, "6. cookies")

    test_state2.wait(-1.4)
    print "wait for negative time -1.4 \n", test_state2
    suite2.run_test(test_state2.get_time(), 5, "7. time:")
    suite2.run_test(test_state2.get_cookies(), 5, "8. cookies")
    suite2.report_results()

    print "Testing Phase 1: time_until method"
    print "time_until method"
    print "---------------------------------"
 
    suite1 = poc_simpletest.TestSuite()    
    test_state1 = Test_Class()
    
    suite1.run_test(test_state1.time_until(10.0), 10.0, "1. target cookie is 10.0:")
    suite1.run_test(test_state1.time_until(0.0), 0.0, "2. target cookie is 0.0:")
    suite1.run_test(test_state1.time_until(-1.0), 0.0, "3. target cookie is -1.0 (impossible, just checking):")
    suite1.run_test(test_state1.time_until(0.5), 1.0, "4. target cookie is fractional - 0.5 cookies:")
    suite1.run_test(test_state1.time_until(11.5), 12.0, "5. target cookie is fractional - 11.5 cookies:")
    
    test_state1.wait(10.0)
    suite1.run_test(test_state1.time_until(9.0), 0.0, "6. target is 9.0 when you had 10.0 cookies:")
    suite1.run_test(test_state1.time_until(11.0), 1.0, "7. target is 11.0 when you had 10.0 cookies:")
    suite1.run_test(test_state1.time_until(19.24), 10.0, "8. target is 19.24 when you had 10.0 cookies:")
    suite1.report_results()

    print "Testing Phase 1: buy_item"
    print "buy_item" 
    print "---------------------------------"

    suite3 = poc_simpletest.TestSuite()    
    test_state3 = Test_Class()
    
    test_state3.buy_item("Upgrade 1", 1.0, 1.0)
    print "1. buying a upgrade with 0 current cookies \n", test_state3
    suite3.run_test(test_state3.get_cookies(), 0.0, "1.1 current # of cookies should be zero: ")
    suite3.run_test(test_state3.get_cps(), 1.0, "1.2 current cps should not change: ")
    suite3.run_test(test_state3.get_history(), [(0.0, None, 0.0, 0.0)], "1.3 history should be default: ")
    
    test_state3.buy_item("Free upgrade", 0.0, 1.0)
    print "2. buying a free upgrade that doesn't cost cookies \n", test_state3
    suite3.run_test(test_state3.get_cookies(), 0.0, "2.1 current # of cookies should be zero: ")
    suite3.run_test(test_state3.get_cps(), 2.0, "2.2 current cps should be increased: ")
    suite3.run_test(test_state3.get_history(), [(0.0, None, 0.0, 0.0), (0.0, "Free upgrade", 0.0, 0.0)], "2.3 history should be updated: ")
   
    test_state3.wait(10.0)
    test_state3.buy_item("Upgrade 1", 1.0, 1.0)
    print "3. buying upgrade 1 again with 20 current cookies \n", test_state3
    suite3.run_test(test_state3.get_cookies(), 19.0, "3.1 current # of cookies should be 19 ")
    suite3.run_test(test_state3.get_cps(), 3.0, "3.2 current cps should be updated: ")
    suite3.run_test(test_state3.get_history(), [(0.0, None, 0.0, 0.0), (0.0, "Free upgrade", 0.0, 0.0), (10.0, "Upgrade 1", 1.0, 20.0)], "3.3 history should be updated: ")
    suite3.report_results()
    
