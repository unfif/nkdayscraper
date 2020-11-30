<template>
  <span>
    <button
      v-if="dispmode.hasBtn" type="button" class="horseinfomodalbtn btn btn-sm btn-outline-info"
      @click="dispmode.callback(record[dispmode.urlinfo], dispmode.params)"
    >
    </button>
    <span v-if="!dispmode.hasLink">
      {{ text }}
    </span>
    <a
      v-else-if="dispmode.hasLink"
      :href="record[dispmode.urlinfo]"
      target="_blank"
      rel="noopener noreferrer"
      data-toggle="tooltip" data-placement="right" data-html="false" title="父：サンデーサイレンス 母：ウインドインハーヘア"
    >
      {{ text }}
    </a>
  </span>
</template>

<script>
// import axios from 'axios'
// import $ from 'jquery'

export default {
  name: 'Nkracetd',
  props: {
    text: {
      String,
      'default': ''
    },
    dispmode: {
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
  setup(){
    // const getUrl = (urlinfo, record, dispmode)=>{
    //   let url = String(urlinfo).startsWith('http') ? urlinfo : record[dispmode[urlinfo]];
    //   return url;
    // }
    // const getHorseInfoForModal = (url)=>{// '/nkdb/horse/2015104107'// https://db.netkeiba.com/horse/2015104793
    //   axios.get(url.replace('https://db.netkeiba.com/', '/nkdb/'))
    //   .then((res)=>{
    //     const htmltext = res.data;
    //     const html = $.parseHTML(htmltext);
    //     const $contents = $(html).find('#contents');
    //     let $race_results_tbl = $contents.find('table.db_h_race_results.nk_tb_common');
    //     let horsename = $contents.find('#db_main_box .horse_title h1').text().trim();
    //     $race_results_tbl.find('thead').find('img').remove();
    //     $race_results_tbl
    //     .addClass('table table-sm table-hover table-striped')
    //     .find('th, td').css({'white-space': 'nowrap', 'padding': '0.05em'});
    //     $('h5#horseInfoModalLabel').text(horsename);
    //     // $race_results_tbl.wrap('<div class="scrollable"></div>');
    //     $('#horseInfoModal div.modal-body').empty().append($race_results_tbl).wrapInner('<div class="scrollable"></div>');
    //     $('#horseinfomodalshowbtn').click();
    //     // $('#horseInfoModal').modal('show')
    //   })
    // }
    // const getResultForModal = (url)=>{// '/nkdb/horse/2015104107'// https://db.netkeiba.com/horse/2015104793
    //   axios.get(url.replace('https://db.netkeiba.com/', '/nkdb/'))
    //   .then((response)=>{
    //     const htmltext = response.data;
    //     const html = $.parseHTML(htmltext);
    //     const $contents = $(html).find('#contents');
    //     let $race_results_tbl = $contents.find('table.db_h_race_results.nk_tb_common');
    //     let horsename = $contents.find('#db_main_box .horse_title h1').text().trim();
    //     $race_results_tbl.find('thead').find('img').remove();
    //     $race_results_tbl
    //     .addClass('table table-sm table-hover table-striped')
    //     .find('th, td').css({'white-space': 'nowrap', 'padding': '0.05em'});
    //     $('h5#horseInfoModalLabel').text(horsename);
    //     // $race_results_tbl.wrap('<div class="scrollable"></div>');
    //     $('#horseInfoModal div.modal-body').empty().append($race_results_tbl).wrapInner('<div class="scrollable"></div>');
    //     $('#horseinfomodalshowbtn').click();
    //     // $('#horseInfoModal').modal('show')
    //   })
    // }
    // return {
    //   getHorseInfoForModal,
    //   getResultForModal
    // }
  }
}
</script>

<style scoped>

</style>
