<template>
  <!-- <h5 v-if="innerText"><span class="badge bg-secondary">{{ innerText }}</span></h5> -->
  <div class="btn-group btn-group-sm">
    <button v-for="param in displayTargets" :key="param"
      class="btn btn-outline-secondary btn-sm"
      @click="showTargets($event, param, displayParams)"
    >{{ param.toUpperCase() }}</button>
  </div>
</template>

<script>
import { reactive } from 'vue'

export default {
  name: 'NkShowTargets',
  emits: ['click-nav-button'],
  props: {
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
      default: ()=>({place: 'all', coursetype: 'all', racenum: 'all'})
    }
  },
  setup(props, { emit } ){
    const data = reactive({
      place: 'all',
      coursetype: 'all',
      racenum: 11,
      is_show_all_ranks: false
    })
    const showTargets = (event, param, displayParams)=>{
      const displayParams_copy = Object.assign({}, displayParams);
      for(let key in displayParams_copy){
        if(displayParams_copy[key] === 'param') displayParams_copy[key] = param;
      }
      data.place = displayParams_copy.place;
      data.coursetype = displayParams_copy.coursetype;
      data.racenum = displayParams_copy.racenum;
      data.is_show_all_ranks = false;
      flipDisplayForSameRoundRaces(event);
      emit('click-nav-button', {event, data});
    }
    const flipDisplayForSameRoundRaces = (event)=>{
      if(!data.is_show_all_ranks && event.target.tagName === 'TD') data.place = 'all';
    }
    return {
      data,
      showTargets,
      flipDisplayForSameRoundRaces
    }
  }
}
</script>

<style lang="scss" scoped>
nav.dispplacerace {
  h5 {
    margin: 0;
    line-height: unset;
  }
  h5 > span.bg-secondary,
  button {
    width: 3.7rem;
    // padding: 4px 8px;
    line-height: unset;
    // border: 1.111px solid;
  }
}
// .btn-group > .btn:not(.dropdown-toggle),
// .btn-group > .btn-group > .btn {
//   border-radius: 0;
// }
</style>
