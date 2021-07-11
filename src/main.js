import { createApp } from 'vue'
import { createStore } from 'vuex'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.css'

export const store = createStore({
  state () {
    return {
      place: 'all',
      coursetype: 'all',
      racenum: '11',
      is_show_all_ranks: false
    }
  },
  mutations: {
    updateDisplayParams (state, displayParams) {
      state.place = displayParams.place,
      state.coursetype = displayParams.coursetype,
      state.racenum = displayParams.racenum,
      state.is_show_all_ranks = false
    }
  }
})

createApp(App).use(store).mount('#app')
