<template>
  <div class="placeinfo scrollable">
    <table class="placeinfo sticky table table-sm table-striped table-hover">
      <thead class="table-dark">
        <tr>
          <th
            v-for="column in results.schema.fields" :key="column.name"
            v-show="column.name !== '形式'"
          >{{ column.name }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="courcedetails in results.data" :key="courcedetails.場所 + courcedetails.形式">
          <th class="table-secondary">
            {{ courcedetails.場所 + courcedetails.形式 }}
          </th>
          <td
            v-for="(courcedetail, key) in courcedetails" :key="courcedetail"
            v-show="!(['場所', '形式'].includes(key))"
          >{{ courcedetail }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { reactive } from 'vue'
export default {
  name: 'NkResults',
  props: {
    results: {
      type: Object
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
  }
}
</style>
