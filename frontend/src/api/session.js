const BASE_URL = "http://localhost:8000";

async function handleResponse(res) {
  if (!res.ok) {
    let message = `HTTP ${res.status}`;
    try {
      const body = await res.json();
      if (body.detail) {
        message = Array.isArray(body.detail)
          ? body.detail.map((e) => e.msg || JSON.stringify(e)).join("; ")
          : String(body.detail);
      }
    } catch (_) { /* ignore */ }
    throw new Error(message);
  }
  if (res.status === 204) return null;
  return res.json();
}

export async function listSessions(
  { page = 1, page_size = 50, search = "" } = {},
  signal
) {
  const params = new URLSearchParams({ page, page_size });
  if (search) params.set("search", search);
  const res = await fetch(`${BASE_URL}/sessions?${params}`, { signal });
  return handleResponse(res);
}

export async function createSession(payload) {
  const res = await fetch(`${BASE_URL}/sessions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return handleResponse(res);
}

export async function deleteSession(id) {
  const res = await fetch(`${BASE_URL}/sessions/${id}`, { method: "DELETE" });
  return handleResponse(res);
}