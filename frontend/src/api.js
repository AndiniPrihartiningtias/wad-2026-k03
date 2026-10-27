
const BASE_URL = "http://127.0.0.1:8000"

// Mengambil daftar peminjaman
export async function listSessions(
  { page = 1, limit = 50, search = "" } = {},
  signal
) {
  const params = new URLSearchParams({
    page: String(page),
    limit: String(limit),
    search,
  })

  const res = await fetch(`${BASE_URL}/sessions?${params}`, {
    signal,
  })

  if (!res.ok) {
    throw new Error("Gagal mengambil data dari server")
  }

  return res.json()
}

// Menambahkan data peminjaman
export async function createSession(payload) {
  const res = await fetch(`${BASE_URL}/sessions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))

    throw new Error(
      err.detail
        ? typeof err.detail === "string"
          ? err.detail
          : JSON.stringify(err.detail)
        : "Gagal membuat data"
    )
  }

  return res.json()
}

// Menghapus data peminjaman (khusus admin)
export async function deleteSession(id, token) {
  const res = await fetch(`${BASE_URL}/sessions/${id}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))

    if (res.status === 401) {
      throw new Error("Silakan login terlebih dahulu")
    }

    if (res.status === 403) {
      throw new Error("Hanya admin yang dapat menghapus data")
    }

    if (res.status === 404) {
      throw new Error("Data peminjaman tidak ditemukan")
    }

    throw new Error(
      err.detail
        ? typeof err.detail === "string"
          ? err.detail
          : JSON.stringify(err.detail)
        : "Gagal menghapus data"
    )
  }
}

// Membuat akun baru
export async function register(username, password) {
  const res = await fetch(`${BASE_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username,
      password,
    }),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))

    if (res.status === 409) {
      throw new Error("Username sudah digunakan.")
    }

    throw new Error(
      err.detail
        ? typeof err.detail === "string"
          ? err.detail
          : JSON.stringify(err.detail)
        : "Gagal membuat akun."
    )
  }

  return res.json()
}

// Login untuk mendapatkan token JWT
export async function login(username, password) {
  const formData = new URLSearchParams()
  formData.append("username", username)
  formData.append("password", password)

  const res = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: formData,
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))

    throw new Error(
      typeof err.detail === "string"
        ? err.detail
        : "Username atau password salah"
    )
  }

  return res.json()
}

// Mengambil profil pengguna yang sedang login
export async function getMe(token) {
  const res = await fetch(`${BASE_URL}/me`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!res.ok) {
    throw new Error("Gagal mengambil profil pengguna")
  }

  return res.json()
}

// Memperbarui username atau password pengguna
export async function updateMe(token, username, password = "") {
  const payload = { username }

  // Password hanya dikirim jika diisi
  if (password) {
    payload.password = password
  }

  const res = await fetch(`${BASE_URL}/me`, {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(payload),
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))

    if (res.status === 401) {
      throw new Error("Sesi login berakhir. Silakan login kembali.")
    }

    throw new Error(
      typeof err.detail === "string"
        ? err.detail
        : "Gagal memperbarui data pengguna."
    )
  }

  return res.json()
}
