<template>
  <div class="placeinfo scrollable">
    <table class="placeinfo sticky table table-sm table-hover">
      <thead class="table-dark">
        <tr>
          <th v-for="column in results.schema.fields" :key="column.name"
            v-show="!(['形式', 'index', 'size', 'display_top', 'display_bottom'].includes(column.name))"
          >
            {{ column.name }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="raceResult in results.data" :key="raceResult.index" :class="{bottom: raceResult.display_bottom}">
          <th class="table-secondary" :rowspan="makeRowspan(raceResult)">
            {{ raceResult.場所 + raceResult.形式 }}
          </th>
          <td v-for="(raceDetail, key) in raceResult" :key="`${key}-${raceDetail}`"
            v-show="!(['場所', '形式', 'index', 'size', 'display_top', 'display_bottom'].includes(key))"
            v-html="displayRaceDetail(raceDetail, key)"
          >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { onBeforeUpdate } from 'vue'
export default {
  name: 'NkResults',
  props: {
    results: {
      type: Object,
      default: ()=>{}
    }
  },
  setup(){
    const data = {
      is_setRows: {}
    }

    onBeforeUpdate(()=>{
      data.is_setRows = {};
    })

    let wakuLists = [];

    const displayRaceDetail = (raceDetail, key)=>{
      const span = document.createElement('span');
      if(Array.isArray(raceDetail)){
        const values = []
        if(key === '枠番') wakuLists = [];
        raceDetail.forEach((value, index)=>{
          if(value != 99){
            span.innerText = value;
            if(key === '枠番'){
              wakuLists.push(value);
              span.className = `postnum_${value}`
            }else if(key === '馬番'){
              span.className = `postnum_${wakuLists[index]}`;
            }else if(key === '人気'){
              span.className = `rank_${value}`;
            }
            span.classList.add(key);
            values.push(span.outerHTML);
          }
        })
        return values.join('');
      }
      if(key === '距離') span.className = raceDetail <= 1600 ? 'short-distance' : 'long-distance';
      span.innerText = raceDetail;
      return span.outerHTML;
    }

    const makeRowspan = (raceResult)=>{
      let rowspan = 0;
      if(raceResult.display_top) rowspan = raceResult.size
      return rowspan;
    }

    return {
      data,
      displayRaceDetail,
      makeRowspan
    }
  }
}
</script>

<style lang="scss" scoped>
table.sticky {
  thead th:nth-child(1) {
    background-color: #454d55;
  }
  thead th:nth-child(1),
  tbody th:nth-child(1) {
    position: sticky;
    left: 0;
  }
}
.table-sm {
  th,
  td {
    white-space: nowrap;
    font-family: Osaka-mono, "Osaka-等幅", "ＭＳ ゴシック", monospace;
  }
}
</style>
<style>
table.placeinfo th[rowspan="0"] {
  display: none;
}
table.placeinfo tr.bottom {
  height: 2.5em;
}
table.placeinfo th,
table.placeinfo td {
  padding-top: 0;
  padding-bottom: 0;
}
table.placeinfo td span.枠番,
table.placeinfo td span.馬番,
table.placeinfo td span.人気 {
  display: inline-block;
  width: 16px;
  text-align: center;
}
table.placeinfo td span.騎手 {
  display: inline-block;
  width: 3rem;
  text-align: left;
}
</style>
