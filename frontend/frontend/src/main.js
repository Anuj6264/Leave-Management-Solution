import Vue from 'vue';
import App from './App.vue';
import router from './router/index.js';
import axios from 'axios';

// axios.defaults.baseURL = 'http://localhost:5000';

Vue.prototype.$http = axios;

new Vue({    
    router,
    render: h => h(App),
  }).$mount('#app')

