<template>
  <div class="state-message" aria-live="polite">
    <div v-if="status === 'loading'" class="state state--loading">
      <p>⏳ Memuat data…</p>
    </div>

    <div v-else-if="status === 'error'" class="state state--error">
      <p>❌ Gagal memuat data: {{ errorMsg }}</p>
      <button type="button" @click="$emit('retry')">Coba lagi</button>
    </div>

    <div v-else-if="status === 'empty'" class="state state--empty">
      <p>📭 Belum ada sesi peminjaman.</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "StateMessage",
  props: {
    status: { type: String, required: true },
    errorMsg: { type: String, default: "" },
  },
  emits: ["retry"],
};
</script>

<style scoped>
.state-message { margin: 1rem 0; }
.state { padding: 1.5rem; border-radius: 8px; text-align: center; }
.state--loading { background: #eef; color: #224; }
.state--error   { background: #fee; color: #a00; }
.state--empty   { background: #f5f5f5; color: #555; }
.state--error button { margin-top: .5rem; padding: .4rem .8rem; cursor: pointer; }
</style>