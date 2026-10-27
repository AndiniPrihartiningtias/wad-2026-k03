<script setup>
import { deleteSession } from '../api.js'

const props = defineProps({
  item: {
    type: Object,
    required: true,
  },
  isAdmin: {
    type: Boolean,
    default: false,
  },
  token: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['deleted'])

async function remove() {
  if (!props.isAdmin) {
    window.alert('Hanya admin yang dapat menghapus data.')
    return
  }

  if (!props.token) {
    window.alert('Silakan login terlebih dahulu.')
    return
  }

  const confirmed = window.confirm(
    `Yakin ingin menghapus peminjaman "${props.item.book_title}"?`
  )

  if (!confirmed) return

  try {
    await deleteSession(props.item.id, props.token)
    emit('deleted')
  } catch (err) {
    window.alert(err.message || 'Gagal menghapus data.')
  }
}
</script>

<template>
  <tr class="session-item">
    <td>{{ item.book_title }}</td>
    <td>{{ item.borrower_name }}</td>
    <td>{{ item.status }}</td>
    <td>
      <button
        v-if="isAdmin"
        type="button"
        @click="remove"
        :aria-label="`Hapus peminjaman ${item.book_title}`"
      >
        Hapus
      </button>

      <span v-else>-</span>
    </td>
  </tr>
</template>

<style scoped>
.session-item button {
  margin-left: 12px;
  cursor: pointer;
}
</style>