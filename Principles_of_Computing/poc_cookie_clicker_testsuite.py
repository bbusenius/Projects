"""
Test suite for Cookie Clicker
"""

import poc_simpletest

def run_test(Test_Class):

    # print instruction
    print "---------------------------------"
    print "Testing Phase 1: ClikerState set up"
    print "methods tested: __init__, __str__, get_cookies, get_cps, get_time, get_history"
    print "---------------------------------"
    
    # test ClickerState on initial state
    suite0 = poc_simpletest.TestSuite()    
    test_state0 = Test_Class()
    
    print "Initial State: \n", test_state0
    
    suite0.run_test(test_state0.get_cookies(), 0.0, "1. Initial amount of cookies:")
    suite0.run_test(test_state0.get_cps(), 1.0, "2. Initial cps:")
    suite0.run_test(test_state0.get_time(), 0.0, "3. Initial time:")
    suite0.run_test(test_state0.get_history(), [(0.0, None, 0.0, 0.0)], "4. Initial history:")
    suite0.report_results()

    # print instruction
    print "---------------------------------"
    print "Testing Phase 1: wait method"
    print "Your __init__, __str__, get_cookies, get_cps, get_time, get_history need to be functional"
    print "---------------------------------"

    # test ClickerState on time_until    
    suite2 = poc_simpletest.TestSuite()    
    
    test_wait1 = Test_Class()
    test_wait1.wait(0.0)
    print "wait for 0 s \n", test_wait1
    suite2.run_test(test_wait1.get_time(), 0.0, "1. time:")
    suite2.run_test(test_wait1.get_cookies(), 0.0, "2. cookies")
   
    test_wait2 = Test_Class() 
    test_wait2.wait(3.52)
    print "wait for 3.52 s \n", test_wait2
    suite2.run_test(test_wait2.get_time(), 3.52, "3. time:")
    suite2.run_test(test_wait2.get_cookies(), 3.52, "4. cookies")
   
    test_wait3 = Test_Class() 
    test_wait3.wait(1.48)
    print "wait for another 1.48 s \n", test_wait3
    suite2.run_test(test_wait3.get_time(), 1.48, "5. time:")
    suite2.run_test(test_wait3.get_cookies(), 1.48, "6. cookies")

    test_wait4 = Test_Class()
    test_wait4.wait(-1.4)
    print "wait for negative time -1.4 \n", test_wait4
    suite2.run_test(test_wait4.get_time(), 0.0, "7. time:")
    suite2.run_test(test_wait4.get_cookies(), 0.0, "8. cookies")
    suite2.report_results()

    # print instruction
    print "---------------------------------"
    print "Testing Phase 1: time_until method"
    print "Your __init__, __str__, get_cookies, get_cps, get_time, get_history and wait need to be functional"
    print "---------------------------------"

    # test ClickerState on time_until    
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
