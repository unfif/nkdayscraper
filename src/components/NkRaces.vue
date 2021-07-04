<template>
  <NkNav :places="places" @click-nav-button="showTargets($event)"/>
  <div class="dispraceresults scrollable">
    <table class="raceresults table table-sm table-hover table-striped-inactive">
      <thead class="table-dark">
        <tr>
          <th v-for="col in cols" :key="col" :class="`col_${col}`">{{ col }}</th>
        </tr>
      </thead>
      <tbody v-if="!is_raceLoading">
        <tr v-for="record in records.data" :key="record.index"
          v-show="showTargetByRecordMap(record, [{place: '場所'}, {racenum: 'R'}, {coursetype: '形式'}]) && showTargetByRankInfo(record.rankinfo)"
          :class="makeClassesFromRecord(record, ['場所', '形式', 'R', '着順', 'index', 'rankinfo'])"
          @click="flipDisplayTargets($event, record)"
        >
          <td v-for="(col, index) in cols" :key="`${record.index}_${col}`"
            :class="[`col_${col}`, makeClass(col, record), !Boolean(index % 2) ? 'x-odd' : 'x-even']"
            :style="makeDistanceStyle(col, record)"
          >
            <NkRaceTd :text="String(record[col])" :record="record" :displaymode="getDisplayMode(col)"/>
          </td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr v-for="index in 9" :key="index"><td>&nbsp;</td></tr>
      </tbody>
    </table>
  </div>
  <GeneralDialog/>
</template>

<script>
import { reactive, computed } from 'vue'
import NkNav from './NkNav.vue'
import NkRaceTd from './NkRaceTd.vue'
import GeneralDialog from './GeneralDialog.vue'
import axios from 'axios'

