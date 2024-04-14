<template>
    <div class="col-sm-3 card">
        <h4>{{this.data.title}}</h4> 
        <span>{{ this.data.content }}</span>
        <button class="mb-2 btn btn-warning" @click="updateCard" >update </button>
    </div>
</template>

<script>
export default {
    name: 'CardComponent',
    props: ['data'],
    methods: {
        updateCard() {
            this.$router.push({ name: 'updateCard' , params: { list_name: this.data.list, card_id: this.data.id  } })
        }
    }
}
</script>

<style>
.card{
    border: 1px solid black;
    border-radius: 5px;

    margin: 10px;
}
</style>