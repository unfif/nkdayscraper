<template>
  <div class="placeinfo scrollable">
    <table class="placeinfo sticky table table-sm table-striped table-hover">
      <thead class="table-dark">
        <tr>
          <th v-for="column in results.schema.fields" :key="column.name"
            v-show="column.name !== '形式'"
          >
            {{ column.name }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="courcedetails in results.data" :key="courcedetails.場所 + courcedetails.形式">
          <th class="table-secondary">
            <ul>
              <li>{{ courcedetails.場所 }}</li>
              <li>{{ courcedetails.形式 }}</li>
            </ul>
          </th>
          <td v-for="(courcedetail, key) in courcedetails" :key="courcedetail"
            v-show="!(['場所', '形式'].includes(key))"
            v-html="displayResult(courcedetail, key)"
          >
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'NkResults',
  props: {
    results: {
      type: Object,
      default: ()=>{}
    }
  },
  setup(){
    let wakuLists = [];

    const displayResult = (results, key)=>{
      if(Array.isArray(results)){
        const li = document.createElement('li');
        const span = document.createElement('span');
        const liList = [];
        let spanList = [];
        if(key === '枠番') wakuLists = [];
        let wakuList = [];
        results.forEach((values, rowIndex)=>{
          const pad = {word: ' ', length: 2};
          if(key === '騎手'){pad.word = '　'; pad.length = 4;}
          if(['枠番', '馬番', '人気', '騎手'].includes(key)){
            spanList = [];
            wakuList = [];
            values.forEach((value, colIndex)=>{
              span.innerText = value;
              span.className = null;
              if(key === '枠番'){
                span.className = `postnum_${value}`;
                wakuList.push(value);
              }else if(key === '馬番'){
                span.className = `postnum_${wakuLists[rowIndex][colIndex]}`;
              }
              span.classList.add(key);
              if(key === '人気') span.classList.add(`rank_${value}`);
              spanList.push(span.outerHTML);
            })
            li.innerHTML = spanList.join('');
            if(key === '枠番') wakuLists.push(wakuList);
          }else if(key === '距離'){
            li.innerText = values;
            li.className = values[0] <= 1600 ? 'short-distance' : 'long-distance';
          }else{
            li.innerText = values;
          }
          liList.push(li.outerHTML);
        })
        return '<ul>' + liList.join('') + '</ul>';
      }
    }

    return {
      displayResult
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
table.placeinfo ul {
  list-style: none;
  margin-top: 0;
  margin-bottom: 0;
  padding-left: 0;
}
table.placeinfo td span {
  display: inline-block;
  width: 16px;
  text-align: center;
}
table.placeinfo td span.騎手 {
    width: 3rem;
}
</style>
