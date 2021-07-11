<template>
  <NkHeader
    :date="data.date" :places="data.places"
    @change-race-date="changeRaceDate($event)"
    @click-nav-button="showTargets($event)"
  />
  <main>
    <NkRaces
      :cols="data.cols" :records="data.records" :is_raceLoading="data.is_raceLoading"
      :place="data.place" :coursetype="data.coursetype" :racenum="data.racenum" :is_show_all_ranks="data.is_show_all_ranks"
    />
    <NkResults :results="data.results"/>
    <NkJockeys :jockeys="data.jockeys" :places="data.places"/>
  </main>
</template>

<script>
import { reactive } from 'vue'
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
      date: new Date(),
      places: [],
      cols: ["場所", "R", "タイトル", "形式", "距離", "情報1", "情報2", "レコード", "天候", "状態", "時刻", "着順", "枠番", "馬番", "馬名", "性", "齢", "斤量", "騎手", "タイム", "着差", "人気", "オッズ", "上り", "通過", "所属", "調教師", "馬体重", "増減"],
      records: {schema: {fields: null}, data: []},
      results: {schema: {fields: null}, data: []},
      jockeys: {schema: {fields: null}, data: []},
      is_raceLoading: true,

      place: 'all',
      coursetype: 'all',
      racenum: '11',
      is_show_all_ranks: false
    })

    const getData = (date = null)=>{
      data.is_raceLoading = true;
      let url = '/api/';
      if(date) url += `${date}/`;
      axios.get(url)
      .then((response)=>{
        if(response.data){
          const racesinfo = JSON.parse(response.data.racesinfo);
          data.date = new Date(racesinfo.data[0].date);
          data.places = racesinfo.data[0].places;
          data.records = JSON.parse(response.data.records);
          data.results = JSON.parse(response.data.results);
          data.jockeys = JSON.parse(response.data.jockeys);
        }
      })
      .catch((err)=>{console.log('err:', err)})
      .finally(()=>{data.is_raceLoading = false})
    }

    const changeRaceDate = (event)=>{
      data.date = new Date(event.date);
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      };
      getData(data.date.toLocaleDateString('ja-JP', options).replace(/\//g, '-'));
    }

    const showTargets = (event)=>{
      data.place = event.data.place;
      data.coursetype = event.data.coursetype;
      data.racenum = event.data.racenum;
      data.is_show_all_ranks = false;
    }

    getData();

    return {
      data,
      getData,
      changeRaceDate,
      showTargets
    }
  }
}
</script>

<style>
html body {
  padding: 0px;
  background: #666;
  font-size: 12px;
}
h1, h2, h3, h4, h5, h6 {
  margin: 0;
  padding: 0;
}
h2, h3 {
  margin: 0 8px;
}
main {
  /* padding: 1rem; */
  background: #EEE;
}
.scrollable {
  overflow: auto;
  white-space: nowrap;
}

.postnum_1 {
  background: #ffffff !important;
  color: #000000 !important;
}
.postnum_2 {
  background: #444444 !important;
  color: #ffffff !important;
}
.postnum_3 {
  background: #e95556 !important;
  color: #ffffff !important;
}
.postnum_4 {
  background: #416cba !important;
  color: #ffffff !important;
}
.postnum_5 {
  background: #e7c52c !important;
  color: #ffffff !important;
}
.postnum_6 {
  background: #45af4c !important;
  color: #ffffff !important;
}
.postnum_7 {
  background: #ee9738 !important;
  color: #ffffff !important;
}
.postnum_8 {
  background: #ef8fa0 !important;
  color: #ffffff !important;
}

.BgYellow,
.rank_1 {
  background: #fff080 !important;
}
.BgBlue02,
.rank_2 {
  background: #ccdfff !important;
}
.BgOrange,
.rank_3 {
  background: #f0c8a0 !important;
}
</style>
