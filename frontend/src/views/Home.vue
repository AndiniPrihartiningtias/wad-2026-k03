<script setup>
import SessionList from "../components/SessionList.vue";
import SessionForm from "../components/SessionForm.vue";
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const listRef = ref(null);

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("role");
  router.push("/login");
}

function onCreated() {
  listRef.value?.load();
}
</script>

<template>
  <main>
    <header>
      <h1>Pencatatan Peminjaman Buku</h1>
      <button @click="logout">Logout</button>
    </header>
    <section>
      <SessionForm @created="onCreated" />
      <SessionList ref="listRef" />
    </section>
  </main>
</template>