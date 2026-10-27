<script setup>
import { ref } from 'vue'
import { register } from '../api.js'

const username = ref('')
const password = ref('')
const message = ref('')
const error = ref('')
const loading = ref(false)

async function submitForm() {
  message.value = ''
  error.value = ''

  if (!username.value.trim() || !password.value) {
    error.value = 'Username dan password wajib diisi.'
    return
  }

  if (password.value.length < 8) {
    error.value = 'Password minimal 8 karakter.'
    return
  }

  loading.value = true

  try {
    await register(username.value.trim(), password.value)

    message.value = 'Akun berhasil dibuat. Silakan login.'
    username.value = ''
    password.value = ''
  } catch (err) {
    error.value = err.message || 'Gagal membuat akun.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="user-form">
    <h2>Create Account</h2>
    <p>Buat akun pengguna baru.</p>

    <form @submit.prevent="submitForm">
      <div class="form-group">
        <label for="username">Username</label>
        <input
          id="username"
          v-model="username"
          type="text"
          autocomplete="username"
          placeholder="Masukkan username"
          minlength="3"
          maxlength="50"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          autocomplete="new-password"
          placeholder="Minimal 8 karakter"
          minlength="8"
          maxlength="128"
          required
        />
      </div>

      <button type="submit" :disabled="loading">
        {{ loading ? 'Membuat akun...' : 'Buat Akun' }}
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
.user-form {
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

.user-form button {
  padding: 10px 16px;
  cursor: pointer;
}

.user-form button:disabled {
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
