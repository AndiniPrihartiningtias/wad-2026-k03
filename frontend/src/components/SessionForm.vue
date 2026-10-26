<template>
  <form class="session-form" @submit.prevent="onSubmit" novalidate>
    <h2>Form Peminjaman</h2>

    <div class="field">
      <label for="book_title">Judul Buku</label>
      <input id="book_title" v-model="form.book_title" type="text" />
      <small v-if="clientErrors.book_title" class="error">
        {{ clientErrors.book_title }}
      </small>
    </div>

    <div class="field">
      <label for="borrower_name">Nama Peminjam</label>
      <input id="borrower_name" v-model="form.borrower_name" type="text" />
      <small v-if="clientErrors.borrower_name" class="error">
        {{ clientErrors.borrower_name }}
      </small>
    </div>

    <div class="field">
      <label for="status">Status</label>
      <select id="status" v-model="form.status">
        <option value="">— Pilih status —</option>
        <option value="dipinjam">Dipinjam</option>
        <option value="dikembalikan">Dikembalikan</option>
      </select>
      <small v-if="clientErrors.status" class="error">
        {{ clientErrors.status }}
      </small>
    </div>

    <p v-if="serverError" class="error server-error">
      Server: {{ serverError }}
    </p>

    <button type="submit" :disabled="submitting">
      {{ submitting ? "Menyimpan…" : "Simpan" }}
    </button>
  </form>
</template>

<script setup>
import { reactive, ref } from "vue";
import { createSession } from "../api/session.js";

const emit = defineEmits(["created"]);

const form = reactive({
  book_title: "",
  borrower_name: "",
  status: "",
});

const clientErrors = ref({});
const serverError = ref("");
const submitting = ref(false);

function validate() {
  const e = {};
  if (form.book_title.trim().length < 1)
    e.book_title = "Judul buku wajib diisi.";
  if (form.borrower_name.trim().length < 1)
    e.borrower_name = "Nama peminjam wajib diisi.";
  if (!form.status) e.status = "Status wajib dipilih.";
  clientErrors.value = e;
  return Object.keys(e).length === 0;
}

async function onSubmit() {
  serverError.value = "";
  if (!validate()) return;
  submitting.value = true;
  try {
    await createSession({ ...form });
    form.book_title = "";
    form.borrower_name = "";
    form.status = "";
    clientErrors.value = {};
    emit("created");
  } catch (err) {
    serverError.value = err.message || "Gagal menyimpan data.";
  } finally {
    submitting.value = false;
  }
}
</script>

<style scoped>
.session-form { max-width: 480px; display: grid; gap: .75rem; margin: 1rem 0; }
.field { display: grid; gap: .25rem; }
label { font-weight: 600; }
input, select { padding: .5rem; border: 1px solid #ccc; border-radius: 6px; }
.error { color: #c00; font-size: .85rem; }
.server-error { background: #fee; padding: .5rem; border-radius: 6px; }
button[type="submit"] { padding: .6rem 1rem; cursor: pointer; }
button:disabled { opacity: .6; cursor: not-allowed; }
</style>