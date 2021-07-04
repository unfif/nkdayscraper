<template>
  <nav v-bind="$attrs" class="dispplacerace btn-toolbar">
    <NkShowTargets :inner-text="''"
      :display-targets="['all']"
      :display-params="{place: 'all', coursetype: 'all', racenum: 'all'}"
      @click-nav-button="throughEvent($event)"
    />
    <NkShowTargets :inner-text="'場所'"
      :display-targets="places"
      :display-params="{place: 'param', coursetype: 'all', racenum: 'all'}"
      @click-nav-button="throughEvent($event)"
    />
    <NkShowTargets :inner-text="'コース'"
      :display-targets="['芝', 'ダート']"
      :display-params="{place: 'all', coursetype: 'param', racenum: 'all'}"
      @click-nav-button="throughEvent($event)"
    />
    <NkShowTargets :inner-text="'レース'"
      :display-targets="['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']"
      :display-params="{place: 'all', coursetype: 'all', racenum: 'param'}"
      @click-nav-button="throughEvent($event)"
    />
  </nav>
</template>

<script>
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
    const throughEvent = (event)=>{
      const data = event.data;
      emit('click-nav-button', {data});
    }

    return {
      throughEvent
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
