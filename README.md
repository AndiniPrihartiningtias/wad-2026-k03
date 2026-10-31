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
*   **A5 (Salsa):** Integrator & Quality Assurance (Testing, Bug Fixing, Video Demo, & Dokumentasi)

---

## 🚀 Cara Menjalankan Aplikasi (Setup)

### 1. Prasyarat (Prerequisites)
Pastikan Anda sudah menginstall **Python** dan **Node.js** di komputer Anda.

### 2. Konfigurasi Environment (.env) - *PENTING!*
Aplikasi ini menggunakan JWT Secret Key. Jika tidak dikonfigurasi, Backend akan error 500.
1. Duplikat file `.env.example` dan ubah namanya menjadi **`.env`**.
2. Buka file `.env` dan pastikan berisi baris berikut:
   ```env
   JWT_SECRET_KEY=rahasia_kelompok_k03
