import time
def calculate_function_time(func, *args, **kwargs):
    start = time.time()
    func(*args, **kwargs)
    end = time.time()
    print("Time passed:", end - start, "seconds")
    return end - start