<template>
    <div class="popper-tooltip" role="tooltip" ref="ref_tooltip">
      {{ data.tooltip }}
      <div class="popper-arrow" data-popper-arrow></div>
    </div>
</template>

<script>
import { ref, reactive, onUpdated } from 'vue'
import { createPopper } from "@popperjs/core"
import axios from 'axios'

const showEvents = ['mouseenter', 'focus'];
const hideEvents = ['mouseleave', 'blur'];

const getPedigreeFromHorseId = async (horse_id)=>{
  const response = await axios.get(`http://localhost:5000/pedigree/${horse_id}`);
  const parser = new DOMParser();
  const html = parser.parseFromString(response.data, 'text/html');
  const sire_tds = html.querySelectorAll('table.blood_table.detail tbody td');
  const sire_td_rowspan = sire_tds[0].rowSpan;
  const sire_name = sire_tds[0].querySelector('a').innerText.split('\n')[0];
  const mare_name = sire_tds[sire_td_rowspan * 2 - 1].querySelector('a').innerText.split('\n')[0];
  const broodmare_sire_name = sire_tds[sire_td_rowspan * 2].querySelector('a').innerText.split('\n')[0];
  return `父：${sire_name}、母：${mare_name}、母父：${broodmare_sire_name}`;
}

const getRaceInfoFromRaceId = async (race_id)=>{
  const response = await axios.get(`http://localhost:5000/nkrace/${race_id}`);
  const parser = new DOMParser();
  const html = parser.parseFromString(response.data, 'text/html');
  const raceList_item02 = html.querySelectorAll('.RaceList_NameBox .RaceList_Item02');
  return raceList_item02[0].innerText;
}

export default {
  name: 'NkTooltip',
  props: {
    target: {
      default: ref(null)
    },
    displaymode: {
      Object,
      default: {
        hasBtn: false,
        hasLink: false,
        urlinfo: null,
        callback: ()=>{}
      }
    }
  },
  setup(props){
    const ref_tooltip = ref(null);

    const data = reactive({
      tooltip: ''
    })

    onUpdated(()=>{
      const target = props.target;
      const tooltip = ref_tooltip.value;

      if(props.displaymode.hasLink && ['結果URL', '馬URL'].includes(props.displaymode.urlinfo)){
        let placement = 'bottom';
        if(props.displaymode.urlinfo === '馬URL') placement = 'right';
        const popperInstance = createPopper(target, tooltip, {
          placement: placement,
          modifiers: [
            {
              name: 'offset',
              options: {
                offset: [0, 8],
              },
            },
          ],
        });

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
          popperInstance.setOptions({
            modifiers: [{ name: 'eventListeners', enabled: true }],
          });
          popperInstance.update();
          setTimeout(hide, 2000);
        }

        const hide = ()=>{
          tooltip.removeAttribute('data-show');
          popperInstance.setOptions({
            modifiers: [{ name: 'eventListeners', enabled: false }],
          });
        }
        
        showEvents.forEach(event => {
          target.addEventListener(event, show);
        });

        hideEvents.forEach(event => {
          target.addEventListener(event, hide);
        });

      }
    });

    return {
      data,
      ref_tooltip
    }
  }
};
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

.popper-arrow,
.popper-arrow::before {
  position: absolute;
  width: 8px;
  height: 8px;
  background: inherit;
}

.popper-arrow {
  visibility: hidden;
}

.popper-arrow::before {
  visibility: visible;
  content: '';
  transform: rotate(45deg);
}

.popper-tooltip[data-popper-placement^='top'] > .popper-arrow {
  bottom: -4px;
}

.popper-tooltip[data-popper-placement^='bottom'] > .popper-arrow {
  top: -4px;
}

.popper-tooltip[data-popper-placement^='left'] > .popper-arrow {
  right: -4px;
}

.popper-tooltip[data-popper-placement^='right'] > .popper-arrow {
  left: -4px;
}
</style>