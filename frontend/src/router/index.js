import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Signup from '../views/Signup.vue'
import Welcome from '../views/Welcome.vue'
import Home from '../views/Home.vue'
import CreateList from '../views/CreateList.vue'
import CreateCard from '../views/CreateCard.vue'
import UpdateList from '../views/UpdateList.vue'
import Cards from '../views/Cards.vue'
import UpdateCard from '../views/UpdateCard.vue'


Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'welcome', component: Welcome },
  { path: '/login', name: 'login', component: Login},
  { path: '/signup', name: 'signup', component: Signup},
  { path: '/home', name: 'home', component: Home},
  { path: '/cards/:list_id', name: 'cards', component: Cards },
  { path: '/create_list', name: 'createList', component: CreateList },
  { path: '/update_list/:list_id', name: 'updateList', component: UpdateList },
  { path: '/create_card/:list_id', name: 'createCard', component: CreateCard},
  { path: '/update_card/:list_id/:card_id', name: 'updateCard', component: UpdateCard},

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router