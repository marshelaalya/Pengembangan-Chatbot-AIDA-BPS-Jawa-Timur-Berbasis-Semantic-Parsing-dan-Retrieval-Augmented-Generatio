import { createStore } from 'vuex'

export default createStore({
  state: {
    mfd: null
  },
  mutations: {
    setMfd(state, mfd) {
      state.mfd = mfd
    }
  },
  actions: {
  },
  modules: {
  }
})