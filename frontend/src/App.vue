<template>
  <div id="app">

    <nav class="navbar navbar-dark navbar-expand-sm bg-success fixed-top">
        <div class="container">
            <a class="navbar-brand" href="/">KanBan App</a>
            <ul class="navbar-nav mr-auto">
                <li class="nav-item"><a class="nav-link" href="http://localhost:8080/home">Home</a></li>
            </ul>

            <ul class="navbar-nav navbar-right">
                <div v-if="$store.state.loggedIn === true">
                  <button class="nav-item lgbtn btn-danger rounded"  v-on:click="logoutUser">Logout</button>
                </div>
                    
                <div v-else>
                  <button class="nav-item lgbtn btn-primary rounded" @click="loginUser">Sign In</button>
                  <button class="nav-item lgbtn btn-warning rounded" @click="signUpUser">Sign Up</button>
                </div>
            </ul>
        </div>
    </nav>


  
    <router-view class="content"/>
  </div>
</template>

<script>

  import Vuex from 'vuex'
  import store from './store/index.js'
  export default {
    methods:{
      ...Vuex.mapActions(['logoutUser']),
      loginUser(){
        this.$router.push({name : 'login'})
      },
      signUpUser(){
        this.$router.push({ name: 'signup' })
      }
    },
    data(){
      return {
        loggedData : store.state.loggedIn
      }
      
    }
  }
</script>



<style lang="scss">
.content{
  margin-top: 100px;
  margin-left: 20px;
  margin-right: 20px;
}
.lgbtn{
  margin-left: 10px;
  padding: 5px;
  color: white;
}
</style>