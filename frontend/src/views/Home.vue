<template>
    <div>
        <div v-if="user_id !== null">
            <div class="row">
                <div class="col-3">

                </div>

                <div class="col-sm-6">
                    <h3>Hello {{ username }}</h3>
                    <div v-if="listArray.length === 0">
                        <h1>There is no Lists</h1>
                        <div class="mt-3">
                            <button class="btn btn-primary" @click="createList">Add List</button>
                        </div>
                    </div>
                    <div v-else>

                        
                        <div class="row">
                            <table class="table">
                                <thead>
                                <tr>
                                    <th >Lists</th>
                                    <th >Add Tasks</th>
                                    <th>Last Updated</th>
                                    <th class="text-center" colspan="2">Actions</th>
                                    
                                </tr>
                            </thead>
                            
                            <tbody>
                                <list v-for="item in listArray" :data="item" />
                            </tbody>

                            </table>
                            
                            
                            
                        </div>    
                        
                        <div class="actions">
                            <button class="btn btn-primary" @click="createList">Add List</button>
                            <button class="ml-3 btn btn-danger" @click="exportData">Export PDF</button>
                            <button class="ml-3 btn btn-warning" @click="exportCsvList">Export List</button>
                        </div>
                        
            
                    </div>
                    
                    
                </div>

                <div class="col-6">

                </div>
            </div>
            
        </div>
        <div v-else>
            <wait />
        </div>
        
    </div>
</template>

<script>
import { FetchFunction, FetchFunction2 } from '@/FetchFunc';
import ApiUrl from '@/config';
import ListTracker from '../components/List.vue'
import WaitComponent from '../components/Wait.vue'
import axios from 'axios'

    export default {
        name: 'Home',
        components: {
            list: ListTracker,
            wait: WaitComponent
        },
        data(){
            return {
                listArray : null,
                user_id : null,
                username: null
            }
        },
        methods: {

           exportData() {
            axios.get(`${ApiUrl}/${this.user_id}/export`, { responseType: 'blob' })
            .then(response => {
                // Check the Content-Type header to make sure it's a PDF file
                if (response.headers['content-type'] === 'application/pdf') {
                // Use the Blob constructor to create a new Blob from the response data
                const pdfBlob = new Blob([response.data], { type: 'application/pdf' })

                // Create an object URL for the PDF file
                const url = URL.createObjectURL(pdfBlob)

                // Create an anchor element
                const link = document.createElement('a')

                // Set the href and download attributes
                link.href = url
                link.download = 'report.pdf'

                // Append the link to the DOM
                document.body.appendChild(link)

                // Click the link to download the PDF
                link.click()

                // Remove the link from the DOM
                document.body.removeChild(link)

                // Revoke the object URL
                URL.revokeObjectURL(url)
                } else {
                console.error('Error: Not a PDF file')
                }
            })
            .catch(error => {
                console.error(error)
            })
           },

           createList(){
                this.$router.push({ name: 'createList' })
           },

           exportCsvList(){
            axios.get(`${ApiUrl}/${this.user_id}/listcsv`, { responseType : 'blob'})
            .then((response) => {

                
                if (response.headers['content-type'] === 'text/csv') {
                
                const csvBlob = new Blob([response.data], { type: 'text/csv' })

                const url = URL.createObjectURL(csvBlob)

                
                const link = document.createElement('a')

                
                link.href = url
                link.download = 'list.csv'

                
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

        async mounted(){
            console.log(this.$store.state.loggedIn)
            if (this.$store.state.loggedIn === false){
                this.$router.push({name: 'login'})
            }

            FetchFunction2({
                options: {
                    url : `${ApiUrl}/users`,
                },
                authRequired : true
            }).then((resp) => {
                
                this.user_id = resp.id
                this.username = resp.username

            })
            .catch((err) => console.log(err))


            await FetchFunction2({
                options: {
                    url : `${ApiUrl}/lists`,
                },
                authRequired : true
            }).then((data) => {
            
                this.listArray = data

            }).catch((err) => console.log(err.response.data.message))
        }
    }
</script>

<style>
.actions{
    margin-top: 20px;
}
</style>