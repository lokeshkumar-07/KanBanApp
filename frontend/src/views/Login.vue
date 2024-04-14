<template>
    <div class="row">

        <div class="col-lg-3">

        </div>

        <div class="col-lg-6 col-sm-12">
            <div>
                <div class="alert alert-danger text-center" role="alert" v-if="error !== null">
                    <h4 class="alert-heading">{{ error }}</h4>
                </div>

                <div class="alert alert-success text-center" role="alert">
                    <h4 >SignIn Form</h4>
                </div>

                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" v-model="loginData.email" id="email" name="email" class="form-control" />
                </div>

                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" v-model="loginData.password" id="password" name="password" class="form-control" />
                </div>
    

                <div class="form-group text-center">
                    <button class="btn btn-block btn-danger" @click="loginUser(loginData)">SignIn</button>
                </div>

                <div class="border-top pt-3">
                    <small class="text-muted">
                        Need a Accouont? <router-link :to="{ name: 'signup' } " >SignUp</router-link>
                    </small>
                </div>
                
            </div>
        </div>

        <div class="col-lg-3">
        </div>

        
    </div>
    
</template>

<script>
    import Vuex from 'vuex'
    import { required, email } from 'vuelidate/lib/validators'
    import { FetchFunction, FetchFunction2 } from '@/FetchFunc'
    import router from '@/router'

    export default {
        name: 'Login',
        data(){
            return {
                loginData: {
                    email: null,
                    password: null
                },
                error: null
            }
        },

        validations: {
            loginData: {
               email: {required,email},
               password: required 
            }
        },

        methods: {

            loginUser(){

                FetchFunction2({
                    options: {
                        url: `http://127.0.0.1:5000/login?include_auth_token`,
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json;charset=UTF-8'
                        },
                        data: {
                            email: this.loginData.email,
                            password: this.loginData.password
                        }
                    }
                }).then((resp) => {
                    console.log(resp)
                    const authToken = resp.response.user.authentication_token
                    console.log(authToken)
                    localStorage.setItem('token', authToken)
                    this.$store.state.loggedIn = true
                    router.push({name: 'home'})
                    alert("login successfull")
                }).catch((err) => {
                    if(err.response.data.response.errors['email']){
                        this.error = err.response.data.response.errors['email'][0]
                    }
                    if(err.response.data.response.errors['password']){
                        this.error = err.response.data.response.errors['password'][0]
                    }
                })

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

</style>