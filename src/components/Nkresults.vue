<template>
  <div class="placeinfo scrollable">
    <table class="placeinfo sticky table table-sm table-striped table-hover">
      <thead class="table-dark">
        <tr>
          <th
            v-for="column in results.schema.fields"
            v-show="column.name !== '形式'"
            :key="column.name"
          >{{ column.name }}</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="courcedetails in results.data"
          :key="courcedetails.場所 + courcedetails.形式"
        >
          <th class="table-secondary">
            {{ courcedetails.場所 + courcedetails.形式 }}
          </th>
          <td
            v-for="(courcedetail, key) in courcedetails"
            v-show="!(['場所', '形式'].includes(key))"
            :key="courcedetail"
          >{{ courcedetail }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { reactive } from 'vue'
export default {
  name: 'Nkresults',
  props: {
    results: {
      type: Object,
    }
  },
  setup(){
    const data = reactive({
      pass: null
    })
    return {data}
  }
}
</script>

<style scoped>
table.sticky thead th:nth-child(1),
table.sticky tbody th:nth-child(1){
  position: sticky;
  left: 0;
}
table.sticky thead th:nth-child(1){
  background-color: #454d55;
}
.table-sm th, .table-sm td{
  /* padding: 0.25em; */
  white-space: nowrap;
}
</style>