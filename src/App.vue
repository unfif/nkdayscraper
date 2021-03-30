<template>
  <div id="app">
    <NkHeader :date="data.date" :places="data.places"/>
    <main>
      <NkRaces :places="data.places" :cols="data.cols" :records="data.records"/>
      <NkResults :results="data.results"/>
      <NkJockeys :jockeys="data.jockeys" :places="data.places"/>
    </main>
  </div>
</template>

<script>
import { reactive, onMounted } from 'vue'
import NkHeader from './components/NkHeader.vue'
import NkRaces from './components/NkRaces.vue'
import NkResults from './components/NkResults.vue'
import NkJockeys from './components/NkJockeys.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    NkHeader,
    NkRaces,
    NkResults,
    NkJockeys
  },
  setup(){
    const data = reactive({
      date: '',
      places: [],
      cols: ["場所", "R", "タイトル", "形式", "距離", "情報1", "情報2", "レコード", "天候", "状態", "時刻", "着順", "枠番", "馬番", "馬名", "性", "齢", "斤量", "騎手", "タイム", "着差", "人気", "オッズ", "上り", "通過", "所属", "調教師", "馬体重", "増減"],
      records: [],
      results: {
        schema: {fields: null},
        data: null
      },
      jockeys: {
        schema: {fields: null},
        data: null
      }
    })
    onMounted(()=>{
      axios.get("/api/racesinfo/")
      .then((response)=>{
        const racesinfo = response.data;
        data.date = racesinfo.data[0].date.split('T')[0];
        data.places = racesinfo.data[0].places;
      })
      .catch(err => console.log('err:', err))

      axios.get("/api/records/")
      .then((response)=>{
        data.records = response.data.data;
      })
      .catch(err => console.log('err:', err))

      axios.get("/api/racesgp2/")
      .then((response)=>{
        data.results = response.data;
      })
      .catch(err => console.log('err:', err))

      axios.get("/api/jockeys/")
      .then((response)=>{
        data.jockeys = response.data;
      })
      .catch(err => console.log('err:', err))
    })
    return {data}
  }
}
</script>

<style>
html body{
  padding: 0px;
  background: #666;
  font-size: 12px;
}
h1, h2, h3, h4, h5, h6{
  margin: 0;
  padding: 0;
}
h2, h3{
  margin: 0 8px;
}
main{
  margin: 0 auto;
  padding: 1rem;
  background: #EEE;
}
.flex{
  display: flex;
}
.scrollable{
  overflow: auto;
  white-space: nowrap;
}

.postnum_1{
  background: #ffffff !important;
  color: #000000 !important;
}
.postnum_2{
  background: #444444 !important;
  color: #ffffff !important;
}
.postnum_3{
  background: #e95556 !important;
  color: #ffffff !important;
}
.postnum_4{
  background: #416cba !important;
  color: #ffffff !important;
}
.postnum_5{
  background: #e7c52c !important;
  color: #ffffff !important;
}
.postnum_6{
  background: #45af4c !important;
  color: #ffffff !important;
}
.postnum_7{
  background: #ee9738 !important;
  color: #ffffff !important;
}
.postnum_8{
  background: #ef8fa0 !important;
  color: #ffffff !important;
}
.BgYellow,
.rank_1{
  background: #fff080 !important;
}
.BgBlue02,
.rank_2{
  background: #ccdfff !important;
}
.BgOrange,
.rank_3{
  background: #f0c8a0 !important;
}
</style>
