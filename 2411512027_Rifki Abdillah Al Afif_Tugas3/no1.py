import math
import multiprocessing as mp
import time
import matplotlib.pyplot as plt


# 1. Fungsi hitung_prima (CPU-bound task)
def hitung_prima(n):
    if n < 2:
        return False
    for i in range(2, int(math.isqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


def hitung_range(start_end):
    start, end = start_end
    return sum(1 for i in range(start, end) if hitung_prima(i))


if __name__ == "__main__":
    LIMIT = 1_000_000
    WORKERS = [1, 2, 4, 8]

    num_chunks = 16
    chunk_size = LIMIT // num_chunks
    ranges = [(i * chunk_size, (i + 1) * chunk_size) for i in range(num_chunks)]

    waktu_eksekusi = []

    # Gunakan 'spawn' agar kompatibel di Windows
    ctx = mp.get_context("spawn")

    for w in WORKERS:
        start_time = time.time()
        with ctx.Pool(processes=w) as pool:
            results = pool.map(hitung_range, ranges)
            total_prima = sum(results)
        elapsed = time.time() - start_time

        waktu_eksekusi.append(elapsed)
        print(
            f"Worker: {w} | Total Prima: {total_prima} | Waktu: {elapsed:.4f} detik"
        )

    # Hitung Speedup Aktual
    t1 = waktu_eksekusi[0]
    speedup_aktual = [t1 / t for t in waktu_eksekusi]

    # Hitung Kurva Teoritis Hukum Amdahl (p = 0.95)
    p = 0.95
    speedup_amdahl = [1 / ((1 - p) + (p / w)) for w in WORKERS]

    # Plot Speedup vs Jumlah Worker
    plt.figure(figsize=(8, 5))
    plt.plot(
        WORKERS,
        speedup_aktual,
        marker="o",
        linewidth=2,
        label="Speedup Aktual (Eksperimen)",
    )
    plt.plot(
        WORKERS,
        speedup_amdahl,
        marker="s",
        linestyle="--",
        color="red",
        label=f"Hukum Amdahl (p={p})",
    )
    plt.plot(
        WORKERS,
        WORKERS,
        linestyle=":",
        color="gray",
        label="Speedup Ideal (Linear)",
    )

    plt.title("Analisis Speedup Skala: Worker vs Speedup")
    plt.xlabel("Jumlah Worker (Processes)")
    plt.ylabel("Speedup (T1 / Tn)")
    plt.xticks(WORKERS)
    plt.legend()
    plt.grid(True)
    plt.show()