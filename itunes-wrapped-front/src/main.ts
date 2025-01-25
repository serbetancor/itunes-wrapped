import './index.css'

import { type Component, createApp } from 'vue'
import { createAppRouter } from './router'
import App from './App.vue'

const app = createApp(App as Component)

app.use(createAppRouter())
app.mount('#app')
