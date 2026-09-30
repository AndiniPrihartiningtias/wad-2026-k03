const BASE_URL = "http://127.0.0.1:8000"

export async function listSessions({ page = 1, page_size = 50, search = "" } = {}, signal) {
  const params = new URLSearchParams({ page, page_size, search })
  const res = await fetch(`${BASE_URL}/sessions?${params}`, { signal })
  if (!res.ok) throw new Error("Gagal mengambil data dari server")
  return res.json()
}

export async function createSession(payload) {
  const res = await fetch(`${BASE_URL}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail ? JSON.stringify(err.detail) : "Gagal membuat data")
  }
  return res.json()
}

export async function deleteSession(id) {
  const res = await fetch(`${BASE_URL}/sessions/${id}`, { method: "DELETE" })
  if (!res.ok) throw new Error("Gagal menghapus data")
}