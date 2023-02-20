import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'

import Exhibit from './components/Exhibit.vue'
import Select from './components/Select.vue'
import Upload from './components/Upload.vue'
import Videos from './components/Videos.vue'
import Wait from './components/Wait.vue'
import Results from './components/Results.vue'

Vue.use(VueRouter)

Vue.config.productionTip = false

const routes = [
  { path: '/exhibit', component: Exhibit },
  { path: '/exhibit/select', component: Select },
  { path: '/exhibit/select/upload', component: Upload },
  { path: '/exhibit/select/:name', component: Videos },
  { path: '/exhibit/wait/:taskId', component: Wait },
  { path: '/exhibit/results/:taskId', component: Results },
]

const router = new VueRouter({
  routes,
  scrollBehavior () {
    return { x: 0, y: 0 }
  }
})

new Vue({
  render: h => h(App),
  router: router
}).$mount('#app')
