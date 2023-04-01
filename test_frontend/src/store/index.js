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
    area:null
  },
  plugins: [persistedState],
  mutations: {
    access(state, access) {
      state.accessToken = access.accessToken;
      state.uid = access.uid;
      state.corporateName = access.corporateName;
    },
    resetState(state) {
      Object.assign(state, getDefaultState());
    },
  },
  actions: {
    // signUserIn({ commit }, payload) {
    //   commit("setLoading", false);
    //   const loggedUser = payload;
    //   commit("setUser", loggedUser);
    // },
    // autoSignIn({ commit }, payload) {
    //   const userRef = doc(db, "Users", payload);
    //   getDoc(userRef)
    //     .then((snapshot) => {
    //       const user_obj = snapshot.data();
    //       console.log(user_obj);
    //       commit("setUser", user_obj);
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    // },
    // logout({ commit }) {
    //   const auth = getAuth();
    //   signOut(auth)
    //     .then(() => {
    //       console.log("User is signed out!");
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    //   commit("setUser", null);
    // },
    // updatePetArray({ commit }, payload) {
    //   const arrayRef = doc(db, "Users", payload.userid);
    //   updateDoc(arrayRef, { listedPets: arrayUnion(payload) })
    //     .then(() => {
    //       console.log("PetID updated in user database");
    //       commit("addPetArray", payload);
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //       console.log("PetID failed to update in user database");
    //     });
    // },
    // deletePetArray({ commit }, payload) {
    //   const petid = payload.petid;
    //   deleteDoc(doc(db, "Pets", petid))
    //     .then(() => {
    //       // console.log(this.store.state.user.listedPets)
    //       var updatedUser = this.getters.getuser;
    //       console.log(1);
    //       console.log(updatedUser);
    //       var listedPets = updatedUser.listedPets;
    //       console.log(listedPets);
    //       var index = listedPets.indexOf(payload);
    //       console.log(index);
    //       listedPets.splice(index, 1);
    //       console.log(listedPets);
    //       updatedUser.listedPets = listedPets;
    //       console.log("Pet has been deleted from pet database");
    //       // mutations
    //       // commit('deletePetArr', listedPets)
    //       commit("deletePetArr", listedPets);
    //     })
    //     .catch((err) => {
    //       console.log(err);
    //     });
    // },
    // deleteUserArray(payload) {
    //   const docRef = doc(db, "Users", payload.userid);
    //   updateDoc(docRef, payload.listedPets)
    //     .then(() => {
    //       console.log(0);
    //       console.log("Pet has been removed in user database");
    //     })
    //     .catch((err) => {
    //       console.log(1);
    //       console.log(err);
    //     });
    // },
    // loadedPet({ commit }, petid) {
    //   const petRef = doc(db, "Pets", petid);
    //   getDoc(petRef).then((snapshot) => {
    //     const pet_obj = snapshot.data();
    //     commit("changePetid", pet_obj);
    //   });
    // },
    // setOthers({ commit }, payload) {
    //   commit("setOthers", payload);
    // },
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
  },
});

function getDefaultState() {
  return {
    accessToken: null,
    uid: null,
    corporateName: null,
  };
}
