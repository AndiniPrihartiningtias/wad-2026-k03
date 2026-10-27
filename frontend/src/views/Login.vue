<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login, getMe } from '../api.js'
import UserForm from '../components/UserForm.vue'

const router = useRouter()

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

async function handleLogin() {
  errorMessage.value = ''

  if (!username.value.trim() || !password.value) {
    errorMessage.value = 'Username dan password wajib diisi.'
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

    localStorage.setItem('access_token', accessToken)
    localStorage.removeItem('token')
    localStorage.removeItem('role')

    // Simpan role dari profil backend
    localStorage.setItem('role', user.role)

    password.value = ''
    await router.push('/')
  } catch (err) {
    errorMessage.value = err.message || 'Login gagal.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main>
    <header>
      <h1>Pencatatan Peminjaman Buku</h1>
      <p>Silakan login menggunakan akun yang sudah terdaftar.</p>
    </header>

    <section class="login-form">
      <h2>Login</h2>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            autocomplete="username"
            placeholder="Masukkan username"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
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

        <p v-if="errorMessage" class="error-message" role="alert">
          {{ errorMessage }}
        </p>
      </form>
    </section>

    <section class="register-form">
      <h2>Registrasi Akun</h2>
      <p>Belum memiliki akun? Daftar melalui formulir berikut.</p>
      <UserForm />
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
.register-form {
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

button {
  padding: 10px 16px;
  cursor: pointer;
}

button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.error-message {
  color: #c62828;
}
</style>
