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
    area:null,
    district:null,
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
  actions: {
   
  },
  getters: {
    getuser(state) {
      console.log(state.user);
      return state.user;
    },
    loading(state) {
      return state.loading;
    },
    loadedpet(state) {
      return state.loadedPet;
    },
    listedpet(state) {
      return state.user.listedPets;
    },

    getOthers(state) {
      return state.others;
    },
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
  };
}
