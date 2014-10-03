def sort_count(A,B):
    """
    Calculate inversions in a list.
    """
    global inversions
    C=[]
    len_a = len(A)
    len_b = len(B)
    i, j = 0, 0
    while i < len_a and j < len_b:
        if A[i] <= B[j]:
            C.append(A[i])
            i=i+1
        else:
            inversions = inversions + len(A)-i 
            C.append(B[j])
            j = j+1
    if i == len_a:
        C.extend(B[j:])
    else:
        C.extend(A[i:])
    return C 

def divide_array(L):
    N = len(L)
    if N > 1:
        left = divide_array(L[0:N/2])
        right = divide_array(L[N/2:])
        return sort_count(left,right)
    else:
        return L


inversions = 0
array = [5,4,3,6,7]
sorted_array = divide_array(array)
print inversions