export default {
  name: 'NkRaces',
  components: {
    NkNav,
    NkRaceTd,
    GeneralDialog
  },
  props: {
    places: {
      type: Array,
      default: ()=>[]
    },
    cols: {
      type: Array,
      default: ()=>[]
    },
    records: {
      type: Object,
      default: ()=>{
        return {
          schema: {fields: null},
          data: []
        }
      }
    },
    is_raceLoading: {
      type: Boolean,
      default: true
    }
  },
  setup(){
    const data = reactive({
      place: 'all',
      coursetype: 'all',
      racenum: 11,
      is_show_all_ranks: false
    })

    const getDisplayMode = computed(()=>(col)=>{
      let response = {hasBtn: false, hasLink: false, urlinfo: null, callback: null};
      if(col === 'タイトル') response = {hasBtn: true, hasLink: true, urlinfo: '結果URL', callback: getModal, params: getResults_params};
      else if(col === '馬名') response = {hasBtn: true, hasLink: true, urlinfo: '馬URL', callback: getModal, params: getHorseInfo_params};
      else if(col === '騎手') response = {hasBtn: false, hasLink: true, urlinfo: '騎手URL', callback: null, params: null};
      else if(col === '調教師') response = {hasBtn: false, hasLink: true, urlinfo: '調教師URL', callback: null, params: null};
      return response;
    })

    const showTargets = (event)=>{
      data.place = event.data.place;
      data.coursetype = event.data.coursetype;
      data.racenum = event.data.racenum;
      data.is_show_all_ranks = event.data.is_show_all_ranks;
    }

    const showTargetByRecordMap = computed(()=>(record, map)=>{
      return map.reduce((acc, cur)=>{
        const key = Object.keys(cur)[0];
        return acc && (data[key] === 'all' ? true : record[cur[key]] == data[key]);
      }, true)
    })

    const showTargetByRankInfo = computed(()=>(rankinfo)=>{
      return data.is_show_all_ranks ? true : rankinfo.startsWith('initdisp_');
    })

    const flipDisplayTargets = computed(()=>(event, record)=>{
      if(!['A', 'BUTTON'].includes(event.target.tagName)){
        data.is_show_all_ranks = !data.is_show_all_ranks
        data.place = record.場所;
        data.racenum = record.R;
        flipDisplayForSameRoundRaces(event);
      }
    })

    const flipDisplayForSameRoundRaces = (event)=>{
      if(!data.is_show_all_ranks && event.target.tagName === 'TD') data.place = 'all';
    }

    const makeClass = computed(()=>(col, record)=>{
      if(col === '形式') return `coursetype_${record[col]}`;
      else if(col === '枠番') return `postnum_${record[col]}`;
      else if(col === '人気') return `rank_${record[col]}`;
      else if(col === '上り') return `rank_${record['last3frank']}`;
      else if(col === '所属' && record[col] === '栗東') return 'text-success';
    })

    const makeClassesFromRecord = (record, prefixes)=>{
      const classes = prefixes.map((prefix)=>{
        return `${prefix}_${record[prefix]}`;
      })
      return classes;
    }

    const makeDistanceStyle = (col, record)=>{
      if(record['rankinfo'] === 'initdisp_top' && col === '距離'){
        return {background: 'linear-gradient(transparent 80%, ' + (record[col] <= 1600 ? '#ee9738' : '#45af4c') + ' 20%'}
      }
    }

    return {
      data,
      getDisplayMode,
      showTargets,
      showTargetByRecordMap,
      showTargetByRankInfo,
      flipDisplayTargets,
      flipDisplayForSameRoundRaces,
      makeClass,
      makeClassesFromRecord,
      makeDistanceStyle
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
    {select: 'th', css: {'whiteSpace': 'nowrap', 'padding': '0.05em'}},
    {select: 'td', css: {'whiteSpace': 'nowrap', 'padding': '0.05em'}},
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
    {select: 'th', css: {'whiteSpace': 'nowrap', 'padding': '0.05em'}},
    {select: 'td', css: {'whiteSpace': 'nowrap', 'padding': '0.05em'}},
    {select: 'ol', css: {display: 'flex', margin: 0, padding: 0, 'listStyle': 'none'}},
    {select: 'ul', css: {display: 'flex', margin: 0, padding: 0, 'listStyle': 'none'}},
    {select: 'li', css: {'marginRight': 'auto'}},
    {select: 'td.Ninki', css: {display: 'flex', 'flexDirection': 'column'}}
  ]
};

const getModal = (url, params)=>{
  axios.get(url.replace(params.url_obj.replace.from, params.url_obj.replace.to))
  .then((response)=>{
    const htmltext = response.data;
    const parser = new DOMParser();
    const doc = parser.parseFromString(htmltext, 'text/html');
    let modal_body = doc.querySelector(params.body_sel);
    modal_body.parentNode.querySelectorAll('table').forEach(
      (table)=>{table.classList.add('table', 'table-sm', 'table-hover', 'table-striped', 'col', 'mx-1')}
    );
    params.remove_sel_list.forEach((value)=>{
      if(modal_body.querySelector(value) != null) modal_body.querySelector(value).remove();
    });
    let modal_title = doc.querySelector(params.title_sel).innerText.trim();
    document.querySelector('#modal-title').innerHTML = `<span class="badge bg-primary">${modal_title}</span>`;
    document.querySelector('#modal-wrapper .modal-body').innerHTML = `<div class="scrollable">${modal_body.outerHTML}<div>`;
    params.replace_obj.forEach((value)=>{
      document.querySelectorAll(`div.modal ${value.select}`).forEach(
        (node, index, nodeList)=>{nodeList[index].outerHTML = `${value.replacer.start}${node.innerHTML}${value.replacer.end}`}
      )
    });
    params.css_obj.forEach((value)=>{
      document.querySelectorAll(`div.modal ${value.select}`).forEach(
        (node, index, nodeList)=>{
          for(let property in value.css){
            nodeList[index].style[property] = value.css[property];
          }
        }
      )
    });
    document.querySelector('#display-modal-btn').click();
  })
};
</script>

<style lang="scss" scoped>
.table-sm {
  th,
  td {
    white-space: nowrap;
  }
}

th.col_R,
th.col_場所,
th.col_着順,
th.col_馬番,
th.col_枠番,
th.col_人気,
th.col_所属,
th.col_増減 {
  width: 2.25em;
}
th.col_タイトル,
th.col_馬名 {
  width: 13em;
}
th.col_形式,
th.col_レコード,
th.col_タイム {
  width: 4.5em;
}
th.col_距離,
th.col_天候,
th.col_状態,
th.col_斤量,
th.col_上り {
  width: 2.5em;
}
th.col_時刻,
th.col_オッズ {
  width: 3.5em;
}
th.col_情報1,
th.col_情報2 {
  width: 2.75em;
}
th.col_性,
th.col_齢 {
  width: 1.25em;
}
th.col_騎手,
th.col_調教師,
th.col_着差 {
  width: 4em;
}
th.col_通過 {
  width: 6.25em;
}
th.col_馬体重 {
  width: 3.25em;
}

.raceresults tbody td.x-even {
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
td.col_所属 {
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
td.col_複勝率 {
  text-align: right;
}

table.raceresults tbody {
  tr.rankinfo_initdisp_top,
  tr.rankinfo_initdisp_topend {
    border-top: 3px solid #999;
  }
  tr:not(.rankinfo_initdisp_top):not(.rankinfo_initdisp_topend) {
    .col_場所,
    .col_R,
    .col_タイトル,
    .col_形式,
    .col_距離,
    .col_情報1,
    .col_情報2,
    .col_レコード,
    .col_天候,
    .col_状態,
    .col_時刻 {
      text-indent: 500%;
      white-space: nowrap;
      overflow: hidden;
    }
  }
}

tr.rankinfo_initdisp_top {
  td.coursetype_芝 {
    background: #45af4c !important;
    color: #ffffff;
  }
  td.coursetype_ダート {
    background: #ee9738 !important;
    color: #ffffff;
  }
}
</style>
