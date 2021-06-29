<template>
  <header>
    <input type="date" :value="dateFormated" @change="emitRaceDate($event)">
    <h4 v-for="place in places" :key="place">{{ place }}</h4>
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
  setup(props, { emit }){
    const dateFormated = computed(()=>{
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      };
      return props.date.toLocaleDateString('ja-JP', options).replace(/\//g, '-');
    });

    const emitRaceDate = (event)=>{
      const date = event.target.value;
      emit('change-race-date', {date});
    }

    return {
      dateFormated,
      emitRaceDate
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
  input[type="date"] {
    width: 12rem;
    font-size: 1.5rem;
    color: #fff;
    background: #343a40;
    border-width: 0;
    border-radius: 0;
  }
}
</style>
