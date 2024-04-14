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

                <button class="btn btn-success" @click="updateCard">Update Card</button>
                <button class="ml-3 btn btn-danger" @click="deleteCard">Delete Card</button>

                <div class="border-top pt-3">
                    <small class="text-muted">
                        Go to<router-link :to="{ name: 'cards', params:{list_id: this.$route.params.list_id } } "> Back</router-link>
                    </small>
                </div>

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
import { FetchFunction, FetchFunction2 } from '@/FetchFunc';
import WaitComponent from '../components/Wait.vue'
import store from '../store/index.js'
import { required } from 'vuelidate/lib/validators'

export default {
    name: 'UpdateCard',
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
            card_id: this.$route.params.card_id,
            list_data: [],
            isSubmitted: false,
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
            list_id: { required }
            
        }
            
    },
    components: {
        wait: WaitComponent
    },
    methods: {
        
        updateCard() {

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

            FetchFunction2({
                    
                    options: {
                        url: `${ApiUrl}/cards/${this.$route.params.list_id}/${this.$route.params.card_id}`,
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'PUT',
                        data: this.card
                    },
                    authRequired: true
                }).then((data) => {
                    alert('Card Updated')
                    this.$router.push({ name: 'cards', params:{list_id: this.$route.params.list_id } })
                }).catch((err) => {
                    console.log(err.response.data.message)
            })
        },

        deleteCard(){
            FetchFunction2({
                options: {
                    url: `${ApiUrl}/cards/${this.$route.params.list_id}/${this.$route.params.card_id}`,
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    method: 'delete',
                },
                authRequired: true
            })
            .then((data) => {
                alert('card deleted')
                this.$router.push({name:'cards', params: {list_id: this.$route.params.list_id}})
            })
            .catch(err => {
                console.log(err.response.data.message)
            })
        }
    },

    
    async mounted() {

        if (store.state.loggedIn === false){
                this.$router.push({name: 'login'})
        }

        FetchFunction2({
            options: {
                url: `${ApiUrl}/cards/${this.$route.params.list_id}/${this.$route.params.card_id}`
            }
            ,
            authRequired: true
        } 
        ).then((data) => {
            console.log(data)
            this.card = data
        }).catch(err => {
            console.log(err.message)
        }),

        FetchFunction2({ 
            options: {
                url: `${ApiUrl}/lists`
            }
            ,
            authRequired: true
        })
        .then((data) =>{
            console.log(data)
            this.list_data = data
        })
        .catch(err => {
            console.log(err.response.data.message)
        })
    }
}

</script>