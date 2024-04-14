<template>
    <div class="row">
        <div class="col-2">

        </div>
        <div class="col-sm-8">
            <div class="alert alert-danger text-center" role="alert" v-if="error !== null">
                <h4 class="alert-heading">{{ error }}</h4>
            </div>
            <div class="form-group">
                <label >Name</label>
                <input id="name" class="form-control" type="text" placeholder="Enter the name" v-model="list.name" 
                    :class="{ 'is-invalid': isSubmitted && $v.list.name.$error }" />
                    <div v-if="isSubmitted && !$v.list.name.required" class="invalid-feedback">Name field is required</div>
            </div>
            
            <div class="form-group">
                <label >Description</label>
                <textarea row="4" id="name" class="form-control" type="text" placeholder="Enter the Description" v-model="list.description"  
                    :class="{ 'is-invalid': isSubmitted && $v.list.description.$error }" ></textarea>
                    <div v-if="isSubmitted && !$v.list.description.required" class="invalid-feedback">Description is required</div>
            </div>
        
        

            <button class="btn btn-primary btn-block" @click="createList">Create List</button>

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
import { required } from 'vuelidate/lib/validators'


export default {
    name: 'CreateList',
    data() {
        return {
            list : {
                name: null,
                description: null
            },
            error: null,
            isSubmitted: false
            

        }
    },
    validations: {
            list: {
               name: {required},
               description: {required},

            }
        },
    methods:  {
        
        async createList() {
            this.isSubmitted = true;
            this.$v.$touch();
            if (this.$v.$invalid) {
                return;
            }

            await FetchFunction2({ 
    
                options: {
                    method: 'post',
                    url: `${ApiUrl}/lists`,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    data : this.list 
                },
                authRequired: true
            }).then((response) => {
                console.log(response)
                this.$router.push({name: 'home'})
            }).catch((err) => {
                this.error = err.response.data.message
                console.log(err.response.data.message)
            })
            
        }
    },
    components: {

    },
    async mounted () {
        if (this.$store.state.loggedIn === false){
                this.$router.push({name: 'login'})
        }
    }
}

</script>