<template>
  <header>
    <input type="date" :value="dateFormated" @change="emitRaceDate($event)">
    <NkNav :places="places"/>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import NkNav from './NkNav.vue'

const props = defineProps({
  date: {type: Date},
  places: {type: Array}
})

const emit = defineEmits(['change-race-date'])

const dateFormated = computed(() => {
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  };
  return props.date.toLocaleDateString('ja-JP', options).replace(/\//g, '-');
})

const emitRaceDate = (event) => {
  const date = event.target.value;
  emit('change-race-date', {date});
}
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
    width: 9rem;
    font-size: 1.1rem;
    color: #fff;
    background: #343a40;
    border-width: 0;
    border-radius: 0;
  }
}
</style>
