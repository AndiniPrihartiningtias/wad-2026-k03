<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { listSessions } from '../api/session.js'
import SessionItem from './SessionItem.vue'

const status = ref('loading')   // 'loading' | 'data' | 'empty' | 'error'
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
      { page: 1, page_size: 50 },
      controller.signal
    )

    items.value = data.items ?? data
    status.value = items.value.length ? 'data' : 'empty'
  } catch (err) {
    if (err.name === 'AbortError') return

    errorMsg.value = err.message
    status.value = 'error'
  }
}

onMounted(load)

onUnmounted(() => {
  controller?.abort()
})

defineExpose({ status, items, errorMsg, load })
</script>

<template>
  <div>
    <p v-if="status === 'loading'">
      Memuat data...
    </p>

    <p v-else-if="status === 'error'">
      {{ errorMsg }}
      <button type="button" @click="load">
        Coba lagi
      </button>
    </p>

    <p v-else-if="status === 'empty'">
      Belum ada sesi peminjaman.
    </p>

    <table v-else>
      <thead>
        <tr>
          <th scope="col">Judul Buku</th>
          <th scope="col">Nama Peminjam</th>
          <th scope="col">Aksi</th>
        </tr>
      </thead>

      <tbody>
        <SessionItem
          v-for="item in items"
          :key="item.id"
          :item="item"
          @deleted="load"
        />
      </tbody>
    </table>
  </div>
</template>