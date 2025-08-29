import time
def calculate_function_time(func, *args, **kwargs):
    start = time.perf_counter()
    func(*args, **kwargs)
    end = time.perf_counter()
    print("Time passed:", end - start, "seconds")
    return end - start