<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grid Component</title>
    <link rel="shortcut icon" href="{@url_for('static', filename='favicon.ico')@}">
    <link rel="stylesheet" type="text/css" href="{@url_for('static', filename='css/bootstrap.min.css')@}">
    <link rel="stylesheet" type="text/css" href="{@url_for('static', filename='css/styles-vue.css')@}">
    <script src="{@url_for('static', filename='js/axios.js')@}"></script>
    <script src="{@url_for('static', filename='js/vue.js')@}"></script>
    <script src="{@url_for('static', filename='js/vue-composition-api@0.6.7.js')@}"></script>
    <script type="text/x-template" id="grid-template"><!-- component template -->
      <main>
        <nav class="dispplacerace navbar">
          <div class="dispplace">
            <h5><span class="badge bg-secondary">場所</span></h5>
            <button class="dispallplace btn btn-outline-secondary btn-sm" @click="dispplace = 'all'; dispcoursetype = 'all'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">ALL</button>
            <button class="dispplace btn btn-outline-secondary btn-sm" @click="dispplace = '函館'; dispcoursetype = 'all'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">函館</button>
            <button class="dispplace btn btn-outline-secondary btn-sm" @click="dispplace = '福島'; dispcoursetype = 'all'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">福島</button>
            <button class="dispplace btn btn-outline-secondary btn-sm" @click="dispplace = '阪神'; dispcoursetype = 'all'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">阪神</button>
          </div>
          <div class="dispcoursetype">
            <h5><span class="badge bg-secondary">コース</span></h5>
            <button class="dispallcoursetypes btn btn-outline-secondary btn-sm" @click="dispplace = 'all'; dispcoursetype = 'all'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">ALL</button>
            <button class="dispcoursetype btn btn-outline-secondary btn-sm" @click="dispplace = 'all'; dispcoursetype = '芝'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">芝</button>
            <button class="dispcoursetype btn btn-outline-secondary btn-sm" @click="dispplace = 'all'; dispcoursetype = 'ダート'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">ダート</button>
            <!-- <button class="dispcoursetype btn btn-outline-secondary btn-sm">障害</button> -->
          </div>
          <div class="disprace btn-group">
            <h5><span class="badge bg-secondary">レース</span></h5>
            <button class="dispallraces btn btn-outline-secondary btn-sm" @click="dispplace = 'all'; dispcoursetype = 'all'; dispracenum = 'all'; dispallsameraces = false; flipDispPlace();">ALL</button>
          <!-- <div class="btn-group" role="group" aria-label="Basic example"> -->
            <button
              v-for="idx in 12"
              class="dispracenum btn btn-outline-secondary btn-sm"
              @click="dispplace = 'all'; dispcoursetype = 'all'; dispracenum = idx; dispallsameraces = false; flipDispPlace();"
            >
              {{idx}}
            </button>
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
                  :class="[
                    'col_' + col,
                    {active: sortKey === col}
                  ]"
                  @click="sortBy(col)"
                >
                  {{col | capitalize}}<span class="arrow" :class="sortOrders[col] > 0 ? 'asc' : 'dsc'"></span>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="row in rows"
                :class="[
                  '場所_'+row.場所,
                  '形式_'+row.形式,
                  'R_'+row.R,
                  '着順_'+row.着順,
                  'idx_'+row.index,
                  'rankinfo_'+row.rankinfo
                ]"
                :data-place="row.場所"
                :data-coursetype="row.形式"
                :data-racenum="row.R"
                :data-rank="row.着順"
                :data-idx="row.index"
                :data-rankinfo="row.rankinfo"
                v-show="dispPlace(row.場所) && dispRacenum(row.R) && dispRankinfo(row.rankinfo) && dispCoursetype(row.形式)"
                @click="
                  dispallsameraces = !dispallsameraces
                  dispplace = row.場所;
                  dispracenum = row.R;
                  flipDispPlace();
                "
              >
                <td
                  v-for="(col, index) in cols"
                  :class="[
                    'col_'+col,
                    makeClass(col === '形式', 'coursetype_' + row[col]),
                    makeClass(col === '枠番', 'postnum_' + row[col]),
                    makeClass(col === '人気', 'rank_' + row[col]),
                    makeClass(col === '上り', 'rank_' + row['last3frank']),
                    makeClass(col === '所属' && row[col] === '栗東', 'text-primary'),
                    !Boolean(index % 2) ? 'x-odd' : 'x-even'
                  ]"
                  :style="[
                    col === '距離' && row['rankinfo'] === 'initdisp_top' ? {background: 'linear-gradient(transparent 80%, ' + (row[col] <= 1600 ? '#ee9738' : '#45af4c') + ' 20%'} : ''
                  ]"
                >
                  {{String(row[col])}}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </script>
  </head>
  <body>
    <header>
      <h2>{@records.日程[0]@}</h2>
      {%- for place in places %}
      <h2>{@place@}</h2>
      {%- endfor %}
    </header>
    <div id="grid-root"><!-- grid root element -->
      <form id="search">
        Search <input name="query" v-model="query">
      </form>
      <grid :records="records" :cols="cols" :filter-key="query"></grid>
    </div>
    <div class=sourcedisp>
    </div>
    <script>
      Vue.component("grid", {
        template: "#grid-template",
        // delimiters: ['{|{', '}|}'],
        props: {
          cols: Array,
          records: Array,
          // dispplace: String,
          // dispracenum: Number,
          // dispallsameraces: Boolean
          filterKey: String
        },
        data: function(){
          var sortOrders = {};
          this.cols.forEach(function(key){
            sortOrders[key] = 1;
          });
          return {// 初期値
            dispplace: 'all',
            dispcoursetype: 'all',
            dispracenum: 11,
            dispallsameraces: false,
            sortKey: "",
            sortOrders: sortOrders
          };
        },
        computed: {
          rows: function(){
            var sortKey = this.sortKey;
            var filterKey = this.filterKey && this.filterKey.toLowerCase();
            var order = this.sortOrders[sortKey] || 1;
            var records = this.records;
            if(filterKey){
              records = records.filter(function(row){
                return Object.keys(row).some(function(key){
                  return (String(row[key]).toLowerCase().indexOf(filterKey) > -1);
                });
              });
            }
            if(sortKey){
              records = records.slice().sort(function(a, b){
                a = a[sortKey];
                b = b[sortKey];
                return (a === b ? 0 : a > b ? 1 : -1) * order;
              });
            }
            return records;
          }
        },
        filters: {
          capitalize: function(str){
            return str.charAt(0).toUpperCase() + str.slice(1);
          }
        },
        methods: {
          dispCoursetype: function(coursetype){
            if(this.dispcoursetype === 'all'){
              return true;
            }else{
              return coursetype == this.dispcoursetype;
            }
          },
          dispPlace: function(place){
            if(this.dispplace === 'all'){
              return true;
            }else{
              return place == this.dispplace;
            }
          },
          dispRacenum: function(racenum){
            if(this.dispracenum === 'all'){
              return true;
            }else{
              return racenum == this.dispracenum;
            }
          },
          dispRankinfo: function(rankinfo){
            if(this.dispallsameraces){
              return true;
            }else{
              return rankinfo.startsWith('initdisp_');
            }
          },
          flipDispPlace: function(){
            if(!this.dispallsameraces){
              this.dispplace = 'all';
              $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css('border-bottom', '3px double #999');
            }else{
              $('.rankinfo_initdisp_end, .rankinfo_initdisp_topend').css({'border-color': 'inherit', 'border-width': 0});
            }
          },
          makeClass: function(condition, cls){
            return condition ? cls : ''
          },
          toggleSameRaceTr: function(){
            console.log(!this.dispallsameraces);
            this.dispallsameraces = !this.dispallsameraces;
          },
          sortBy: function(col){
            this.sortKey = col;
            this.sortOrders[col] = this.sortOrders[col] * -1;
          }
        },
        // mounted: function(){
        //   $('.raceresults tr').find('td:visible:odd').css('background', '#ddd');
        //   console.log($('.raceresults tr').find('td:visible:odd'));
        // }
      });

      var cols = ["場所", "R", "タイトル", "形式", "距離", "情報1", "情報2", "レコード", "天候", "状態", "時刻", "着順", "枠番", "馬番", "馬名", "性", "齢", "斤量", "騎手", "タイム", "着差", "人気", "オッズ", "上り", "通過", "所属", "調教師", "馬体重", "増減"];
      var recordsGrid = new Vue({
        el: "#grid-root",
        data: {// 初期化
          query: "",
          cols: cols,
          records: [],
          dispcoursetype: null,
          dispplace: null,
          dispracenum: null,
          dispallsameraces: false
        }
      });
      // axios.get("{@url_for('static', filename='data/json/raceresults.json')@}")
      // .then(response => {recordsGrid.records = response.data.data;console.log(response)})
      // .catch(err => console.log('err:', err))

      // axios.post('http://localhost:8360/v1/graphql', {"query": "{ races { date distance place racenum title coursetype courseinfo1 courseinfo2 jrarecord { time } weather condition posttime horseresults { ranking postnum horsenum horsename sex age jockeyweight jockey time margin fav odds last3f passageratelist affiliate trainer horseweight horseweightdiff } } }"})
      // .then(response => {console.log(response)})
    </script>
    <script src="{@url_for('static', filename='js/jquery-3.5.1.min.js')@}"></script>
    <script src="{@url_for('static', filename='js/bootstrap.bundle.min.js')@}"></script>
    <!-- <script src="{@url_for('static', filename='js/main.js')@}"></script> -->
    <script>
      $(function(){
        recordsGrid.records = JSON.parse('{@records.to_json(orient='table', force_ascii=False)@}').data;
      })
    </script>
  </body>
</html>
