import time
import random
import multiprocessing as mp

# Fungsi simulasi tugas berat CPU-bound (menghitung jumlah kuadrat)
def cpu_heavy_task(n):
    return sum(i * i for i in range(n))

# Producer: Memasukkan tugas ke dalam Queue
def producer(queue, num_tasks):
    for i in range(num_tasks):
        item = random.randint(100_000, 500_000)
        queue.put(item)
        print(f"[Producer] Mengirim tugas {i + 1}: size {item}")
    
    # Mengirim sinyal berhenti (Sentinel Value) ke Consumer
    queue.put(None)

# Consumer: Mengambil tugas dari Queue dan memprosesnya
def consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        result = cpu_heavy_task(item)
        print(f"[Consumer] Memproses size {item} -> Hasil: {result}")

if __name__ == '__main__':
    print("Pengujian Soal 3 (Producer-Consumer Multiprocessing):")
    
    queue = mp.Queue()
    num_tasks = 5
    
    start_time = time.time()
    
    p_prod = mp.Process(target=producer, args=(queue, num_tasks))
    p_cons = mp.Process(target=consumer, args=(queue,))
    
    p_prod.start()
    p_cons.start()
    
    p_prod.join()
    p_cons.join()
    
    elapsed = time.time() - start_time
    print(f"Selesai dalam waktu: {elapsed:.4f} detik")