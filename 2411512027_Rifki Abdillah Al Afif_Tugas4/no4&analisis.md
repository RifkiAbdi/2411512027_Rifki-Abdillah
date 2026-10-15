# Tugas Individu 4 - Pemrograman Paralel

Nama: Rifki Abdillah AL Afif
NIM: 2411512027
Mata Kuliah: Pemrograman Paralel  

---

# Tugas 1 - Eksperimen Skala

## Tujuan

Percobaan ini bertujuan untuk mengetahui pengaruh batas konkurensi terhadap waktu yang dibutuhkan untuk menjalankan beberapa proses pengambilan data secara asynchronous.

Program menggunakan `asyncio`, `aiohttp`, dan `asyncio.Semaphore`. Data yang digunakan berupa informasi package dari PyPI. Pengujian dilakukan dengan beberapa batas konkurensi, yaitu 1, 3, 5, 10, dan 20.

## Hasil Percobaan

Program mengukur waktu yang dibutuhkan untuk menyelesaikan seluruh request pada setiap batas konkurensi.
Batas konkurensi 1: 5.25 detik
Batas konkurensi 3: 2.93 detik
Batas konkurensi 5: 2.08 detik
Batas konkurensi 10: 3.15 detik
Batas konkurensi 20: 2.70 detik

Hasil pengujian kemudian divisualisasikan dalam bentuk grafik.

## Analisis

Berdasarkan percobaan, perubahan batas konkurensi memengaruhi waktu penyelesaian seluruh request. Ketika batas konkurensi dibuat lebih besar, beberapa request dapat diproses secara concurrent sehingga waktu total cenderung menjadi lebih kecil. Pada batas konkurensi 1, request dijalankan secara bergantian sehingga proses membutuhkan waktu lebih lama. Ketika batas dinaikkan menjadi 3, 5, 10, dan 20, lebih banyak request dapat berjalan pada waktu yang sama. Namun, peningkatan batas konkurensi tidak selalu berarti peningkatan performa tanpa batas. Semakin banyak request yang dijalankan secara bersamaan, semakin besar pula penggunaan sumber daya dan beban pada koneksi jaringan maupun server. Oleh karena itu, diperlukan batas konkurensi yang sesuai dengan kondisi sistem. Percobaan ini menunjukkan salah satu penggunaan asyncio untuk menangani pekerjaan yang bersifat I/O-bound, khususnya ketika program harus menunggu respons dari jaringan.


## Tugas 2 - Deteksi Blocking Call
## Tujuan

Percobaan ini bertujuan untuk mengamati pengaruh operasi blocking terhadap event loop asyncio. Program membandingkan tiga jenis pekerjaan, yaitu:
asyncio.sleep()
time.sleep()
Proses CPU-bound

Selain itu, digunakan coroutine pengukur untuk mengamati jalannya event loop selama program dijalankan.

## Hasil Percobaan

Program menjalankan beberapa coroutine secara concurrent menggunakan asyncio.gather(). asyncio.sleep() dapat memberikan kesempatan kepada event loop untuk menjalankan coroutine lain selama coroutine tersebut menunggu. Sebaliknya, time.sleep() menghentikan eksekusi thread sehingga event loop tidak dapat menjalankan coroutine lain selama proses tersebut berlangsung. ##Proses CPU-bound juga dapat menghambat event loop karena melakukan perhitungan dalam jumlah besar tanpa memberikan kesempatan kepada event loop melalui await.

## Analisis

Hasil percobaan menunjukkan bahwa tidak semua fungsi yang berada di dalam coroutine bersifat non-blocking.asyncio.sleep() merupakan operasi yang sesuai dengan mekanisme asynchronous karena menggunakan await. Saat menunggu, kontrol dapat dikembalikan kepada event loop sehingga coroutine lain dapat dijalankan. Berbeda dengan asyncio.sleep(), penggunaan time.sleep() di dalam coroutine dapat memblokir event loop. Selama time.sleep() berlangsung, coroutine lain tidak dapat berjalan dengan normal. Hal yang sama terjadi pada proses CPU-bound. Meskipun fungsi tersebut dibuat dengan async def, proses perhitungan yang panjang tetap dapat menghambat event loop apabila tidak memiliki mekanisme untuk memberikan kesempatan kepada tugas lain. Dari percobaan ini dapat dipahami bahwa penggunaan asyncio tidak secara otomatis membuat seluruh proses menjadi asynchronous. Operasi yang bersifat blocking tetap dapat menghambat event loop.


