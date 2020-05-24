import Vue from 'vue'
import VueRouter from 'vue-router'

// 注册路由插件
Vue.use(VueRouter)

// 定义路由懒加载函数
const Home = () => import('../views/home/Home')
const Category = () => import('../views/category/Category')
const Cart = () => import('../views/cart/Cart')
const Profile = () => import('../views/profile/Profile')

// 定义路由表
const routes = [
  {
    path: '',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home,
    meta: {title: '首页'}
  },
  {
    path: '/category',
    name: 'Category',
    component: Category,
    meta: {title: '分类'}
  },
  {
    path: '/cart',
    name: 'Cart',
    component: Cart,
    meta: {title: '购物车'}
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {title: '我的'}
  },
]

// 实例化 VueRouter
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})


// 注册一个全局的前置守卫
router.beforeEach((to, from, next) => {
  // console.log(to)
  // console.log(from)
  // document.title = to.meta.title
  document.title = to.matched[0].meta.title
  next()
})

// 导出 router
export default router
