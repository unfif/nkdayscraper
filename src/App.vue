<template>
  <div id="app">
    <Header :date="data.date" :places="data.places"/>
    <div class="contents">
      <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
      <Nkraces :places="data.places" :cols="data.cols" :records="data.records"/>
      <Nkresults :results="data.results"/>
    </div>
  </div>
</template>

<script>
import {reactive, onMounted} from '@vue/composition-api'
import Header from './components/Header.vue'
import Nkraces from './components/Nkraces.vue'
import Nkresults from './components/Nkresults.vue'
import axios from 'axios'

export default {
  name: 'App',
  components: {
    Header,
    Nkraces,
    Nkresults
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
      }
    })
    onMounted(function(){
      axios.get("http://localhost:5000/api/")
      .then(response => {
        data.records = JSON.parse(response.data.racesdf).data;
        let racesinfo = JSON.parse(response.data.racesinfo);
        data.date = racesinfo.data[0].date.split('T')[0];
        data.places = racesinfo.data[0].places;
        data.results = JSON.parse(response.data.racesgp2);
        console.log(data.results.data);
      })
      .catch(err => console.log('err:', err))
    })
    return {data}
  }
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
  /* body {
    font-family: Helvetica Neue, Arial, sans-serif;
    font-size: 14px;
    color: #444;
  }

  table {
    border: 2px solid #42b983;
    border-radius: 3px;
    background-color: #fff;
  }

  th {
    background-color: #42b983;
    color: rgba(255, 255, 255, 0.66);
    cursor: pointer;
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
  }

  td {
    background-color: #f9f9f9;
  }

  th,
  td {
    min-width: 120px;
    padding: 10px 20px;
  } */
  h1, h2, h3, h4, h5, h6{
    margin: 0;
    padding: 0;
  }
  html body{
    padding: 0px;
    background: #666;
    font-size: 12px;
  }
  h2, h3{
    margin: 0 8px;
  }
  .contents{
    /* display: flex;
    flex-direction: column;
    align-items: center; */
    width: 95%;
    margin: 0 auto;
    padding: 4px 10px;
    background: #EEE;
  }
  .flex{
    display: flex;
  }
  .scrollable{
    overflow: auto;
    /* overflow-x: scroll; */
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
