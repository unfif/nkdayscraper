<template>
  <nav v-bind="$attrs" class="dispplacerace btn-toolbar">
    <NkShowTargets :inner-text="''"
      :display-targets="['all']"
      :display-params="{place: 'all', coursetype: 'all', racenum: 'all'}"
      @click-nav-button="handleNavEvent($event)"
    />
    <NkShowTargets :inner-text="'場所'"
      :display-targets="places"
      :display-params="{place: 'param', coursetype: 'all', racenum: 'all'}"
      @click-nav-button="handleNavEvent($event)"
    />
    <NkShowTargets :inner-text="'コース'"
      :display-targets="['芝', 'ダート']"
      :display-params="{place: 'all', coursetype: 'param', racenum: 'all'}"
      @click-nav-button="handleNavEvent($event)"
    />
    <NkShowTargets :inner-text="'レース'"
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
      default: ()=>[]
    }
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
      flipDisplayForSameRoundRaces(event);
      emit('click-nav-button', {event, data});
    }

    const flipDisplayForSameRoundRaces = (event)=>{
      if(!data.is_show_all_ranks && event.target.tagName === 'TD') data.place = 'all';
    }

    const handleNavEvent = (event)=>{
      showTargets(event.event, event.data.place, event.data.coursetype, event.data.racenum);
    }

    return {
      data,
      showTargets,
      flipDisplayForSameRoundRaces,
      handleNavEvent
    }
  }
}
</script>

<style lang="scss" scoped>
nav.dispplacerace {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 2px 4px;
  // margin-bottom: 2px;
}
</style>
