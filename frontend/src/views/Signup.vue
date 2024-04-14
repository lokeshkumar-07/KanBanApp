<template>
    
    <div class="row">

        <div class="col-lg-3">

        </div>

        <div class="col-lg-6 col-sm-12">

            <div class="alert alert-danger" role="alert" v-if="error !== null">
                <h2 class="alert-heading">{{ error }}</h2>
            </div>


            <div class="container" style="text-align: left">
                <div class="alert alert-success" role="alert">
                    <h2 >SignUp form Validation</h2>
                </div>
                
                    
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" v-model="userForm.email" id="email" name="email" class="form-control"
                        :class="{ 'is-invalid': isSubmitted && $v.userForm.email.$error }" />
                    <div v-if="isSubmitted && $v.userForm.email.$error" class="invalid-feedback">
                        <span v-if="!$v.userForm.email.required">Email field is required</span>
                        <span v-if="!$v.userForm.email.email">Please provide valid email</span>
                    </div>
                </div>
                <div class="form-group">
                    <label for="name">Username</label>
                    <input type="text" v-model="userForm.name" id="name" name="name" class="form-control"
                        :class="{ 'is-invalid': isSubmitted && $v.userForm.name.$error }" />
                    <div v-if="isSubmitted && !$v.userForm.name.required" class="invalid-feedback">Name field is required</div>
                </div>
            
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" v-model="userForm.password" id="password" name="password" class="form-control"
                        :class="{ 'is-invalid': isSubmitted && $v.userForm.password.$error }" />
                    <div v-if="isSubmitted && $v.userForm.password.$error" class="invalid-feedback">
                        <span v-if="!$v.userForm.password.required">Password field is required</span>
                        <span v-if="!$v.userForm.password.minLength">Password should be at least 5 characters long</span>
                    </div>
                </div>
                <div class="form-group">
                    <label for="confirmPassword">Confirm Password</label>
                    <input type="password" v-model="userForm.confirmPassword" id="confirmPassword" name="confirmPassword"
                        class="form-control" :class="{ 'is-invalid': isSubmitted && $v.userForm.confirmPassword.$error }" />
                    <div v-if="isSubmitted && $v.userForm.confirmPassword.$error" class="invalid-feedback">
                        <span v-if="!$v.userForm.confirmPassword.required">Confirm Password field is required</span>
                        <span v-else-if="!$v.userForm.confirmPassword.sameAsPassword">Passwords should be matched</span>
                    </div>
                </div>
            
                <div class="form-group text-center">
                    <button class="btn btn-danger btn-block " @click="handleSubmit">Sign Up</button>
                </div>

                <div class="border-top pt-3">
                    <small class="text-muted">
                        Already Have an Account? <router-link :to="{name:'login'}">Sign In</router-link>
                    </small>
                </div>
                
            </div>

        </div>

        <div class="col-lg-6">

        </div>

        
    </div>

    
</template>

<script>
    import ApiUrl from '@/config';
    import FetchFunction, { FetchFunction2 } from '@/FetchFunc';
    import axios from 'axios'
    import { required, email, minLength, sameAs } from 'vuelidate/lib/validators'

    export default {
        name: 'Signup',
        data(){
            return {
                userForm:{
                    name: null,
                    email: null,
                    password: null
                },
                isSubmitted: false,
                error: null
            }
        },
        validations: {
            userForm: {
                name : {required},
                email: {required, email},
                password: {
                    required,
                    minLength: minLength(5)
                },
                confirmPassword: {
                    required,
                    sameAsPassword: sameAs('password')
                },
            }
            
    },

        methods: {
            async handleSubmit(){

                this.isSubmitted = true;
                this.$v.$touch();
                if (this.$v.$invalid) {
                    return;
                }

                FetchFunction2({
                    options: {
                        method: 'POST',
                        url: `${ApiUrl}/users`,
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json;charset=UTF-8'
                        },
                        data: {
                            email: this.userForm.email,
                            username: this.userForm.name,
                            password: this.userForm.password
                        }
                    }
                }).then((data) => {
                    alert('User created')
                    this.$router.push({ name: 'login'})
                }).catch(err => {
                    this.error = err.response.data.message
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
.btn-vue{
    background: #53b985;
    color: #31485D;
    font-weight: bold;
}
</style>