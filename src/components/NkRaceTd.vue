<template>
  <span>
    <button v-if="displaymode.hasBtn"
      type="button" class="btn btn-sm btn-outline-info"
      @click="displaymode.callback(record[displaymode.urlinfo], displaymode.params)"
    >
    </button>
    <span v-if="!displaymode.hasLink">
      {{ text }}
    </span>
    <span v-else>
      <a
        :href="record[displaymode.urlinfo]"
        target="_blank"
        rel="noopener noreferrer"
        aria-describedby="tooltip"
        ref="ref_target"
      >
        {{ text }}
      </a>
      <NkTooltip :target="ref_target" :displaymode="displaymode"/>
    </span>
  </span>
</template>

<script>
import { ref } from 'vue'
import NkTooltip from './NkTooltip.vue'

export default {
  name: 'NkRaceTd',
  components: {
    NkTooltip
  },
  props: {
    text: {
      String,
      default: ''
    },
    displaymode: {
      Object,
      default: {
        hasBtn: false,
        hasLink: false,
        urlinfo: null,
        callback: ()=>{}
      }
    },
    record: {
      Object,
      default: {}
    }
  },
  setup(){
    const ref_target = ref(null);

    return {
      ref_target
    }
  }
}
</script>

<style scoped>
</style>
