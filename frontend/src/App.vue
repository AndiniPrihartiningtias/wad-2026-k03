<template>
  <header style="max-width: 800px; margin: 0 auto; padding: 20px 20px 0 20px;">
    <h1>Pencatat Peminjaman Buku Perpustakaan</h1>
  </header>
  <main style="max-width: 800px; margin: 0 auto; padding: 20px;">
    <SessionForm @created="handleCreate" />

    <StateMessage v-if="loading" message="Memuat data peminjaman buku..." />
    
    <StateMessage v-else-if="error" :message="`Error: ${error}`" :showRetry="true" @retry="loadSessions" />
    
    <StateMessage v-else-if="sessions.length === 0" message="Tidak ada peminjaman buku yang ditemukan." />

    <SessionList v-else :sessions="sessions" v-model:searchQuery="search" @delete="handleDelete" />
  </main>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue';
import { fetchSessions, createSession, deleteSession } from './api/session';
import SessionForm from './components/SessionForm.vue';
import SessionList from './components/SessionList.vue';
import StateMessage from './components/StateMessage.vue';

const sessions = ref([]);
const loading = ref(true);
const error = ref(null);
const search = ref('');
let controller = null;

async function loadSessions() {
  if (controller) controller.abort();
  controller = new AbortController();

  loading.value = true;
  error.value = null;
  try {
    const res = await fetchSessions(search.value);
    sessions.value = res.data;
  } catch (err) {
    if (err.name !== 'AbortError') error.value = err.message;
  } finally {
    loading.value = false;
  }
}

watch(search, () => loadSessions());

async function handleCreate(newSession) {
  await createSession(newSession);
  await loadSessions();
}

async function handleDelete(id) {
  if (confirm('Apakah Anda yakin ingin menghapus data peminjaman ini?')) {
    await deleteSession(id);
    await loadSessions();
  }
}

onMounted(() => loadSessions());
onUnmounted(() => { if (controller) controller.abort(); });
</script>
