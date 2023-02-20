from multiprocessing import Lock

def init_():
    global gpu_lock
    gpu_lock = Lock()

def get_gpu_lock():
    return gpu_lock