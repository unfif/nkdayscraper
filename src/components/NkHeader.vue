<template>
  <header>
    <h2>{{ date }}</h2>
    <h2 v-for="place in places" :key="place">{{ place }}</h2>
  </header>
</template>

<script>
// import NkNav from './NkNav.vue'
export default {
  name: "NkHeader",
  // components: {
  //   NkNav,
  // },
  props: {
    date: {type: String},
    places: {type: Array}
  }
};
</script>

<style scoped>
html header {
  display: flex;
  margin: 0;
  padding: 8px 0 0;
  background: #343a40;
  color: #fff;
}
</style>