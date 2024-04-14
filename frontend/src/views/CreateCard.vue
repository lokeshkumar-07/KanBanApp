<template>
    <div>
        <div class="row">
            <div class="col-2">

            </div>

            <div class="col-8">
                <div class="alert alert-danger text-center" role="alert" v-if="errors !== null">
                    <h4 class="alert-heading">{{ error }}</h4>
                </div>
                <div class="form-group">
                    <label >Title </label>
                    <input id="title" class="form-control" type="text" placeholder="Title" v-model="card.title" 
                        :class="{ 'is-invalid': isSubmitted && $v.card.title.$error }" />
                    <div v-if="isSubmitted && !$v.card.title.required" class="invalid-feedback">Title is required</div>
                </div>
                <div class="form-group">
                    <label >Content </label>
                    <textarea rows="3" id="content" class="form-control" type="text" placeholder="Enter the name" v-model="card.content" 
                        :class="{ 'is-invalid': isSubmitted && $v.card.content.$error }" ></textarea>
                    <div v-if="isSubmitted && !$v.card.content.required" class="invalid-feedback">Content is required</div>
                </div>
               
                
                <div class="form-group"  >
                    <label for="example-datepicker">Deadline</label>
                    <b-form-datepicker id="example-datepicker" v-model="card.deadline" class="mb-2"
                        :class="{ 'is-invalid': isSubmitted && $v.card.deadline.$error }" ></b-form-datepicker>
                    <div v-if="isSubmitted && !$v.card.deadline.required" class="invalid-feedback">Deadline is required</div>
                </div>
                
                
                

                
                <div class="form-check form-check-inline">
                    <label for="not_complected" >Not Complected </label>
                    <input type="radio" class="form-check-input" name="mark" id="not_complected" value="Not Complected" v-model="card.mark" /> 
                    <label for="complected" >Complected </label>
                    <input type="radio" class="form-check-input" name="mark" id="complected" value="Complected" v-model="card.mark" /> 
                </div>    
                
                <div class="row">
                    <label class="col-2" >Select the list </label>
                    <select class="col-10 browser-default custom-select" required v-model="card.list_id">
                        <option id="select" v-for="item in list_data" :value="item.id" >{{item.name}}</option>
                    </select>
                </div>
                

                <br />

                <button class="btn btn-success" @click="createCard">Create Card</button>

                <div class="border-top pt-3">
                    <small class="text-muted">
                        Go to<router-link :to="{ name: 'home' } " > Home</router-link>
                    </small>
                </div>
            </div>

            <div class="col-2">

            </div>
        </div>
       
    </div>
</template>

<script>
import ApiUrl from '@/config';
import { FetchFunction2, FetchFunction } from '../FetchFunc.js';
import store from '../store/index.js'
import { required } from 'vuelidate/lib/validators'

export default {
    name: 'CreateList',
    data() {
        return {
            card : {
                title: null,
                content: null,
                deadline: null,
                list_id: null,
                complete_date: "null",
                mark: "Not Complected"
            },
            isSubmitted : false,
            list_data : [],
            errors: null
        }
    },
    validations: {
        card: {
            title : {required},
            content: {required},
            deadline: {
                required,
            },
            
        }
            
    },
    methods: {
        async createCard(){


            this.isSubmitted = true;
            this.$v.$touch();
            if (this.$v.$invalid) {
                return;
            }

            function formatDate(oDate) {
                
                let sMonth = '' + (oDate.getMonth() + 1);
                let sDay = '' + oDate.getDate();
                let iYear = oDate.getFullYear();

                if (sMonth.length < 2) { sMonth = '0' + sMonth; }
                if (sDay.length < 2) { sDay = '0' + sDay; }

                return [iYear, sMonth, sDay].join('-');
            }

            if(this.card.mark === "Complected"){
                const date = new Date()
            
                this.card.complete_date = formatDate(date)
            }

            await FetchFunction2({
               
                options: {
                    method: 'post',
                    url: `${ApiUrl}/cards/${this.$route.params.list_id}`,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'POST',
                    data : this.card
                },
                authRequired: true
            }).then((data) => {
                alert('Card Created')
                this.$router.push({ name: 'cards', params: {list_id: this.$route.params.list_id} })
            }).catch((err) => {
                console.log(err)
            })
        }
    },
    async mounted () {
        if (store.state.loggedIn === false){
                this.$router.push({name: 'login'})
        }
        FetchFunction2({ 
            options: {
                url: `${ApiUrl}/lists`,
            },
            authRequired: true
        })
        .then((data) =>{
            console.log(data)
            this.list_data = data

        })
        .catch(err => {
            this.errors = err.response.data.message
        })
    }
}

</script>