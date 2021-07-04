<template>
  <!-- <h5 v-if="innerText"><span class="badge bg-secondary">{{ innerText }}</span></h5> -->
  <div class="btn-group btn-group-sm">
    <button v-for="param in displayTargets" :key="param"
      class="btn btn-outline-secondary btn-sm"
      @click="showTargets(param, displayParams)"
    >{{ param.toUpperCase() }}</button>
  </div>
</template>

<script>
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
      default: ()=>({
        place: 'all',
        coursetype: 'all',
        racenum: 'all',
        is_show_all_ranks: false
      })
    }
  },
  setup(props, { emit } ){
    const showTargets = (param, displayParams)=>{
      const displayParams_copy = Object.assign({}, displayParams);
      for(let key in displayParams_copy){
        if(displayParams_copy[key] === 'param') displayParams_copy[key] = param;
      }
      const data = {};
      data.place = displayParams_copy.place;
      data.coursetype = displayParams_copy.coursetype;
      data.racenum = displayParams_copy.racenum;
      data.is_show_all_ranks = displayParams_copy.is_show_all_ranks;
      emit('click-nav-button', {data});
    }
    return {
      showTargets
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
