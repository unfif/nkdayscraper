<template>
  <span>
    <button v-if="displaymode.hasBtn"
      type="button" class="btn btn-sm btn-outline-info"
      @click="displaymode.callback(record[displaymode.urlinfo], displaymode.params)"
    >
    </button>
    <span v-if="!displaymode.hasLink">
      {{ text !== 'null' ? text : '' }}
    </span>
    <span v-else>
      <a :href="record[displaymode.urlinfo]" ref="ref_target"
        target="_blank" rel="noopener noreferrer" aria-describedby="tooltip"
      >
        {{ text !== 'null' ? text : '' }}
      </a>
      <GeneralTooltip v-if="['結果URL', '馬URL'].includes(displaymode.urlinfo)"
        :target="ref_target"
        :placement="displaymode.urlinfo === '馬URL' ? 'right' : 'bottom'"
        :callback="getCaptionFromEachUrl(displaymode.urlinfo)"
        :callbackParam="getCallbackParamFromEachUrl(ref_target, displaymode.urlinfo)"
      />
    </span>
  </span>
</template>

<script>
import { ref } from 'vue'
import GeneralTooltip from './GeneralTooltip.vue'
import axios from 'axios'

export default {
  name: 'NkRaceTd',
  components: {
    GeneralTooltip
  },
  props: {
    text: {
      type: String,
      default: ''
    },
    displaymode: {
      type: Object,
      default: ()=>({
        hasBtn: false,
        hasLink: false,
        urlinfo: null,
        callback: ()=>{}
      })
    },
    record: {
      type: Object,
      default: ()=>({})
    }
  },
  setup(){
    const ref_target = ref(null);

    const getCaptionFromEachUrl = (urlType)=>{
      if(urlType != null){
        if(urlType === '馬URL') return getPedigreeFromHorseId;
        else if(urlType === '結果URL') return getRaceInfoFromRaceId;
      }
    }

    const getCallbackParamFromEachUrl = (target, urlType)=>{
      if(urlType != null && target != null){
        let param;
        if(urlType === '馬URL'){
          const horse_id = target.href.split('/').pop();
          param = horse_id;
        }else if(urlType === '結果URL'){
          let querys = {};
          const keyvalues = target.href.split('?').pop().split('&');
          keyvalues.forEach((keyvalue)=>{
            keyvalue = keyvalue.split('=');
            querys[keyvalue[0]] = keyvalue[1];
          })
          param = querys.race_id;
        }
        return param;
      }
    }

    return {
      ref_target,
      getCaptionFromEachUrl,
      getCallbackParamFromEachUrl
    }
  }
}

const getPedigreeFromHorseId = async (horse_id)=>{
  const response = await axios.get(`http://localhost:5000/pedigree/${horse_id}`);
  const parser = new DOMParser();
  const html = parser.parseFromString(response.data, 'text/html');
  const sire_tds = html.querySelectorAll('table.blood_table.detail tbody td');
  const sire_td_rowspan = sire_tds[0].rowSpan;
  const sire_name = sire_tds[0].querySelector('a').innerText.split('\n')[0];
  const mare_name = sire_tds[sire_td_rowspan * 2 - 1].querySelector('a').innerText.split('\n')[0];
  const broodmare_sire_name = sire_tds[sire_td_rowspan * 2].querySelector('a').innerText.split('\n')[0];
  return `父：${sire_name}、母父：${broodmare_sire_name}、母：${mare_name}`;
}

const getRaceInfoFromRaceId = async (race_id)=>{
  const response = await axios.get(`http://localhost:5000/nkrace/${race_id}`);
  const parser = new DOMParser();
  const html = parser.parseFromString(response.data, 'text/html');
  const raceList_item02 = html.querySelectorAll('.RaceList_NameBox .RaceList_Item02');
  return raceList_item02[0].innerText;
}
</script>

<style scoped>
</style>
