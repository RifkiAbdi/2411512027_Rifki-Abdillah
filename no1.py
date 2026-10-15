# Import library yang digunakan
import aiohttp
import asyncio
import time
import matplotlib.pyplot as plt


# Daftar 20 package PyPI yang akan diuji
daftar_paket_banyak = [
    "numpy",
    "pandas",
    "requests",
    "flask",
    "django",
    "fastapi",
    "scipy",
    "matplotlib",
    "pillow",
    "sqlalchemy",
    "pytest",
    "aiohttp",
    "beautifulsoup4",
    "sympy",
    "scikit-learn",
    "openpyxl",
    "seaborn",
    "jupyter",
    "torch",
    "tensorflow"
]


# Fungsi untuk mengambil data package dengan batas konkurensi
async def ambil_dengan_batas(session, nama_paket, semaphore):
    async with semaphore:
        url = f"https://pypi.org/pypi/{nama_paket}/json"

        async with session.get(url) as response:
            await response.json()

        return nama_paket


# Fungsi untuk menjalankan seluruh request dengan batas konkurensi tertentu
async def jalankan(batas_konkurensi):
    semaphore = asyncio.Semaphore(batas_konkurensi)

    # Mulai menghitung waktu
    mulai = time.perf_counter()

    # Membuat session HTTP untuk request ke PyPI
    async with aiohttp.ClientSession() as session:
        tugas = [
            ambil_dengan_batas(session, nama_paket, semaphore)
            for nama_paket in daftar_paket_banyak
        ]

        # Menjalankan seluruh tugas secara concurrent
        await asyncio.gather(*tugas)

    # Selesai menghitung waktu
    selesai = time.perf_counter()

    return selesai - mulai


# Menyimpan hasil waktu dari setiap batas konkurensi
hasil_waktu = []


# Menguji beberapa nilai batas konkurensi
for batas in [1, 3, 5, 10, 20]:
    waktu = asyncio.run(jalankan(batas))

    # Menyimpan batas konkurensi dan waktu hasil pengujian
    hasil_waktu.append((batas, waktu))

    # Menampilkan hasil pengujian
    print(f"Batas konkurensi {batas}: {waktu:.2f} detik")


# Memisahkan data batas konkurensi dan waktu untuk grafik
batas = [data[0] for data in hasil_waktu]
waktu = [data[1] for data in hasil_waktu]


# Membuat grafik perbandingan waktu
plt.plot(batas, waktu, marker="o")

# Memberikan nama pada sumbu grafik
plt.xlabel("Batas Konkurensi")
plt.ylabel("Waktu Total (detik)")

# Memberikan judul grafik
plt.title("Waktu terhadap Batas Konkurensi")

# Menampilkan garis bantu pada grafik
plt.grid(True)

# Menampilkan grafik
plt.show()