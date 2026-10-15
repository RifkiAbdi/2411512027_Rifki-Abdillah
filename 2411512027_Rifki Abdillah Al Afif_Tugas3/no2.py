import random
import time
import multiprocessing as mp

# Jumlah angka acak per proses
N_SAMPLES = 1_000_000
NUM_PROCESSES = 4

# Versi (a): Message Passing (Queue)
def worker_queue(queue):
    subtotal = sum(random.random() for _ in range(N_SAMPLES))
    queue.put(subtotal)

def run_queue_version():
    queue = mp.Queue()
    processes = []
    
    start_time = time.time()
    
    for _ in range(NUM_PROCESSES):
        p = mp.Process(target=worker_queue, args=(queue,))
        processes.append(p)
        p.start()
        
    total = sum(queue.get() for _ in range(NUM_PROCESSES))
    
    for p in processes:
        p.join()
        
    elapsed = time.time() - start_time
    return total, elapsed

# Versi (b): Shared Memory (Value + Lock)
def worker_value(shared_val, lock):
    subtotal = sum(random.random() for _ in range(N_SAMPLES))
    with lock:
        shared_val.value += subtotal

def run_value_version():
    shared_val = mp.Value('d', 0.0)
    lock = mp.Lock()
    processes = []
    
    start_time = time.time()
    
    for _ in range(NUM_PROCESSES):
        p = mp.Process(target=worker_value, args=(shared_val, lock))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    elapsed = time.time() - start_time
    return shared_val.value, elapsed

if __name__ == '__main__':
    print("Pengujian Soal 2:")
    
    total_q, time_q = run_queue_version()
    print(f"[Versi Queue] Total: {total_q:.4f} | Waktu Eksekusi: {time_q:.4f} detik")
    
    total_v, time_v = run_value_version()
    print(f"[Versi Value] Total: {total_v:.4f} | Waktu Eksekusi: {time_v:.4f} detik")