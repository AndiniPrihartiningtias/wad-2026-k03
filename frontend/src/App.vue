<script setup>
import SessionList from "./components/SessionList.vue";
import SessionForm from "./components/SessionForm.vue";
import { ref } from "vue";

const listRef = ref(null);

function onCreated() {
  listRef.value?.load();
}
</script>

<template>
  <main>
    <header>
      <h1>Pencatatan Peminjaman Buku</h1>
    </header>
    <section>
      <SessionForm @created="onCreated" />
      <SessionList ref="listRef" />
    </section>
  </main>
</template>