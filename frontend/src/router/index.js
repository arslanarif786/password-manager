// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    component: () => import('@/layouts/default/Default.vue'),
    children: [
      {
        path: '',
        name: 'HomePage',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "home" */ '@/views/HomePage.vue'),
      },
      {
        path: 'login',
        name: 'LoginPage',
        component: () => import(/* webpackChunkName: "home" */ '@/views/LoginPage.vue'),
      },
      {
        path: 'signup',
        name: 'SignupPage',
        component: () => import(/* webpackChunkName: "home" */ '@/views/SignupPage.vue'),
      },
      {
        path: 'dashboard',
        name: 'DashboardPage',
        component: () => import(/* webpackChunkName: "home" */ '@/views/DashboardPage.vue'),
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
