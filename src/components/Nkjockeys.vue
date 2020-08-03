<template>
  <div class="jockeysrank flex scrollable">
    <table
      v-for="place in places"
      class="racejockeys table table-sm table-striped table-hover"
      :key="place"
    >
      <thead class="table-dark">
        <tr>
          <th>場所</th>
          <th>騎手</th>
          <th
            v-for="field in jockeys.schema.fields"
            v-show="!(['place', 'jockey', 'dispmode'].includes(field.name)) && !field.name.endsWith('順')"
            :key="field"
          >
            {{ field.name }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="record in jockeys.data"
          v-show="record.place === place && (data.isAllDisp || (!(record['1着'] == 0 && record['2着'] == 0 && record['3着'] == 0)))"
          @click="ffDisp"
          :key="record.jockey"
        >
          <th :style="record.dispmode !== 'place1st' ? hiddentext : null">{{ record.place }}</th>
          <th>{{ record.jockey }}</th>
          <td
            v-for="(td, key) in record"
            :class="hasRank(key, record)"
            v-show="!(['place', 'jockey', 'dispmode'].includes(key)) && !key.endsWith('順')"
            :key="record.jockey + '_' + key"
          >
            {{ dispExists(td) }}
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { reactive } from 'vue'
export default {
  name: 'Nkjockeys',
  props: {
    jockeys: {
      type: Object,
    },
    places: {
      type: Array,
      'default': ()=>[]
    }
  },
  setup(){
    const data = reactive({
      isAllDisp: false
    })
    const dispExists = (val)=>{
      return val == 0 ? '...' : val;
    }
    const ffDisp = ()=>{
      data.isAllDisp = !data.isAllDisp;
    }
    const hasRank = (key, record)=>{
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
      'text-indent': '200%',
      'white-space': 'nowrap',
      'overflow': 'hidden'
    }
    return {
      data,
      dispExists,
      ffDisp,
      hasRank,
      hiddentext
    }
  }
}
</script>

<style scoped>
.table-sm th, .table-sm td{
  /* padding: 0.25em; */
  white-space: nowrap;
}
div.jockeysrank > table{
  margin: 4px 4px 24px;
}
</style>