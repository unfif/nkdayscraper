<template>
  <div class="tmpelm">
    <div class="dispplacerace">
      <div class="dispplace">
        <h5><span class="badge bg-secondary">場所</span></h5>
        <button class="dispallplace btn btn-outline-primary btn-sm"
          @click="dispCategory($event, 'all', 'all', 'all')"
        >ALL</button>
        <button class="dispplace btn btn-outline-primary btn-sm"
          v-for="place in places"
          @click="dispCategory($event, place, 'all', 'all')"
          :key="place"
        >{{ place }}</button>
      </div>
      <div class="dispcoursetype">
        <h5><span class="badge bg-secondary">コース</span></h5>
        <button class="dispallcoursetypes btn btn-outline-secondary btn-sm"
          @click="dispCategory($event, 'all', 'all', 'all')"
        >ALL</button>
        <button class="dispcoursetype btn btn-outline-secondary btn-sm"
          @click="dispCategory($event, 'all', '芝', 'all')"
        >芝</button>
        <button class="dispcoursetype btn btn-outline-secondary btn-sm"
          @click="dispCategory($event, 'all', 'ダート', 'all')"
        >ダート</button>
      </div>
      <div class="disprace btn-group-dummy">
        <h5><span class="badge bg-secondary">レース</span></h5>
        <button class="dispallraces btn btn-outline-secondary btn-sm"
          @click="dispCategory($event, 'all', 'all', 'all')"
        >ALL</button>
      <!-- <div class="btn-group" role="group" aria-label="Basic example"> -->
        <button class="dispracenum btn btn-outline-secondary btn-sm"
          v-for="idx in 12"
          @click="dispCategory($event, 'all', 'all', idx)"
          :key="idx"
        >{{ idx }}</button>
      </div>
      <!-- <div>
        <button class="crawl btn btn-outline-primary btn-sm" style="display: auto; width: auto;">api</button>
      </div> -->
    </div>
    <div class="dispraceresults scrollable">
      <table class="raceresults table table-sm table-hover table-striped-inactive">
        <thead class="table-dark">
          <tr>
            <th
              v-for="col in cols"
              :class="['col_' + col]"
              :key="col"
            >{{ col }}</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="record in records"
            :class="[
              '場所_'+record.場所,
              '形式_'+record.形式,
              'R_'+record.R,
              '着順_'+record.着順,
              'idx_'+record.index,
              'rankinfo_'+record.rankinfo
            ]"
            v-show="dispPlace(record.場所) && dispRacenum(record.R) && dispRankinfo(record.rankinfo) && dispCoursetype(record.形式)"
            @click="if($event.target.tagName !== 'A'){
              data.dispallsameraces = !data.dispallsameraces
              data.place = record.場所;
              data.racenum = record.R;
              flipDispPlace($event);
            }"
            :key="record.index"
          >
            <td
              v-for="(col, index) in cols"
              :class="[
                'col_'+col,
                makeClass(col === '形式', 'coursetype_' + record[col]),
                makeClass(col === '枠番', 'postnum_' + record[col]),
                makeClass(col === '人気', 'rank_' + record[col]),
                makeClass(col === '上り', 'rank_' + record['last3frank']),
                makeClass(col === '所属' && record[col] === '栗東', 'text-success'),
                !Boolean(index % 2) ? 'x-odd' : 'x-even'
              ]"
              :style="[
                col === '距離' && record['rankinfo'] === 'initdisp_top' ? {background: 'linear-gradient(transparent 80%, ' + (record[col] <= 1600 ? '#ee9738' : '#45af4c') + ' 20%'} : ''
              ]"
              :key="record.index + '_' + col"
              v-html="dispColStr(record, col)"
            ></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { reactive } from 'vue'
import $ from 'jquery'
export default  {
  name: 'Nkraces',
  props: {
    places: {
      type: Array,
      'default': ()=>[]
    },
    cols: {
      type: Array,
      'default': ()=>[]
    },
    records: {
      type: Array,
      'default': ()=>[]
    }
  },
  setup(){
    const data = reactive({
      place: 'all',
      coursetype: 'all',
      racenum: 11,
      dispallsameraces: false
    })
    const dispColStr = (record, col)=>{
      let colstr = String(record[col]);
      if(col === 'タイトル') colstr = '<a href="' + record.結果URL + '" target="_blank" rel="noopener noreferrer">' + colstr + '</a>';
      else if(col === '馬名') colstr = '<a href="' + record.馬URL + '" target="_blank" rel="noopener noreferrer">' + colstr + '</a>';
      return colstr;
    }
    const dispCategory = (event, place, coursetype, racenum)=>{
      data.place = place;
      data.coursetype = coursetype;
      data.racenum = racenum;
      data.dispallsameraces = false;
      flipDispPlace(event);
    }
    const dispCoursetype = (coursetype)=>{
      if(data.coursetype === 'all'){
        return true;
      }else{
        return coursetype == data.coursetype;
      }
    }
    const dispPlace = (place)=>{
      if(data.place === 'all'){
        return true;
      }else{
        return place == data.place;
      }
    }
    const dispRacenum = (racenum)=>{
      if(data.racenum === 'all'){
        return true;
      }else{
        return racenum == data.racenum;
      }
    }
    const dispRankinfo = (rankinfo)=>{
      if(data.dispallsameraces){
        return true;
      }else{
        return rankinfo.startsWith('initdisp_');
      }
    }
    const flipDispPlace = (event)=>{
      if(!data.dispallsameraces){
        if(event.target.tagName === 'TD') data.place = 'all';
        $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css('border-bottom', '3px double #999');
      }else{
        $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css({'border-color': 'inherit', 'border-width': 0});
      }
    }
    const makeClass = (condition, cls)=>{
      return condition ? cls : ''
    }
    const wlog = (target)=>{
      console.log(target);
    }

    return {
      data,
      dispColStr,
      dispCategory,
      dispCoursetype,
      dispPlace,
      dispRacenum,
      dispRankinfo,
      flipDispPlace,
      makeClass,
      wlog
    }
  }
};
</script>

