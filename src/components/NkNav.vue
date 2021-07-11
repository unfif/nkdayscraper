<template>
  <nav v-bind="$attrs" class="dispplacerace btn-toolbar">
    <NkShowTargets :display-targets="['all']"
      :display-params="{place: 'all', coursetype: 'all', racenum: 'all'}"
    />
    <NkShowTargets :display-targets="places"
      :display-params="{place: 'param', coursetype: 'all', racenum: 'all'}"
    />
    <NkShowTargets :display-targets="['芝', 'ダート']"
      :display-params="{place: 'all', coursetype: 'param', racenum: 'all'}"
    />
    <NkShowTargets :display-targets="['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12']"
      :display-params="{place: 'all', coursetype: 'all', racenum: 'param'}"
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
  props: {
    places: {
      type: Array,
      default: ()=>[]
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
}
</style>
