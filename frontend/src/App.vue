<template>
  <main>
    <header>
      <h1>Pencatatan Peminjaman Buku</h1>
    </header>
    <section>
      <SessionForm />
      <SessionItem />
      <StateMessage />
    </section>
  </main>
</template>

<script>
import SessionForm from './components/SessionForm.vue'
import SessionItem from './components/SessionItem.vue'
import StateMessage from './components/StateMessage.vue'

export default {
  name: 'App',
  components: {
    SessionForm,
    SessionItem,
    StateMessage
  }
}
</script>