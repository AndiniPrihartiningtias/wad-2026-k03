<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { listSessions } from '../api.js'
import SessionItem from './SessionItem.vue'

const props = defineProps({
  isAdmin: {
    type: Boolean,
    default: false,
  },
  token: {
    type: String,
    default: '',
  },
})

const status = ref('loading')
const items = ref([])
const errorMsg = ref('')
let controller = null

async function load() {
  controller?.abort()
  controller = new AbortController()

  status.value = 'loading'
  errorMsg.value = ''

  try {
    const data = await listSessions(
      { page: 1, limit: 50 },
      controller.signal,
    )

    items.value = Array.isArray(data)
      ? data
      : data.items ?? []

    status.value = items.value.length ? 'data' : 'empty'
  } catch (err) {
    if (err.name === 'AbortError') return

    errorMsg.value = err.message || 'Gagal memuat data.'
    status.value = 'error'
  }
}

onMounted(load)

onUnmounted(() => {
  controller?.abort()
})

defineExpose({
  status,
  items,
  errorMsg,
  load,
})
</script>

<template>
  <div>
    <p v-if="status === 'loading'">
      Memuat data...
    </p>

    <div v-else-if="status === 'error'">
      <p role="alert">{{ errorMsg }}</p>
      <button type="button" @click="load">
        Coba lagi
      </button>
    </div>

    <p v-else-if="status === 'empty'">
      Belum ada data peminjaman.
    </p>

    <table v-else>
      <thead>
        <tr>
          <th scope="col">Judul Buku</th>
          <th scope="col">Nama Peminjam</th>
          <th scope="col">Status</th>
          <th scope="col">Aksi</th>
        </tr>
      </thead>

      <tbody>
        <SessionItem
          v-for="item in items"
          :key="item.id"
          :item="item"
          :is-admin="props.isAdmin"
          :auth-value="props.token"
          @deleted="load"
        />
      </tbody>
    </table>
  </div>
</template>