import './index.css'

import { type Component, createApp } from 'vue'

import App from './App.vue'
import { createAppRouter } from './router'

const app = createApp(App as Component)

app.use(createAppRouter())
app.mount('#app')
