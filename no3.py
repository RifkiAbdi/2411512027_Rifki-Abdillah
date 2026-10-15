# Import library yang digunakan
import asyncio
import random


# Fungsi producer untuk memasukkan item ke dalam priority queue
async def producer(queue, nama_producer, jumlah_item):
    for i in range(jumlah_item):
        prioritas = random.randint(1, 5)
        item = f"item-{nama_producer}-{i}"

        await queue.put((prioritas, item))

        print(
            f"[{nama_producer}] menghasilkan {item} "
            f"dengan prioritas {prioritas}"
        )

        await asyncio.sleep(random.uniform(0.1, 0.3))


# Fungsi consumer untuk mengambil item berdasarkan prioritas
async def consumer(queue, nama_consumer):
    while True:
        prioritas, item = await queue.get()

        print(
            f"[{nama_consumer}] memproses {item} "
            f"dengan prioritas {prioritas}"
        )

        await asyncio.sleep(random.uniform(0.2, 0.5))

        queue.task_done()


# Fungsi utama program
async def main():
    # Membuat priority queue
    queue = asyncio.PriorityQueue()

    # Membuat beberapa producer
    producer_tasks = [
        asyncio.create_task(producer(queue, "Producer-1", 5)),
        asyncio.create_task(producer(queue, "Producer-2", 5)),
    ]

    # Membuat beberapa consumer
    consumer_tasks = [
        asyncio.create_task(consumer(queue, "Consumer-1")),
        asyncio.create_task(consumer(queue, "Consumer-2")),
    ]

    # Menunggu semua producer selesai
    await asyncio.gather(*producer_tasks)

    # Menunggu semua item dalam queue selesai diproses
    await queue.join()

    # Menghentikan consumer
    for task in consumer_tasks:
        task.cancel()

    await asyncio.gather(*consumer_tasks, return_exceptions=True)

    print("\nSemua item sudah selesai diproses.")


# Menjalankan program utama
asyncio.run(main())