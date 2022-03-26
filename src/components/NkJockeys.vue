<template>
  <div class="jockeysrank scrollable">
    <table class="racejockeys table table-sm table-hover"
      v-for="place in places" :key="place"
    >
      <thead class="table-dark">
        <tr>
          <th>場所</th>
          <th>騎手</th>
          <th
            v-for="field in jockeys.schema.fields" :key="field"
            v-show="!(['place', 'jockey', 'dispmode'].includes(field.name)) && !field.name.endsWith('順')"
          >{{ field.name }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="record in jockeys.data" :key="record.jockey"
          v-show="record.place === place && (data.isAllDisp || (!(record['1着'] == 0 && record['2着'] == 0 && record['3着'] == 0)))"
          @click="ffDisp"
        >
          <th :style="record.dispmode !== 'place1st' ? hiddentext : null">{{ record.place }}</th>
          <th>{{ record.jockey }}</th>
          <td
            v-for="(td, key) in record" :key="`${record.jockey}_${key}`"
            :class="hasRank(key, record)"
            v-show="!(['place', 'jockey', 'dispmode'].includes(key)) && !key.endsWith('順')"
          >{{ dispExists(td) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

const props = defineProps({
  jockeys: {
    type: Object
  },
  places: {
    type: Array,
    default: ()=>[]
  }
})

const data = reactive({
  isAllDisp: false
})

const dispExists = (val) => {
  return val == 0 ? '...' : val;
}

const ffDisp = () => {
  data.isAllDisp = !data.isAllDisp;
}

const hasRank = (key, record) => {
  let response = {};
  const lastword = key.slice(-1);
  if(lastword === '着' || lastword === '率'){
    let rank = record[key + '順'];
    if(rank <= 3 && record[key] !== 0){
      response = {['rank_' + rank]: true};
    }
  }
  return response;
}

const hiddentext = {
  'text-indent': '500%',
  'white-space': 'nowrap',
  'overflow': 'hidden'
}
</script>

<style lang="scss" scoped>
.table-sm th,
.table-sm td {
  white-space: nowrap;
}
div.jockeysrank {
  display: flex;
  gap: 0 0.5rem;
  align-items: flex-start;
}
</style>