## Tugas 3 - Producer-Multi-Consumer dengan Prioritas
## Tujuan

Percobaan ini bertujuan untuk membuat sistem producer dan multi-consumer menggunakan asyncio.PriorityQueue. Program menggunakan dua producer dan dua consumer. Setiap producer menghasilkan beberapa item dan memberikan nilai prioritas pada setiap item. Nilai prioritas yang lebih kecil memiliki tingkat prioritas yang lebih tinggi.

## Cara Kerja Program

Producer menghasilkan item kemudian memasukkannya ke dalam PriorityQueue dalam bentuk:(prioritas, item) Consumer mengambil item dari queue dan memprosesnya. Karena menggunakan PriorityQueue, item dengan nilai prioritas yang lebih kecil akan lebih diutamakan ketika consumer mengambil item dari queue. Dua producer dan dua consumer dijalankan secara concurrent menggunakan asyncio.

## Hasil Percobaan

Program menampilkan proses ketika producer menghasilkan item dan ketika consumer mengambil serta memproses item tersebut.
Contoh:
[Producer-1] menghasilkan item-Producer-1-0 dengan prioritas 2
[Producer-2] menghasilkan item-Producer-2-0 dengan prioritas 1
[Consumer-1] memproses item-Producer-2-0 dengan prioritas 1
Urutan output dapat berbeda setiap kali program dijalankan karena terdapat proses asynchronous dan nilai prioritas yang dihasilkan secara acak.

## Analisis

Penggunaan asyncio.PriorityQueue memungkinkan item yang berada di dalam queue diproses berdasarkan tingkat prioritas. Nilai prioritas yang lebih kecil akan dipilih terlebih dahulu oleh consumer ketika item tersebut sudah tersedia di dalam queue. Dengan demikian, sistem dapat digunakan ketika terdapat pekerjaan yang memiliki tingkat kepentingan berbeda. Penggunaan dua producer memungkinkan beberapa sumber menghasilkan pekerjaan secara concurrent. Sementara itu, dua consumer memungkinkan beberapa pekerjaan diproses secara concurrent. Penggunaan queue.join() memastikan program menunggu sampai seluruh item yang telah dimasukkan ke queue selesai diproses. Setelah seluruh pekerjaan selesai, consumer dihentikan menggunakan task.cancel(). Percobaan ini menunjukkan bagaimana asyncio dapat digunakan untuk membuat sistem producer-consumer tanpa menggunakan thread tambahan. PriorityQueue juga dapat digunakan untuk mengatur urutan pekerjaan berdasarkan prioritas.

## Tugas 4 - Refleksi
## Perbandingan asyncio, threading, dan multiprocessing

Menurut saya, asyncio merupakan metode yang paling sesuai untuk menangani pekerjaan yang banyak melakukan proses I/O-bound, seperti komunikasi jaringan atau menunggu respons dari suatu layanan. Dengan mekanisme async dan await, beberapa pekerjaan dapat dijalankan secara concurrent tanpa harus membuat banyak thread.

threading juga dapat digunakan untuk menjalankan beberapa pekerjaan secara concurrent, terutama ketika program perlu menangani beberapa tugas yang menunggu I/O. Namun, penggunaan thread memiliki pengelolaan yang lebih kompleks dibandingkan coroutine asyncio.

Sementara itu, multiprocessing lebih sesuai untuk pekerjaan yang membutuhkan pemrosesan CPU karena proses dijalankan pada process yang berbeda. Metode ini dapat digunakan untuk pekerjaan komputasi yang berat, tetapi membutuhkan sumber daya yang lebih besar dibandingkan coroutine.

Berdasarkan percobaan, asyncio lebih cocok untuk pekerjaan I/O-bound, threading dapat digunakan untuk concurrency berbasis thread, sedangkan multiprocessing lebih sesuai untuk pekerjaan CPU-bound. Pemilihan metode sebaiknya disesuaikan dengan jenis pekerjaan yang akan dijalankan.