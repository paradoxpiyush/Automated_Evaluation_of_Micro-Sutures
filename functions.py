
def zero_interval(arr):
    interval = []
    start, end = 0,0
    for i in range(1, len(arr)-1):
        if arr[i] == 0 and arr[i-1] !=0:
            start = i
        if arr[i] != 0 and arr[i-1] == 0:
            end = i-1
            interval.append((start, end))
    return interval
