<script setup>
import { deleteSession } from '../api.js'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['deleted'])

async function remove() {
  const confirmed = window.confirm(
    `Yakin ingin menghapus sesi "${props.item.book_title}"?`
  )

  if (!confirmed) return

  try {
    await deleteSession(props.item.id)

    // Memberi tahu SessionList bahwa data berhasil dihapus
    emit('deleted')
  } catch (err) {
    window.alert(err.message)
  }
}
</script>

<template>
  <tr class="session-item">
    <td>{{ item.book_title }}</td>
    <td>{{ item.borrower_name }}</td>
    <td>
      <button
        type="button"
        @click="remove"
        :aria-label="`Hapus sesi ${item.book_title}`"
      >
        Delete
      </button>
    </td>
  </tr>
</template>

<style scoped>
.session-item button {
  margin-left: 12px;
}
</style>