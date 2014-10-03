def mystery(sorted_array, left_boundary, right_boundary):
    """
    Mystery algorithm from homework 3.
    https://d396qusza40orc.cloudfront.net/algorithmicthink/AT-Homework3/MysteryFig.pdf
    """
    if left_boundary > right_boundary:
        return -1
    m = (left_boundary + right_boundary) / 2

    if sorted_array[m] == m:
        return m
    else: 
        if sorted_array[m] < m:
            return mystery(sorted_array, m + 1, right_boundary)
        else:
            return mystery(sorted_array, left_boundary, m - 1)

           

#print mystery([-2,0,1,3,7,12,15],0,6)
print mystery([0,1,2,3,4,5,6,7,8],0,100)
