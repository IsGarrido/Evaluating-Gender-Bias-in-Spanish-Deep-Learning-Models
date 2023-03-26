import datetime as dt
import inspect
import os

def log_time(fn):

    if type(fn).__name__ == 'staticmethod':
        fn = fn.__func__
    
    # https://stackoverflow.com/questions/50673566/how-to-get-the-path-of-a-function-in-python
    file = 'file.py'
    try:
        file =os.path.abspath(inspect.getfile(fn)).split('/')[-1]
    except:
        pass

    def wrapper(df, *args, **kwargs):
        tic = dt.datetime.now()
        result = fn(df, *args, **kwargs)
        toc = dt.datetime.now()
        print(f"{file} | {fn.__name__} took {toc - tic }")
        return result
    return wrapper

# https://stackoverflow.com/questions/30382556/python-count-number-of-times-function-passes-through-decorator
log_time_with_counter_calls = {}

def log_time_with_counter(fn):

    if type(fn).__name__ == 'staticmethod':
        fn = fn.__func__
    
    # https://stackoverflow.com/questions/50673566/how-to-get-the-path-of-a-function-in-python
    file = 'file.py'
    try:
        file =os.path.abspath(inspect.getfile(fn)).split('/')[-1]
    except:
        pass

    def wrapper(df, *args, **kwargs):

        uid = file + "_" + fn.__name__
        if uid in log_time_with_counter_calls:
            log_time_with_counter_calls[uid] += 1
        else:
            log_time_with_counter_calls[uid] = 1

        tic = dt.datetime.now()
        result = fn(df, *args, **kwargs)
        toc = dt.datetime.now()
        print(f"[{log_time_with_counter_calls[uid]}] {file} | {fn.__name__} took {toc - tic }")
        return result
    return wrapper