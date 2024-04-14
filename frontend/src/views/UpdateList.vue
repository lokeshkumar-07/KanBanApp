<template>
    <div class="row">
        <div class="col-2">

        </div>
        <div class="col-8">
            <div class="alert alert-danger text-center" role="alert" v-if="errors !== null">
                    <h4 class="alert-heading">{{ error }}</h4>
            </div>
            <div class="form-group">
                <label >Name</label>
                <input id="name" class="form-control" type="text" placeholder="Enter the name" v-model="data.name" />
            </div>
            
            <div class="form-group">
                <label >Description</label>
                <textarea row="4" id="name" class="form-control" type="text" placeholder="Enter the Description" v-model="data.description"  /> 
            </div>
        
        

            <button class="btn btn-primary" @click="updateList">Update List</button>
            <button class="m-5 btn btn-danger" @click="deleteList">Delete List</button>
            <div class="border-top pt-3">
                <small class="text-muted">
                    Go to<router-link :to="{ name: 'home' } " > Home</router-link>
                </small>
            </div>
        </div>

        <div class="col-2">

        </div>
    </div>
</template>

<script>
import ApiUrl from '@/config';
import { FetchFunction, FetchFunction2 } from '@/FetchFunc';
import store from '../store/index.js'

    export default {
        name: 'UpdateList',
        data() {
            return {
                data: {
                    name: null,
                    description: null
                },
                list_id: this.$route.params.list_id,
                errors: null
            }
        },
        methods: {
            async updateList() {

                

                await FetchFunction2({
                    options: {
                        url: `${ApiUrl}/lists/${this.$route.params.list_id}`,
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'PUT',
                        data: this.data
                    },
                    authRequired: true
                }).then((data) => {
                    alert('List Updated')
                }).catch(err => {
                    this.errors = err.response.data.message
                }) 
            },

            deleteList(){
                FetchFunction({
                    url: `${ApiUrl}/lists/${this.$route.params.list_id}`,
                    init_obj: {
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'DELETE'
                    },
                    authRequired: true
                }).then(() => {
                    alert('list Deleted')
                    this.$router.push({ name: 'home' })
                }).catch((err) => {
                    console.log(err.message)
                })
            }
        },
        async mounted() {

            if (store.state.loggedIn === false){
                this.$router.push({name: 'login'})
            }

           await FetchFunction2({
            options: {
                url: `${ApiUrl}/lists/${this.$route.params.list_id}`,
            }
            ,
            authRequired: true
           }).then((data) => {
                this.data.name = data.name,
                this.data.description = data.description
           }).catch(err => {
                console.log(err.response.data.message)
           })
        }
    }
</script>