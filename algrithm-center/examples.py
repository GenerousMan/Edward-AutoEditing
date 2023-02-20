import sys
sys.path.append('edit')
from edit import api

if __name__ == "__main__":
    # folder = '../examples/senma-1'
    # folder = '../examples/senma-2'
    # folder = '../examples/white-girl'
    folder = '../examples/blue-boy'
    api.pp_example(folder)
    pass