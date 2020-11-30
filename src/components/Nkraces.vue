<template>
  <div class="component-root">
    <nav class="dispplacerace navbar">
      <div class="dispplace">
        <h5><span class="badge bg-secondary">場所</span></h5>
        <div class="btn-group">
          <button class="dispallplace btn btn-outline-primary btn-sm"
            @click="dispCategory($event, 'all', 'all', 'all')"
          >ALL</button>
          <button class="dispplace btn btn-outline-primary btn-sm"
            v-for="place in places"
            @click="dispCategory($event, place, 'all', 'all')"
            :key="place"
          >{{ place }}</button>
        </div>
      </div>
      <div class="dispcoursetype">
        <h5><span class="badge bg-secondary">コース</span></h5>
        <div class="btn-group">
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
      </div>
      <div class="disprace">
        <h5><span class="badge bg-secondary">レース</span></h5>
        <div class="btn-group">
          <button class="dispallraces btn btn-outline-secondary btn-sm"
            @click="dispCategory($event, 'all', 'all', 'all')"
          >ALL</button>
          <button class="dispracenum btn btn-outline-secondary btn-sm"
            v-for="idx in 12"
            @click="dispCategory($event, 'all', 'all', idx)"
            :key="idx"
          >{{ idx }}</button>
        </div>
      </div>
      <!-- <div>
        <button class="crawl btn btn-outline-primary btn-sm" style="display: auto; width: auto;">api</button>
      </div> -->
    </nav>
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
            @click="if(!['A', 'BUTTON'].includes($event.target.tagName)){
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
            >
              <Nkracetd :text="String(record[col])" :record="record" :dispmode="getDispmode(col)"/>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <GeneralDialog/>
  </div>
</template>

<script>
import { reactive/*, onMounted, ref, onBeforeUpdate*/ } from 'vue'
import Nkracetd from './Nkracetd.vue'
import GeneralDialog from './GeneralDialog.vue'
import $ from 'jquery'
import axios from 'axios'
export default  {
  name: 'Nkraces',
  components: {
    Nkracetd,
    GeneralDialog
  },
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
    const getDispmode = (col)=>{
      let response = {hasBtn: false, hasLink: false, urlinfo: null, callback: null};
      if(col === 'タイトル') response = {hasBtn: true, hasLink: true, urlinfo: '結果URL', callback: getModal, params: getResults_params};
      else if(col === '馬名') response = {hasBtn: true, hasLink: true, urlinfo: '馬URL', callback: getModal, params: getHorseInfo_params};
      return response;
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
        $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css({'border-bottom': '3px double #999'});
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
      dispCategory,
      dispCoursetype,
      dispPlace,
      dispRacenum,
      dispRankinfo,
      flipDispPlace,
      makeClass,
      getDispmode,
      wlog
    }
  }
};
const getHorseInfo_params = {
  url_obj: {
    replace: {from: 'https://db.netkeiba.com/', to: '/nkdb/'}
  },
  body_sel: '#contents table.db_h_race_results.nk_tb_common',
  remove_sel_list: ['thead img'],
  title_sel: '#db_main_box .horse_title h1',
  replace_obj: [],
  css_obj: [
    {select: 'th, td', css: {'white-space': 'nowrap', 'padding': '0.05em'}},
  ]
};
const getResults_params = {
  url_obj: {
    replace: {from: 'https://race.netkeiba.com/race/result.html?race_id=', to: '/nkrace/'}
  },
  body_sel: '.Result_Pay_Back',
  remove_sel_list: ['div.Description_Box_Corner'],
  title_sel: '.RaceList_NameBox .RaceName',
  replace_obj: [
    {select: 'h2', replacer: {start: '<h6><span class="badge bg-secondary">', end: '</span></h6>'}}
  ],
  css_obj: [
    {select: 'div.FullWrap', css: {display: 'flex'}},
    {select: 'th, td', css: {'white-space': 'nowrap', 'padding': '0.05em'}},
    {select: 'ol, ul', css: {display: 'flex', margin: 0, padding: 0, 'list-style': 'none'}},
    {select: 'li', css: {'margin-right': 'auto'}},
    {select: 'td.Ninki', css: {display: 'flex', 'flex-direction': 'column'}}
  ]
};
const getModal = (url, params)=>{
  axios.get(url.replace(params.url_obj.replace.from, params.url_obj.replace.to))
  .then((response)=>{
    const htmltext = response.data;
    const parsed_html = $.parseHTML(htmltext);
    let $modal_body = $(parsed_html).find(params.body_sel);
    params.remove_sel_list.forEach((value)=>{$modal_body.find(value).remove()});
    let modal_title = $(parsed_html).find(params.title_sel).text().trim();
    $('#modal-label').html(`<span class="badge bg-primary">${modal_title}</span>`);
    $('#modal-wrapper .modal-body').empty().append($modal_body).wrapInner('<div class="scrollable">')
    .find('table').addClass('table table-sm table-hover table-striped');
    params.replace_obj.forEach((value)=>{
      $('div.modal').find(value.select).each(function(){
        $(this).replaceWith(`${value.replacer.start}${this.innerHTML}${value.replacer.end}`);
      })
    });
    params.css_obj.forEach((value)=>{$('div.modal').find(value.select).css(value.css)});
    $('#display-modal-btn').click();
    // $('#modal-wrapper').modal('show')
  })
};
</script>

<style scoped>
nav.dispplacerace{
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 4px;
}
nav.dispplacerace > div{
  display: flex;
  align-items: center;
  /* padding: 4px; */
}
nav.dispplacerace > div > h5{
  /* width: 60px; */
  margin: 0 4px;
  /* text-align: end; */
}
nav.dispplacerace h5 > span.bg-secondary{
  width: 80px;
  line-height: unset;
}
/* nav.dispplacerace > div > h5 > span.badge{
  width: 60px;
  margin: 0 8px;
  text-align: end;
} */
nav.dispplacerace button{
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
  text-indent: 500%;
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
/* table.db_h_race_results.nk_tb_common th,
table.db_h_race_results.nk_tb_common td{
  border: 1px solid #000;
} */
</style>