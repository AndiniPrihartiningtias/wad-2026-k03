<script setup>
import { ref, onMounted } from 'vue'
import { login, getMe } from './api.js'

import SessionList from './components/SessionList.vue'
import SessionForm from './components/SessionForm.vue'
import UserForm from './components/UserForm.vue'
import UpdateForm from './components/UpdateForm.vue'

const listRef = ref(null)

const username = ref('')
const password = ref('')
const token = ref('')
const currentUsername = ref('')
const currentRole = ref('')
const loginError = ref('')
const loginMessage = ref('')
const loading = ref(false)

const isLoggedIn = ref(false)
const isAdmin = ref(false)

// Memuat sesi login yang tersimpan
onMounted(async () => {
  const savedToken = localStorage.getItem('access_token')

  if (!savedToken) return

  try {
    const user = await getMe(savedToken)

    token.value = savedToken
    currentUsername.value = user.username
    currentRole.value = user.role
    isLoggedIn.value = true
    isAdmin.value = user.role === 'admin'
  } catch {
    localStorage.removeItem('access_token')
  }
})

// Login menggunakan backend
async function onLogin() {
  loginError.value = ''
  loginMessage.value = ''

  if (!username.value.trim() || !password.value) {
    loginError.value = 'Username dan password wajib diisi.'
    return
  }

  loading.value = true

  try {
    const result = await login(
      username.value.trim(),
      password.value,
    )

    const accessToken = result.access_token
    const user = await getMe(accessToken)

    token.value = accessToken
    currentUsername.value = user.username
    currentRole.value = user.role
    isLoggedIn.value = true
    isAdmin.value = user.role === 'admin'

    localStorage.setItem('access_token', accessToken)

    password.value = ''
    loginMessage.value = 'Login berhasil.'
    listRef.value?.load()
  } catch (err) {
    loginError.value = err.message || 'Login gagal.'
  } finally {
    loading.value = false
  }
}

// Logout
function onLogout() {
  localStorage.removeItem('access_token')

  token.value = ''
  currentUsername.value = ''
  currentRole.value = ''
  username.value = ''
  password.value = ''

  isLoggedIn.value = false
  isAdmin.value = false
  loginError.value = ''
  loginMessage.value = ''
}

// Refresh daftar setelah peminjaman dibuat
function onCreated() {
  listRef.value?.load()
}

// Memperbarui informasi setelah profil diubah
function onUserUpdated(user) {
  if (user?.username) {
    currentUsername.value = user.username
  }

  if (user?.role) {
    currentRole.value = user.role
    isAdmin.value = user.role === 'admin'
  }
}
</script>

<template>
  <main>
    <header>
      <h1>Pencatatan Peminjaman Buku</h1>
      <p>Aplikasi pengelolaan data peminjaman buku.</p>
    </header>

    <section>
      <!-- Form registrasi -->
      <UserForm />

      <!-- Form login -->
      <section class="login-form">
        <h2>Login</h2>
        <p>Masuk menggunakan akun yang sudah terdaftar.</p>

        <form @submit.prevent="onLogin">
          <div class="form-group">
            <label for="login-username">Username</label>
            <input
              id="login-username"
              v-model="username"
              type="text"
              autocomplete="username"
              placeholder="Masukkan username"
              required
            />
          </div>

          <div class="form-group">
            <label for="login-password">Password</label>
            <input
              id="login-password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              placeholder="Masukkan password"
              required
            />
          </div>

          <button type="submit" :disabled="loading">
            {{ loading ? 'Memproses...' : 'Login' }}
          </button>

          <p v-if="loginError" class="error-message" role="alert">
            {{ loginError }}
          </p>

          <p v-if="loginMessage" class="success-message" role="status">
            {{ loginMessage }}
          </p>
        </form>
      </section>

      <!-- Informasi pengguna yang login -->
      <section v-if="isLoggedIn" class="account-info">
        <h2>Akun Saya</h2>
        <p>Username: {{ currentUsername }}</p>
        <p>Role: {{ currentRole }}</p>

        <button type="button" @click="onLogout">
          Logout
        </button>
      </section>

      <!-- Update profil hanya untuk pengguna yang login -->
      <UpdateForm
        v-if="isLoggedIn"
        :token="token"
        :current-username="currentUsername"
        @updated="onUserUpdated"
      />

      <!-- Form peminjaman -->
      <SessionForm @created="onCreated" />

      <!-- Daftar peminjaman -->
      <SessionList
        ref="listRef"
        :is-admin="isAdmin"
        :token="token"
      />
    </section>
  </main>
</template>

<style scoped>
main {
  max-width: 1000px;
  margin: 0 auto;
  padding: 24px;
}

header {
  margin-bottom: 24px;
}

.login-form,
.account-info {
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

.login-form button,
.account-info button {
  padding: 10px 16px;
  cursor: pointer;
}

.login-form button:disabled {
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