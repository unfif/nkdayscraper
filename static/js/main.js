$(function(){
  $('.raceresults tr').find('td:visible:odd').css('background', '#ddd');

  $('.raceresults tbody tr').click(function(){
    var $this = $(this);
    var place = $this.attr('data-place');
    var racenum = $this.attr('data-racenum');
    var selplace = '[data-place="' + place + '"]';
    var $tbody = $this.closest('tbody')
    var sameracetr = 'tr[data-place="' + place + '"][data-racenum="' + racenum + '"]'
    var $sameracetr = $tbody.find(sameracetr);
    if($sameracetr.length === 1) return;
    var is_visible_allsameracetr = true;
    $sameracetr.each(function(){
      if($(this).css('display') === 'none') is_visible_allsameracetr = false;
    })
    if(is_visible_allsameracetr){
      $('tr.rankinfo_initdisp_end').css('border-bottom', '3px double #999');
      $tbody.find('tr').hide();
      $tbody.find('tr.rankinfo_initdisp_top' + selplace + ', tr.rankinfo_initdisp_mid' + selplace + ', tr.rankinfo_initdisp_end' + selplace + '').show();
    }else{
      $('tr.rankinfo_initdisp_end').css({'border-color': 'inherit', 'border-width': 0});
      $tbody.find('tr').not(sameracetr).hide();
      $sameracetr.show();
      $('.raceresults tr').find('td:visible:odd').css('background', '#ddd');
    }
  })
  $('tr.rankinfo_initdisp_top td.col_距離').each(function(){
    var distance = Number($(this).text());
    var color = 'white';
    if(distance <= 1600) color = '#ee9738';
    else color = '#45af4c';
    $(this).css({"background": "linear-gradient(transparent 80%, " + color + " 20%)"});
    // $(this).css({"border-right": "1px solid " + color, "border-bottom": "1px solid " + color});
  })
  var lastplace = '';
  $('.racejockeys tbody tr').each(function(){
    var thisplace = $(this).find('th:first')
    if(thisplace.text() === lastplace) thisplace.text('');
    else lastplace = thisplace.text();
  })
  $('button.dispallplaces, button.dispallcoursetypes, button.dispallraces').click(function(){
    $('tr.rankinfo_initdisp_end').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr:not(.rankinfo_initnone_mid, .rankinfo_initnone_end)').show();
    $('.rankinfo_initnone_mid, .rankinfo_initnone_end').hide();
  })
  $('button.dispplace').click(function(){
    $('tr.rankinfo_initdisp_end').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr.場所_' + this.innerText).show();
    $('.raceresults tbody tr:not(.場所_' + this.innerText + ')').hide();
    $('.rankinfo_initnone_mid, .rankinfo_initnone_end').hide();
  })
  $('button.dispcoursetype').click(function(){
    $('tr.rankinfo_initdisp_end').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr.形式_' + this.innerText).show();
    $('.raceresults tbody tr:not(.形式_' + this.innerText + ')').hide();
    $('.rankinfo_initnone_mid, .rankinfo_initnone_end').hide();
  })
  $('button.disprace').click(function(){
    $('tr.rankinfo_initdisp_end').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr.R_' + this.innerText).show();
    $('.raceresults tbody tr:not(.R_' + this.innerText + ')').hide();
    $('.rankinfo_initnone_mid, .rankinfo_initnone_end').hide();
  })
  $('.racejockeys tr').click(function(){
    // var place = $(this).attr('data-place');
    // $('.racejockeys tr.hiddentr[data-place="' + place + '"]').toggle()
    $('.racejockeys tr.hiddentr').toggle()
  })
  $("div.disprace button.disprace:contains('11')").click();
  $('button.crawl').click(function(){
    $.ajax({
      url: 'http://localhost:5000/crawl'
    }).done(function(data){
      console.log(data.p1.output[1]);
      // alert(data.p1.output[1]);
    })
  })
})
