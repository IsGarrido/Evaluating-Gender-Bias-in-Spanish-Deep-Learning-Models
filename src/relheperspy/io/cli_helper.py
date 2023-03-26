import argparse

class CliHelper:

    @staticmethod
    def args(**kwargs):
        
        p = argparse.ArgumentParser()
        for k in kwargs:
            v = kwargs[k]
            p.add_argument(k, nargs='?', default= v)
            
        return p.parse_args()
