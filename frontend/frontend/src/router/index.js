import Vue from 'vue';
import VueRouter from 'vue-router';

import Home from '../components/Home.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import ApplyLeave from '../components/ApplyLeave.vue';
import ViewLeaves from '../components/ViewLeaves.vue';
import ManageLeaves from '../components/ManageLeaves.vue';

Vue.use(VueRouter);

 const routes = [
    { 
      path: '/', 
      name: "home",
      component: Home 
    },
    { 
      path: '/login', 
      name: "login",
      component: Login 
    },
    { 
      path: '/register', 
      name: "register",
      component: Register 
    },
    { 
      path: '/apply-leave', 
      name: "apply-leave",
      component: ApplyLeave 
    },
    { 
      path: '/view-leaves', 
      name: "view-leaves",
      component: ViewLeaves 
    },
    { 
      path: '/manage-leaves', 
      name: "manage-leaves",
      component: ManageLeaves,
      meta: { requiresManager: true }
    },
  ];

  const router = new VueRouter({
    mode: 'history',
    routes
  })

  router.beforeEach((to, from, next) => {
    const userRole = localStorage.user_role; 
    if (to.meta.requiresManager && userRole !== 'Manager') {
      alert("Access Denied")
      next('/');
    } else {
      next(); 
    }
  });
  
  export default router;
