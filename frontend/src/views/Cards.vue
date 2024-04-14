<template>
    <div class="row">
        <div class="col-sm-2">

        </div>

        <div class="col-sm-8">
            <cardGraph :chartData="data" />
            <h1>All the cards following</h1>
            <div v-if="note == 'not found'">
                <h4>No card found</h4>
                <div>
                    <button class="btn btn-danger" @click="addCard">Add Card</button>
                    
                </div>
            </div>
            <div else>
                <div v-if="status.total1 !== 0">
                    <span class="text-success">{{ status.comp }} /{{ status.total1 }} Tasks Completes</span><br />
                    <span class="text-warning">{{ status.pending }} /{{ status.total1 }} tasks pending</span><br />
                    <span class="text-danger">{{ status.expires }} /{{ status.total1 }} tasks expires</span><br />

                    <div class="mt-3 mb-3">
                        <button class="btn btn-success" @click="exportlistSummery">summery</button>
                        <button class="ml-2 btn btn-danger" @click="addCard">Add Card</button>
                    </div>
                </div>
                <div class="row text-center">
                    <card v-for="item in card_data" :data="item" /> 
                </div>
                <div class="border-top pt-3">
                    <small class="text-muted">
                        Go to<router-link :to="{ name: 'home' } " > Home</router-link>
                    </small>
                </div>
            </div>
           
        </div>

        <div  class="col-sm-2">

        </div>
        
       
    </div>
</template>

<script>
import ApiUrl from '@/config';
import { FetchFunction2 } from '@/FetchFunc';
import axios from 'axios';
import CardComponent from '../components/Card.vue'
import CardGraph from '../components/CardsGraph.vue'
import WaitComponent from '../components/Wait.vue'

export default {
    name: 'Cards',
    data() {
        return {
            card_data: null,
            data: null,
            xlabel : null,
            ylabel : null,
            status : {
                total1: 0,
                pending: 0,
                expires: 0,
                comp: 0
            },
            created_date : null,
            note: null
    }
    },
    components: {
        card: CardComponent,
        cardGraph: CardGraph
    },

    methods: {
        addCard(){
            this.$router.push({ name: 'createCard', params: {list_id: this.$route.params.list_id }})
        },
        exportlistSummery(){
            axios.get(`${ApiUrl}/${this.$route.params.list_id}/cardscsv`, {responseType : 'blob'})
            .then(response => {
                
                if (response.headers['content-type'] === 'text/csv') {
            
                const csvBlob = new Blob([response.data], { type: 'text/csv' })

                const url = URL.createObjectURL(csvBlob)

                
                const link = document.createElement('a')

               
                link.href = url
                link.download = 'cards.csv'

                
                document.body.appendChild(link)

                
                link.click()

                
                document.body.removeChild(link)

                
                URL.revokeObjectURL(url)
                } else {
                console.error('Error: Not a PDF file')
                }
            })
            .catch(err => {
                console.error(err)
            })
        }
    },

    mounted() {

        FetchFunction2({ 
            options: {
                url: `${ApiUrl}/lists/${this.$route.params.list_id}`
            },
            authRequired: true
         }).then((data) => {
            this.created_date = data.created_date
         }).catch((err) => {
            console.log(err.response.data.message)
        })
        
        FetchFunction2({
            options: {
                url: `${ApiUrl}/cards/${this.$route.params.list_id}`,
            },
            authRequired : true
        }).then((data) => {

            
                this.card_data = data
            
            function formatDate(oDate) {
                
                let sMonth = '' + (oDate.getMonth() + 1);
                let sDay = '' + oDate.getDate();
                let iYear = oDate.getFullYear();

                if (sMonth.length < 2) { sMonth = '0' + sMonth; }
                if (sDay.length < 2) { sDay = '0' + sDay; }

                return [iYear, sMonth, sDay].join('-');
            }
            
          
            
            data.forEach((x) => {
                this.status.total1 += 1
                if(x.mark === "Not Complected"){
                    const date = new Date()
                    const newDate = formatDate(date)
                    if (x.deadline < newDate){
                        this.status.expires += 1
                    }else{
                        this.status.pending += 1
                    }
                }else{
                    this.status.comp += 1
                }
            })

        

            var dateArr = {}
            const start = new Date(this.created_date)
            const end = new Date();
        
            let loop = new Date(start);
            while (loop <= end) {
                
                let key = formatDate(loop)
                dateArr[key] = 0
                let newDate = loop.setDate(loop.getDate() + 1);
                loop = new Date(newDate);
            }
            
            
            data.forEach(d => {
                for (let key in d) {
                    
                    if( key == 'complete_date'){
                        if(d[key] != 'null'){
                            dateArr[d[key]] += 1
                        }
                    }
                }
            })

            
            

            this.xlabel = Object.keys(dateArr)
            this.ylabel = Object.values(dateArr) 
            
            this.data = {
                    labels: this.xlabel,
                    datasets: [
                        {
                            label: 'Cards Trendlines',
                            backgroundColor: 'rgba(0, 0, 255, 0.2)',
                            data: this.ylabel
                        }
                ]
            
            }
            
        }).catch(err => {
            this.note = 'not found'
            console.log(err.response.data.message)
        })

        
    }
}

</script>