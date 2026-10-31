# 📚 Sistem Pencatatan Peminjaman Buku (UAS WAD 2026)

Proyek ini adalah kelanjutan dari UTS (Ujian Tengah Semester) yang kini telah dikembangkan dengan fitur **Authentication (JWT)**, **Authorization (Role-based)**, dan **Database (SQLite)** untuk memenuhi tugas UAS.

## 🛠️ Teknologi yang Digunakan
*   **Backend:** Python (FastAPI), SQLAlchemy, SQLite
*   **Frontend:** Vue 3 (Vite), Vue Router
*   **Security:** JWT (JSON Web Token), Passlib (Bcrypt)

## 👥 Pembagian Tugas (Kelompok K03)
*   **Haikal:** Backend Lead (JWT Authentication & Security)
*   **Zaen:** Backend Support (Database SQLite & User Models)
*   **Nacwa:** Frontend State Lead (Login UI, API Interceptor & Router Guard)
*   **Andini:** Frontend Form (Create Account & Update Form UI)
*   **Salsa:** Integrator & Quality Assurance (Testing, Bug Fixing, Video Demo, & Dokumentasi)

---

## 🚀 Cara Menjalankan Aplikasi (Setup)

### 1. Prasyarat (Prerequisites)
Pastikan Anda sudah menginstall **Python** dan **Node.js** di komputer Anda.

## 2. Layanan
Aplikasi ini menyediakan layanan berupa:
- **Sistem Pencatatan Peminjaman Buku:** Mengelola data peminjaman (Create, Read, Update, Delete).
- **Autentikasi (Login):** Mengamankan akses aplikasi menggunakan JWT (JSON Web Token).
- **Otorisasi (Role-Based):** Membatasi fitur berdasarkan role pengguna (Admin dan User biasa).

### 3. Konfigurasi Environment (.env) - *PENTING!*
Aplikasi ini menggunakan JWT Secret Key. Jika tidak dikonfigurasi, Backend akan error 500.
1. Duplikat file `.env.example` dan ubah namanya menjadi **`.env`**

## 4. Cara Memverifikasi
Untuk memastikan aplikasi berjalan dengan baik, ikuti langkah berikut:
1. Jalankan Backend dan Frontend sesuai instruksi di atas.
2. Buka `http://127.0.0.1:8000/docs` untuk memastikan API Backend menyala.
3. Buka `http://localhost:5173` di browser.
4. Lakukan Login menggunakan akun demo.
5. Pastikan form peminjaman muncul setelah login dan data dapat ditambahkan.

## 5. Masalah yang Sering Muncul
- **Error 500 (Internal Server Error) saat Login:** Pastikan file `.env` sudah dibuat (copy dari `.env.example`) dan berisi `JWT_SECRET_KEY`.
- **Failed to fetch di Frontend:** Pastikan server Backend (uvicorn) sedang menyala di port 8000, dan konfigurasi CORS di backend sudah mengizinkan alamat frontend.
- **Akun tidak bisa login:** Pastikan akun sudah terdaftar di database (lakukan Create Account terlebih dahulu).
  .
4. Buka file `.env` dan pastikan berisi baris beriku```env
   JWT_SECRET_KEY=rahasia_kelompok_k03
