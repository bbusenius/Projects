"""
Simple test suit for Word Wrangler
"""

import poc_simpletest

def run_test1(remove_duplicates):

    # create a TestSuite object
    suite = poc_simpletest.TestSuite()

    suite.run_test(remove_duplicates([1, 1, 2, 3, 4, 4, 5, 6, 7, 7]), [1, 2, 3, 4, 5, 6, 7], "Test #1: Duplicates at ends")
    suite.run_test(remove_duplicates([1, 2, 3, 3, 4, 4, 5, 5, 6, 7]), [1, 2, 3, 4, 5, 6, 7], "Test #2: Duplicates in middle")
    suite.run_test(remove_duplicates([22, 22, 21, 21, 21, 20, 18, 15, 9, 9, 8, 7, 6, 6, 5, 2, 2]), [22, 21, 20, 18, 15, 9, 8, 7, 6, 5, 2], "Test #3: Reverse order dups at ends")
    suite.run_test(remove_duplicates([22, 21, 21, 21, 20, 18, 15, 9, 9, 8, 7, 6, 6, 5, 2]), [22, 21, 20, 18, 15, 9, 8, 7, 6, 5, 2], "Test #4: Reverse order dups in middle")
    suite.run_test(remove_duplicates([4, 5, 6, 9, 15, 22]), [4, 5, 6, 9, 15, 22], "Test #5: No Duplicates") 
    suite.run_test(remove_duplicates([22, 16, 8, 7, 6, 5]), [22, 16, 8, 7, 6, 5], "Test #6: No Duplicates Reverse order") 
    suite.run_test(remove_duplicates([4, 4]), [4], "Test #7: a pair of Duplicates") 
    suite.run_test(remove_duplicates([4]), [4], "Test #8: single element") 
    suite.run_test(remove_duplicates([]), [], "Test #9: empty string") 

    
    suite.report_results()
    
def run_test2(intersect):
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    suite.run_test(intersect([], [2, 3, 4]), [], "Test #1: 1st list empty")
    suite.run_test(intersect([1, 2, 3], []), [], "Test #2: 2nd list empty")
    suite.run_test(intersect([], []), [], "Test #3: Both lists empty")
    suite.run_test(intersect([1, 3, 4, 8], [2, 3, 4, 7]), [3, 4], "Test #4: Same length, shared in middle")
    suite.run_test(intersect([1, 3, 4, 8], [1, 3, 5, 8]), [1, 3, 8], "Test #5: Same length, shared at ends")
    suite.run_test(intersect([1, 2, 3], [1, 2, 3]), [1, 2, 3], "Test #6: All shared")
    suite.run_test(intersect([1, 2, 3], [4, 5, 6]), [], "Test #7: No shared")
    suite.run_test(intersect([1, 3, 4, 5, 6], [2, 4, 5, 7]), [4, 5], "Test #8: 1st longer, shared in middle")
    suite.run_test(intersect([1, 3, 4, 5], [ 2, 3, 4, 6, 7, 8]), [3, 4], "Test #9: 2nd longer, shared in middle")
    suite.run_test(intersect([1, 2, 3, 5], [1, 2, 4]), [1, 2], "Test #10: 1st longer, shared at start")
    suite.run_test(intersect([1, 2, 5, 7], [1, 2, 3, 4, 5, 8]), [1, 2, 5], "Test #11: 2nd longer, shared at start")
    suite.run_test(intersect([1, 2, 3, 5, 6, 8, 9 ], [5, 6, 7, 8, 9]), [5, 6, 8, 9], "Test #12: 1st longer, shared at end")
    suite.run_test(intersect([1, 2, 5], [2, 3, 4, 5]), [2, 5], "Test #13: 2nd longer, shared at end")
    suite.run_test(intersect([1, 2, 5, 9, 12, 22, 25, 26, 27, 30], [2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 26, 27]), [2, 5, 12, 26, 27], "Test #14: Long lists")
    
    suite.report_results()
    
    
