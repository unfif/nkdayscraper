<template>
  <nav v-bind="$attrs" class="dispplacerace navbar">
    <!-- <div class="dispplace">
      <h5><span class="badge bg-secondary">場所</span></h5>
      <div class="btn-group">
        <button v-for="place in ['all'].concat(places)"
          class="btn btn-outline-primary btn-sm"
          @click="showTargets($event, place, 'all', 'all')"
          :key="place"
        >{{ place.toUpperCase() }}</button>
      </div>
    </div>
    <div class="dispcoursetype">
      <h5><span class="badge bg-secondary">コース</span></h5>
      <div class="btn-group">
        <button v-for="coursetype in ['all'].concat(['芝', 'ダート'])"
          class="btn btn-outline-secondary btn-sm"
          @click="showTargets($event, 'all', coursetype, 'all')"
          :key="coursetype"
        >{{ coursetype.toUpperCase() }}</button>
      </div>
    </div>
    <div class="dispracenum">
      <h5><span class="badge bg-secondary">レース</span></h5>
      <div class="btn-group">
        <button v-for="racenum in ['all'].concat(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'])"
          class="btn btn-outline-secondary btn-sm"
          @click="showTargets($event, 'all', 'all', racenum)"
          :key="racenum"
        >{{ racenum.toUpperCase() }}</button>
      </div>
    </div> -->
    <NkShowTargets class="dispplace" :inner-text="'場所'"
      :display-targets="places"
      :display-params="{place: 'param', coursetype: 'all', racenum: 'all'}"
      @click-nav-button="handleNavEvent($event)"
    />
    <NkShowTargets class="dispcoursetype" :inner-text="'コース'"
      :display-targets="['芝', 'ダート']"
      :display-params="{place: 'all', coursetype: 'param', racenum: 'all'}"
      @click-nav-button="handleNavEvent($event)"
    />
    <NkShowTargets class="dispracenum" :inner-text="'レース'"
      :display-targets="['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']"
      :display-params="{place: 'all', coursetype: 'all', racenum: 'param'}"
      @click-nav-button="handleNavEvent($event)"
    />
  </nav>
</template>

<script>
import { reactive } from 'vue'
import NkShowTargets from './NkShowTargets.vue'

export default {
  name: 'NkNav',
  components: {
    NkShowTargets
  },
  emits: ['click-nav-button'],
  props: {
    places: {
      type: Array,
      'default': ()=>[]
    },
    // cols: {
    //   type: Array,
    //   'default': ()=>[]
    // },
    // records: {
    //   type: Array,
    //   'default': ()=>[]
    // }
  },
  setup(props, { emit }){
    const data = reactive({
      place: 'all',
      coursetype: 'all',
      racenum: 11,
      is_show_all_ranks: false,
    })
    const showTargets = (event, place, coursetype, racenum)=>{
      data.place = place;
      data.coursetype = coursetype;
      data.racenum = racenum;
      data.is_show_all_ranks = false;
      flipBorderForRace(event);
      emit('click-nav-button', {event, data});
    }
    const flipBorderForRace = (event)=>{
      const elements = document.querySelectorAll('.rankinfo_initdisp_end, .rankinfo_initdisp_topend');
      if(!data.is_show_all_ranks){
        if(event.target.tagName === 'TD') data.place = 'all';
        elements.forEach((element)=>{
          element.style.borderBottom = '3px double #999';
        });
        // $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css({'border-bottom': '3px double #999'});
      }else{
        elements.forEach((element)=>{
          element.style.borderColor = 'inherit';
          element.style.borderWidth = 0;
        });
        // $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css({'border-color': 'inherit', 'border-width': 0});
      }
    }
    const handleNavEvent = (event)=>{
      showTargets(event.event, event.data.place, event.data.coursetype, event.data.racenum);
    }
    return {
      data,
      showTargets,
      flipBorderForRace,
      handleNavEvent
    }
  }
}
</script>

<style lang="scss" scoped>
nav.navbar.dispplacerace{
  // display: flex;
  // flex-wrap: wrap;
  // margin-bottom: 4px;
  padding: 0;
  margin-bottom: 1rem;
  // > div{
  //   display: flex;
  //   align-items: center;
  //   > h5{
  //     margin: 0 4px;
  //   }
  // }
  // h5 > span.bg-secondary{
  //   width: 80px;
  //   line-height: unset;
  // }
  // button{
  //   width: 4.3em;
  //   margin-left: 1px;
  // }
}
</style>