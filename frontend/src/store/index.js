import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex);

const persistedState = createPersistedState({
  key: "my-vuex-store",
});
export const store = new Vuex.Store({
  state: {
    accessToken: null,
    uid: null,
    corporateName: null,
    area: null,
    district: null,
  },
  plugins: [persistedState],
  mutations: {
    access(state, access) {
      state.accessToken = access.accessToken;
      state.uid = access.uid;
      state.corporateName = access.corporateName;
      state.area = access.area;
      state.district = access.district;
    },
    resetState(state) {
      Object.assign(state, getDefaultState());
    },
  },
  getters: {
    getAccessToken(state) {
      return state.accessToken;
    },
    getCorporateName(state) {
      return state.corporateName;
    },
  },
});

function getDefaultState() {
  return {
    accessToken: null,
    uid: null,
    corporateName: null,
    area: null,
    district: null,
  };
}
