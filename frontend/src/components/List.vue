<template>
    

    
        <tr>
            <th scope="row">
                <router-link :to="{ name: 'cards' , params : {list_id: this.data.id} } " >{{  data.name  }}</router-link>
            </th>
            <td><button class="btn btn-primary" @click="addCard">Add Cards</button></td>
            <td><span class="text-danger" >{{ data.review }}</span></td>
            <td>
                
                <button class="btn btn-info" @click="editList">Edit</button>
        
            </td>
        
            <td>
                <button class="ml-2 btn btn-success" @click="summery">Summery</button>
            </td>
            
        </tr>
        

    
    
</template>

<script>
import ApiUrl from '@/config';
import { FetchFunction } from '@/FetchFunc';

    export default {
        name: 'ListComponent',
        props : ['data'],
        methods: {
            addCard(){
                this.$router.push({ name: 'createCard', params: { list_id: this.data.id } })
            },
            editList(){
                this.$router.push( { name: 'updateList', params: { list_id: this.data.id }})
            },
            summery(){
                this.$router.push( { name: 'cards' , params : {list_id: this.data.id} } )
            },
        
            deleteList() {
                FetchFunction({
                    url: `${ApiUrl}/lists/${this.data.id}`,
                    init_obj: {
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        method: 'DELETE'
                    },
                    authRequired: true
                }).then(() => {
                    alert('list Deleted')
                    this.$router.push(`http://localhost:8080/home`)
                }).catch((err) => {
                    console.log(err.message)
                })
            }
        }
    }
</script>