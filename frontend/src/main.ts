import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createHead } from '@unhead/vue/client'
import { router } from './router'
import App from './App.vue'
import 'video.js/dist/video-js.css'
import './assets/main.css'

const app = createApp(App)
const pinia = createPinia()
const head = createHead()

app.use(pinia)
app.use(router)
app.use(head)

app.mount('#app')