<style scoped>
div.dispplacerace{
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 4px;
}
div.dispplacerace > div{
  display: flex;
  align-items: center;
  padding: 4px;
}
div.dispplacerace > div > h5{
  /* width: 60px; */
  margin: 0 8px;
  /* text-align: end; */
}
div.dispplacerace > div > h5 > span.badge{
  width: 60px;
  /* margin: 0 8px; */
  /* text-align: end; */
}
div.dispplacerace button{
  width: 4.3em;
  margin-left: 1px;
}
/* th.active {
  color: #fff;
} */
/* .rankinfo_initnone_mid,
.rankinfo_initnone_end{
  display: none;
}
.rankinfo_initdisp_end{
  border-bottom: 3px double #999;
}
.rankinfo_initnone_end{
  border-bottom: 3px solid #999;
} */
table.raceresults{
  width: 100%;
  margin: 0 auto 10px;
}
.table-sm th, .table-sm td{
  /* padding: 0.25em; */
  white-space: nowrap;
}
th.col_R{
  width: 2.25em;
}
th.col_場所,
th.col_着順,
th.col_馬番,
th.col_枠番,
th.col_人気{
  width: 2.25em;
}
th.col_タイトル,
th.col_馬名{
  width: 13em;
}
th.col_形式{
  width: 4.5em;
}
th.col_距離,
th.col_天候,
th.col_状態{
  width: 2.5em;
}
th.col_時刻{
  width: 3.5em;
}
th.col_情報1,
th.col_情報2{
  width: 2.75em;
}
th.col_レコード{
  width: 4.5em;
}
th.col_性,
th.col_齢{
  width: 1.25em;
}
th.col_斤量,
th.col_上り{
  width: 2.5em;
}
th.col_騎手,
th.col_調教師{
  width: 4em;
}
th.col_タイム{
  width: 4.5em;
}
th.col_着差{
  width: 4em;
}
th.col_オッズ{
  width: 3.5em;
}
th.col_通過{
  width: 6.25em;
}
th.col_所属{
  width: 2.25em;
}
th.col_馬体重{
  width: 3.25em;
}
th.col_増減{
  width: 2.25em;
}
.raceresults tbody td.x-even{
  background: #ddd;
}
td.col_場所,
td.col_R,
td.col_天候,
td.col_状態,
td.col_着順,
td.col_枠番,
td.col_馬番,
td.col_人気,
td.col_所属{
  text-align: center;
}
td.col_形式,
td.col_情報1,
td.col_姓,
td.col_オッズ,
td.col_馬体重,
td.col_増減,
td.col_騎乗数,
td.col_1着,
td.col_2着,
td.col_3着,
td.col_単勝率,
td.col_連対率,
td.col_複勝率{
  text-align: right;
}
/* .rankinfo_initnone_mid,
.rankinfo_initnone_end{
  display: none;
} */
.rankinfo_initdisp_end,
.rankinfo_initdisp_topend{
  border-bottom: 3px double #999;
}
.rankinfo_initnone_end{
  border-bottom: 3px solid #999;
}
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_場所,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_R,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_タイトル,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_形式,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_距離,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_情報1,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_情報2,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_レコード,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_天候,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_状態,
table.raceresults tbody tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) .col_時刻{
  text-indent: 200%;
  white-space: nowrap;
  overflow: hidden;
}
tr.rankinfo_initdisp_top td.coursetype_芝{
  /* background: linear-gradient(transparent 80%, #45af4c 20%); */
  /* color: #45af4c; */
  /* border-right: 1px solid #45af4c !important; */
  /* border-bottom: 1px solid #45af4c !important; */
  background: #45af4c !important;
  color: #ffffff;
}
tr.rankinfo_initdisp_top td.coursetype_ダート{
  /* background: linear-gradient(transparent 80%, #ee9738 20%); */
  /* color: #ee9738; */
  /* border-right: 1px solid #ee9738 !important; */
  /* border-bottom: 1px solid #ee9738 !important; */
  background: #ee9738 !important;
  color: #ffffff;
}
</style>