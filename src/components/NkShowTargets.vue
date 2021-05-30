<template>
  <div>
    <h5><span class="badge bg-secondary">{{ innerText }}</span></h5>
    <div class="btn-group">
      <button v-for="param in ['all'].concat(displayTargets)"
        class="btn btn-outline-secondary btn-sm"
        @click="showTargets($event, param, displayParams)"
        :key="param"
      >{{ param.toUpperCase() }}</button>
    </div>
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
      default: 'Title'
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
nav.navbar.dispplacerace{
  > div{
    display: flex;
    align-items: center;
    > h5{
      margin: 0 4px 0 0;
    }
  }
  h5 > span.bg-secondary{
    width: 5rem;
    line-height: unset;
  }
  button{
    width: 4.3em;
  }
}
</style>
