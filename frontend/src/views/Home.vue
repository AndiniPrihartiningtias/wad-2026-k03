<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getMe } from '../api.js'

import SessionList from '../components/SessionList.vue'
import SessionForm from '../components/SessionForm.vue'
import UserForm from '../components/UserForm.vue'
import UpdateForm from '../components/UpdateForm.vue'

const router = useRouter()
const listRef = ref(null)

const token = ref('')
const currentUsername = ref('')
const currentRole = ref('')
const isLoggedIn = ref(false)
const isAdmin = ref(false)
const profileLoading = ref(false)
const profileError = ref('')

onMounted(async () => {
  const savedToken = localStorage.getItem('access_token')

  if (!savedToken) return

  profileLoading.value = true

  try {
    const user = await getMe(savedToken)

    token.value = savedToken
    currentUsername.value = user.username
    currentRole.value = user.role
    isLoggedIn.value = true
    isAdmin.value = user.role === 'admin'

    localStorage.setItem('role', user.role)
  } catch {
    localStorage.removeItem('access_token')
    localStorage.removeItem('token')
    localStorage.removeItem('role')
  } finally {
    profileLoading.value = false
  }
})

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('token')
  localStorage.removeItem('role')

  token.value = ''
  currentUsername.value = ''
  currentRole.value = ''
  isLoggedIn.value = false
  isAdmin.value = false

  router.push('/login')
}

function onCreated() {
  listRef.value?.load()
}

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

      <button
        v-if="!isLoggedIn"
        type="button"
        @click="router.push('/login')"
      >
        Login
      </button>

      <button
        v-else
        type="button"
        @click="logout"
      >
        Logout
      </button>
    </header>

    <section v-if="profileLoading">
      <p>Memuat informasi akun...</p>
    </section>

    <section v-if="isLoggedIn" class="account-info">
      <h2>Akun Saya</h2>
      <p>Username: {{ currentUsername }}</p>
      <p>Role: {{ currentRole }}</p>
    </section>

    <UpdateForm
      v-if="isLoggedIn"
      :token="token"
      :current-username="currentUsername"
      @updated="onUserUpdated"
    />

        <section v-if="isLoggedIn">
      <SessionForm @created="onCreated" />
      <SessionList
        ref="listRef"
        :is-admin="isAdmin"
        :token="token"
      />
    </section>

    <section v-else>
      <h2>Silakan Login</h2>
      <p>Anda harus login untuk mengelola data peminjaman buku.</p>
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

header button {
  padding: 10px 16px;
  cursor: pointer;
}

.account-info {
  max-width: 420px;
  margin: 24px 0;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
}
</style>