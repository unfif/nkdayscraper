<template>
  <span>
    <button v-if="displaymode.hasBtn"
      type="button" class="horseinfomodalbtn btn btn-sm btn-outline-info"
      @click="displaymode.callback(record[displaymode.urlinfo], displaymode.params)"
    >
    </button>
    <span v-if="!displaymode.hasLink" v-once>
      {{ text }}
    </span>
    <a v-else v-once
      :href="record[displaymode.urlinfo]"
      target="_blank"
      rel="noopener noreferrer"
      aria-describedby="tooltip"
      ref="ref_target"
    >
      {{ text }}
    </a>
    <div class="popper-tooltip" role="tooltip" ref="ref_tooltip">
      {{ data.tooltip }}
      <div id="arrow" data-popper-arrow></div>
    </div>
  </span>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { createPopper } from "@popperjs/core"
import axios from 'axios'

export default {
  name: 'NkRaceTd',
  props: {
    text: {
      String,
      'default': ''
    },
    displaymode: {
      Object,
      'default': {
        hasBtn: false,
        hasLink: false,
        urlinfo: null,
        callback: ()=>{}
      }
    },
    record: {
      Object,
      'default': {}
    }
  },
  setup(props){
    const ref_target = ref(null);
    const ref_tooltip = ref(null);

    const data = reactive({
      tooltip: ''
    })

    onMounted(()=>{
      const target = ref_target.value;
      const tooltip = ref_tooltip.value;
      let popper = null;

      const create = ()=>{
        let placement = 'bottom';
        if(props.displaymode.urlinfo === '馬URL') placement = 'right';
        popper = createPopper(target, tooltip, {
          placement: placement,
          modifiers: [
            {
              name: 'offset',
              options: {
                offset: [0, 8]
              }
            }
          ]
        });
      }

      const destroy = ()=>{
        if (popper) {
          popper.destroy();
          popper = null;
        }
      }

      const show = async ()=>{
        if(!data.tooltip){
          if(props.displaymode.urlinfo === '馬URL'){
            const horse_id = target.href.split('/').pop();
            data.tooltip = await getPedigreeFromHorseId(horse_id);
          }else if(props.displaymode.urlinfo === '結果URL'){
            let querys = {};
            const keyvalues = target.href.split('?').pop().split('&');
            keyvalues.forEach((keyvalue)=>{
              keyvalue = keyvalue.split('=');
              querys[keyvalue[0]] = keyvalue[1];
            })
            data.tooltip = await getRaceInfoFromRaceId(querys.race_id);
          }
        }
        tooltip.setAttribute('data-show', '');
        create();
        setTimeout(hide, 2000);
      }

      const hide = ()=>{
        tooltip.removeAttribute('data-show');
        destroy();
      }

      const showEvents = ['mouseenter', 'focus'];
      const hideEvents = ['mouseleave', 'blur'];

      if(target){
        showEvents.forEach((event)=>{
          target.addEventListener(event, show);
        });

        hideEvents.forEach((event)=>{
          target.addEventListener(event, hide);
        });
      }

      const getPedigreeFromHorseId = async (horse_id)=>{
        const response = await axios.get(`http://localhost:5000/pedigree/${horse_id}`);
        const parser = new DOMParser();
        const html = parser.parseFromString(response.data, 'text/html');
        let sire_tds = html.querySelectorAll('table.blood_table.detail tbody td');
        let sire_td_rowspan = sire_tds[0].rowSpan;
        let sire_name = sire_tds[0].querySelector('a').innerText.split('\n')[0];
        let mare_name = sire_tds[sire_td_rowspan * 2 - 1].querySelector('a').innerText.split('\n')[0];
        let broodmare_sire_name = sire_tds[sire_td_rowspan * 2].querySelector('a').innerText.split('\n')[0];
        return `父：${sire_name}、母：${mare_name}、母父：${broodmare_sire_name}`;
      }

      const getRaceInfoFromRaceId = async (race_id)=>{
        const response = await axios.get(`http://localhost:5000/nkrace/${race_id}`);
        const parser = new DOMParser();
        const html = parser.parseFromString(response.data, 'text/html');
        let raceList_item02 = html.querySelectorAll('.RaceList_NameBox .RaceList_Item02');
        return raceList_item02[0].innerText;
      }

    });

    return {
      ref_target,
      ref_tooltip,
      data
    }
  }
}
</script>

<style scoped>
.popper-tooltip {
  background: #333;
  color: white;
  font-weight: bold;
  padding: 4px 8px;
  font-size: 13px;
  border-radius: 4px;
  display: none;
}

.popper-tooltip[data-show] {
  display: block;
}

#arrow,
#arrow::before {
  position: absolute;
  width: 8px;
  height: 8px;
  z-index: -1;
}

#arrow::before {
  content: "";
  transform: rotate(45deg);
  background: #333;
}

.popper-tooltip[data-popper-placement^="top"] > #arrow {
  bottom: -4px;
}

.popper-tooltip[data-popper-placement^="bottom"] > #arrow {
  top: -4px;
}

.popper-tooltip[data-popper-placement^="left"] > #arrow {
  right: -4px;
}

.popper-tooltip[data-popper-placement^="right"] > #arrow {
  left: -4px;
}
</style>
