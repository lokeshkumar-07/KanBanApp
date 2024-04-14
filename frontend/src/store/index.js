import FetchFunction, { FetchFunction2 } from '../FetchFunc.js'
import Vue from 'vue'
import Vuex from 'vuex'
import router from '../router/index.js'
import axios from 'axios'

Vue.use(Vuex)

const store =  new Vuex.Store({
  state: {
    loggedIn: localStorage.getItem('token') ? true : false
  },
  getters: {

    getToken(state){
      if (state.loggedIn === true){
        return localStorage.getItem('token')
      }else{
        return null
      }
    }

  },
  mutations: {
    login(state){
      state.loggedIn = true
    },
    logout(state){
      state.loggedIn = false
    }
  },
  actions: {
    

    logoutUser({commit}){
      localStorage.removeItem('token')
      commit('logout')
      router.push({name: 'login'})
    }
  }
})

export default store