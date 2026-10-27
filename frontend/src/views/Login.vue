<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const loading = ref(false);

// SEMENTARA: pura-pura jadi backend. Hapus kalau backend A1 sudah jadi.
async function loginMock(user, pass) {
  if (user === "admin" && pass === "admin123") {
    return { access_token: "token-palsu", role: "admin" };
  }
  throw new Error("Username atau password salah");
}

async function handleLogin() {
  errorMessage.value = "";
  loading.value = true;
  try {
    const data = await loginMock(username.value, password.value);
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.role);
    router.push("/");
  } catch (err) {
    errorMessage.value = err.message;
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <main>
    <header>
      <h1>Login</h1>
    </header>
    <section>
      <div class="card">
        <label>Username</label>
        <input v-model="username" type="text" placeholder="Username" />

        <label>Password</label>
        <input
          v-model="password"
          type="password"
          placeholder="Password"
          @keyup.enter="handleLogin"
        />

        <p v-if="errorMessage" style="color: red">{{ errorMessage }}</p>

        <button :disabled="loading" @click="handleLogin">
          {{ loading ? "Memproses..." : "Login" }}
        </button>
      </div>
    </section>
  </main>
</template>