def run_test3(merge):
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    suite.run_test(merge([], [2, 3, 4]), [2, 3, 4], "Test #1: 1st list empty")
    suite.run_test(merge([1, 2, 3], []), [1, 2, 3], "Test #2: 2nd list empty")
    suite.run_test(merge([], []), [], "Test #3: Both lists empty")
    suite.run_test(merge([1, 3, 4, 8], [2, 5, 6, 7]), [1, 2, 3, 4, 5, 6, 7, 8], "Test #4: Same length 1st starts")
    suite.run_test(merge([3, 4, 8, 9], [1, 2, 5, 7]), [1, 2, 3, 4, 5, 7, 8, 9], "Test #5: Same length 2nd starts")
    suite.run_test(merge([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6], "Test #6: All lower in left")
    suite.run_test(merge([4, 5, 6], [1, 2, 3]), [1, 2, 3, 4, 5, 6], "Test #7: All lower in right")
    suite.run_test(merge([1, 3, 4, 5, 6], [2, 7]), [1, 2, 3, 4, 5, 6, 7], "Test #8: 1st longer starts left")
    suite.run_test(merge([1, 3, 4, 5], [ 2, 6, 7, 8, 9]), [1, 2, 3, 4, 5, 6, 7, 8, 9], "Test #9: 2nd longer starts left")
    suite.run_test(merge([2, 3, 5, 6, 7], [1, 4, 9]), [1, 2, 3, 4, 5, 6, 7, 9], "Test #10: 1st longer starts right")
    suite.run_test(merge([2, 5, 7], [1, 3, 4, 8]), [1, 2, 3, 4, 5, 7, 8], "Test #11: 2nd longer starts right")
    
    suite.report_results()
    
    
def run_test4(merge_sort):
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    suite.run_test(merge_sort([],), [], "Test #1: Empty list ")
    suite.run_test(merge_sort([3],), [3], "Test #2: Single item list")
    suite.run_test(merge_sort([3, 9],), [3,9], "Test #3: Pair in order")
    suite.run_test(merge_sort([3, 2],), [2, 3], "Test #4: Pair out of order")
    suite.run_test(merge_sort([9, 8, 7, 4, 3, 2]), [2, 3, 4, 7, 8, 9], "Test #5: List in reverse order")
    suite.run_test(merge_sort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5], "Test #6: List in order")
    suite.run_test(merge_sort([5, 2, 6, 3, 4, 8, 1, 9]), [1, 2, 3, 4, 5, 6, 8, 9], "Test #7: Random even length list")
    suite.run_test(merge_sort([5, 2, 15, 6, 3, 4, 8, 1, 9]), [1, 2, 3, 4, 5, 6, 8, 9, 15], "Test #8: Random odd length list")
    
    suite.report_results()

def run_test5(gen_all_strings):
    
    # create a TestSuite object
    suite = poc_simpletest.TestSuite()
    
    suite.run_test(gen_all_strings(""), [""], "Test #1: Empty list ")

    testlist = gen_all_strings("a")
    testlist.sort()
    suite.run_test(testlist, ["", "a"], "Test #2: Single char list ")
    
    testlist = gen_all_strings("ab")
    testlist.sort()
    suite.run_test(testlist, ['', 'a', 'ab', 'b', 'ba'], "Test #3: Pair of chars list ")
    
    testlist = gen_all_strings("aa")
    testlist.sort()
    suite.run_test(testlist, ["", "a", "a", "aa", "aa"], "Test #4: Pair of matching chars list ")
    
    testlist = gen_all_strings("abc")
    testlist.sort()
    suite.run_test(testlist, ['', 'a', 'ab', 'abc', 'ac', 'acb', 'b', 'ba', 'bac', 'bc', 'bca', 'c', 'ca', 'cab', 'cb', 'cba'], "Test #5: Three chars list ")
    
    testlist = gen_all_strings("aab")
    testlist.sort()
    suite.run_test(testlist, ['', 'a', 'a', 'aa', 'aa', 'aab', 'aab', 'ab', 'ab', 'aba', 'aba', 'b', 'ba', 'ba', 'baa', 'baa'], "Test #6: Three chars list ")
    
    suite.report_results()
    
    
def run_all(remove_duplicates, intersect, merge, merge_sort, gen_all_strings):
    print "remove_duplicates tests"
    run_test1(remove_duplicates)
    print
    print "intersect tests"
    run_test2(intersect)
    print
    print "merge tests"
    run_test3(merge)
    print
    print "merge_sort tests"
    run_test4(merge_sort)
    print
    print "gen_all_strings tests"
    run_test5(gen_all_strings)
