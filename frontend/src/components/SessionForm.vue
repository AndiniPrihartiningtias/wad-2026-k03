<template>
  <form class="session-form" @submit.prevent="onSubmit" novalidate>
    <h2>Form Peminjaman</h2>

    <div class="field">
      <label for="peminjam">Nama Peminjam</label>
      <input id="peminjam" v-model="form.peminjam" type="text" />
      <small v-if="clientErrors.peminjam" class="error">{{ clientErrors.peminjam }}</small>
    </div>

    <div class="field">
      <label for="judul_buku">Judul Buku</label>
      <input id="judul_buku" v-model="form.judul_buku" type="text" />
      <small v-if="clientErrors.judul_buku" class="error">{{ clientErrors.judul_buku }}</small>
    </div>

    <div class="field">
      <label for="tanggal_pinjam">Tanggal Pinjam</label>
      <input id="tanggal_pinjam" v-model="form.tanggal_pinjam" type="date" />
      <small v-if="clientErrors.tanggal_pinjam" class="error">{{ clientErrors.tanggal_pinjam }}</small>
    </div>

    <div class="field">
      <label for="tanggal_kembali">Tanggal Kembali</label>
      <input id="tanggal_kembali" v-model="form.tanggal_kembali" type="date" />
      <small v-if="clientErrors.tanggal_kembali" class="error">{{ clientErrors.tanggal_kembali }}</small>
    </div>

    <p v-if="serverError" class="error server-error">Server: {{ serverError }}</p>

    <button type="submit" :disabled="submitting">
      {{ submitting ? "Menyimpan…" : "Simpan" }}
    </button>
  </form>
</template>

<script>
import { createSession } from "../api/session.js";

export default {
  name: "SessionForm",
  emits: ["created"],
  data() {
    return {
      form: { peminjam: "", judul_buku: "", tanggal_pinjam: "", tanggal_kembali: "" },
      clientErrors: {},
      serverError: "",
      submitting: false,
    };
  },
  methods: {
    validate() {
      const e = {};
      if (this.form.peminjam.trim().length < 2)
        e.peminjam = "Nama peminjam minimal 2 karakter.";
      if (this.form.judul_buku.trim().length < 2)
        e.judul_buku = "Judul buku minimal 2 karakter.";
      if (!this.form.tanggal_pinjam)
        e.tanggal_pinjam = "Tanggal pinjam wajib diisi.";
      if (!this.form.tanggal_kembali)
        e.tanggal_kembali = "Tanggal kembali wajib diisi.";
      if (
        this.form.tanggal_pinjam &&
        this.form.tanggal_kembali &&
        this.form.tanggal_kembali < this.form.tanggal_pinjam
      )
        e.tanggal_kembali = "Tanggal kembali tidak boleh sebelum tanggal pinjam.";
      this.clientErrors = e;
      return Object.keys(e).length === 0;
    },
    async onSubmit() {
      this.serverError = "";
      if (!this.validate()) return;
      this.submitting = true;
      try {
        await createSession({ ...this.form });
        this.form = { peminjam: "", judul_buku: "", tanggal_pinjam: "", tanggal_kembali: "" };
        this.clientErrors = {};
        this.$emit("created");
      } catch (err) {
        this.serverError = err.message || "Gagal menyimpan data.";
      } finally {
        this.submitting = false;
      }
    },
  },
};
</script>

<style scoped>
.session-form { max-width: 480px; display: grid; gap: .75rem; margin: 1rem 0; }
.field { display: grid; gap: .25rem; }
label { font-weight: 600; }
input { padding: .5rem; border: 1px solid #ccc; border-radius: 6px; }
.error { color: #c00; font-size: .85rem; }
.server-error { background: #fee; padding: .5rem; border-radius: 6px; }
button[type="submit"] { padding: .6rem 1rem; cursor: pointer; }
button:disabled { opacity: .6; cursor: not-allowed; }
</style>