<script setup>
import { ref, watch } from 'vue'
import { updateMe } from '../api.js'

const props = defineProps({
  token: {
    type: String,
    default: '',
  },
  currentUsername: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['updated'])

const username = ref('')
const password = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

watch(
  () => props.currentUsername,
  (value) => {
    username.value = value
  },
  { immediate: true },
)

async function submitForm() {
  message.value = ''
  error.value = ''

  if (!props.token) {
    error.value = 'Silakan login terlebih dahulu.'
    return
  }

  if (!username.value.trim()) {
    error.value = 'Username wajib diisi.'
    return
  }

  if (username.value.trim().length < 3) {
    error.value = 'Username minimal 3 karakter.'
    return
  }

  if (password.value && password.value.length < 8) {
    error.value = 'Password baru minimal 8 karakter.'
    return
  }

  loading.value = true

  try {
    const result = await updateMe(
      props.token,
      username.value.trim(),
      password.value,
    )

    message.value = 'Data pengguna berhasil diperbarui.'
    password.value = ''

    emit('updated', result)
  } catch (err) {
    error.value = err.message || 'Gagal memperbarui data.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="update-form">
    <h2>Update Data Pengguna</h2>
    <p>Ubah username atau password akun.</p>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="update-username">Username baru</label>
        <input
          id="update-username"
          v-model="username"
          type="text"
          autocomplete="username"
          placeholder="Masukkan username baru"
          minlength="3"
          maxlength="50"
          required
        />
      </div>

      <div class="form-group">
        <label for="update-password">
          Password baru (opsional)
        </label>
        <input
          id="update-password"
          v-model="password"
          type="password"
          autocomplete="new-password"
          placeholder="Kosongkan jika tidak ingin mengubah"
          minlength="8"
          maxlength="128"
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Menyimpan...' : 'Simpan Perubahan' }}
      </button>

      <p v-if="error" class="error-message" role="alert">
        {{ error }}
      </p>

      <p v-if="message" class="success-message" role="status">
        {{ message }}
      </p>
    </form>
  </section>
</template>

<style scoped>
.update-form {
  max-width: 420px;
  margin: 24px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.update-form button {
  padding: 10px 16px;
  cursor: pointer;
}

.update-form button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  color: #c62828;
}

.success-message {
  color: #237a3b;
}
</style>