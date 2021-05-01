<template>
  <header>
    <h2>{{ dateFormated }}</h2>
    <h2 v-for="place in places" :key="place">{{ place }}</h2>
  </header>
</template>

<script>
import { computed } from 'vue'

export default {
  name: "NkHeader",
  props: {
    date: {type: Date},
    places: {type: Array}
  },
  setup(props){
    const dateFormated = computed(()=>{
      return props.date.toLocaleDateString();
    });

    return {
      dateFormated
    }
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