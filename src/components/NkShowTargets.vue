<template>
  <div class="btn-group btn-group-sm">
    <button v-for="param in displayTargets" :key="param"
      class="btn btn-outline-primary btn-sm"
      @click="showTargets(param, displayParams)"
    >{{ param.toUpperCase() }}</button>
  </div>
</template>

<script setup>
import { useStore } from 'vuex'

const props = defineProps({
  innerText: {
    type: String,
    default: ''
  },
  displayTargets: {
    type: Array,
    default: ()=>[]
  },
  displayParams: {
    type: Object,
    default: () => ({
      place: 'all',
      coursetype: 'all',
      racenum: 'all',
      is_show_all_ranks: false
    })
  }
})

const store = useStore()

const showTargets = (param, displayParams) => {
  const displayParams_copy = Object.assign({}, displayParams);
  for(let key in displayParams_copy){
    if(displayParams_copy[key] === 'param') displayParams_copy[key] = param;
  }
  store.commit('updateDisplayParams', {
    place: displayParams_copy.place,
    coursetype: displayParams_copy.coursetype,
    racenum: displayParams_copy.racenum,
    is_show_all_ranks: false
  })
}
</script>

<style lang="scss" scoped>
nav.dispplacerace {
  button {
    width: 3.8rem;
    line-height: unset;
  }
}
</style>
