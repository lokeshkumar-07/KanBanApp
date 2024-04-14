<template>
    <div class="home text-center">
      <h1>WelCome to the Kanban App</h1>
      <p>This is A KanBan App In Which you Create Lists. And you can create in as many tasks you want.</p>  
      <div>
        <button class="btn btn-info btn-lg" @click="login">Login</button> <button class="btn btn-danger btn-lg"  @click="signup">SignUp</button>
      </div>
    </div>
  </template>
  
  <script>
  // @ is an alias to /src
  import { FetchFunction2 } from '../FetchFunc.js'
  
  
  export default {
    name: 'Welcome',
    components: {
      
    },
    methods: {
      login(){
        this.$router.push({ name: 'login'})
      },
      signup(){
        this.$router.push({ name: 'signup'})
      }
    },
    mounted() {
      if (this.$store.state.loggedIn === true){
          this.$router.push({name: 'home'})
      }
    }
  }
</script>

<style>

.home{
  padding-top: 100px;
}
</style>
  