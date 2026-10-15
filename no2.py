# Import library yang digunakan
import asyncio
import time


# Coroutine yang menggunakan asyncio.sleep()
async def coroutine_asyncio_sleep():
    print("[asyncio.sleep] Mulai")

    await asyncio.sleep(2)

    print("[asyncio.sleep] Selesai")


# Coroutine yang menggunakan time.sleep()
async def coroutine_time_sleep():
    print("[time.sleep] Mulai")

    time.sleep(2)

    print("[time.sleep] Selesai")


# Coroutine dengan proses CPU-bound
async def coroutine_cpu_bound():
    print("[CPU-bound] Mulai")

    hasil = 0

    for i in range(20_000_000):
        hasil += i

    print("[CPU-bound] Selesai")


# Coroutine pengukur untuk mengamati event loop
async def pengukur():
    print("[Pengukur] Mulai")

    waktu_mulai = time.perf_counter()

    for i in range(10):
        await asyncio.sleep(0.2)

        waktu_sekarang = time.perf_counter()
        selisih = waktu_sekarang - waktu_mulai

        print(f"[Pengukur] Detik ke-{selisih:.2f}")

    print("[Pengukur] Selesai")


# Fungsi utama untuk menjalankan semua coroutine
async def main():
    await asyncio.gather(
        coroutine_asyncio_sleep(),
        coroutine_time_sleep(),
        coroutine_cpu_bound(),
        pengukur()
    )


# Menjalankan program utama
asyncio.run(main())