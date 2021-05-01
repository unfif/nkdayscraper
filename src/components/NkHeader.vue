<template>
  <header>
    <!-- <h2>{{ dateFormated }}</h2> -->
    <input type="date" id="start" name="trip-start" :value="dateFormated">
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
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        // weekday : 'short'
      };
      return props.date.toLocaleDateString('ja-JP', options).replace(/\//g, '-');
    });

    return {
      dateFormated
    }
  }
};
</script>

<style lang="scss" scoped>
html header {
  display: flex;
  margin: 0;
  background: #343a40;
  color: #fff;
  h6, .h6, h5, .h5, h4, .h4, h3, .h3, h2, .h2, h1, .h1{
    margin: 0.5rem;
  }
}
input[type="date"] {
  width: 12rem;
  font-size: 1.5rem;
  color: #fff;
  background: #343a40;
}
</style>