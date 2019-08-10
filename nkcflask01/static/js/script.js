$(function(){
  $('.col_レースID, .col_タイトル, .col_天候, .col_時刻, .col_発走時刻, .col_日程, .col_グレード, .col_頭数, .col_賞金, .col_raceurl').addClass('hiddentd');
  $('.raceresults tr').find('td:not(.hiddentd):even').css('background', '#ddd');

  $('.raceresults tbody tr').click(function(){
    var place = $(this).attr('data-place');
    var racenum = $(this).attr('data-racenum');
    var $tbody = $(this).closest('tbody')
    var sameracetr = 'tr[data-place="' + place + '"][data-racenum="' + racenum + '"]'
    var $sameracetr = $tbody.find(sameracetr);
    var is_disp_allsameracetr = true;
    $sameracetr.each(function(){
      if($(this).css('display') === 'none') is_disp_allsameracetr = is_disp_allsameracetr && false;
    })
    if(is_disp_allsameracetr){
      $('tr.rankinfo_initend').css('border-bottom', '3px double #999');
      $tbody.find('tr').hide();
      $tbody.find('tr.rankinfo_initdisp, tr.rankinfo_initend').show();
    }else{
      $('tr.rankinfo_initend').css('border-bottom', 'none');
      $tbody.find('tr').not(sameracetr).hide();
      $sameracetr.show();
    }
  })
  var lastplace = '';
  $('.racejockeys tbody tr').each(function(){
    var thisplace = $(this).find('th:first')
    if(thisplace.text() === lastplace) thisplace.text('');
    else lastplace = thisplace.text();
  })
  $('button.dispallplaces, button.dispallraces').click(function(){
    $('tr.rankinfo_initend').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr:not(.initnone, .raceend)').show();
    $('.rankinfo_initnone, .rankinfo_raceend').hide();
  })
  $('button.dispplace').click(function(){
    $('tr.rankinfo_initend').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr.場所_' + this.innerText).show();
    $('.raceresults tbody tr:not(.場所_' + this.innerText + ')').hide();
    $('.rankinfo_initnone, .rankinfo_raceend').hide();
  })
  $('button.disprace').click(function(){
    $('tr.rankinfo_initend').css('border-bottom', '3px double #999');
    $('.raceresults tbody tr.R_' + this.innerText).show();
    $('.raceresults tbody tr:not(.R_' + this.innerText + ')').hide();
    $('.rankinfo_initnone, .rankinfo_raceend').hide();
  })
  $('.racejockeys tr').click(function(){
    var place = $(this).attr('data-place');
    $('.racejockeys tr.hiddentr[data-place="' + place + '"]').toggle()
  })
  $("div.disprace button.disprace:contains('11')").click();
})
