import Vue from 'vue'

// vue-router 使用步骤
// 1.导入 VueRouter
import VueRouter from 'vue-router'

// 注释下面的 import, 使用路由懒加载
// import Home from '../views/Home.vue'
// import Test from '../views/Test.vue'
// import UserProfile from '../components/user/UserProfile.vue'
// import UserCollections from '../components/user/UserCollections.vue'

const Home = () => import('../views/Home.vue')
const About = () => import(/* webpackChunkName: "about" */ '../views/About.vue')
const Test = () => import('../views/Test.vue')
const UserProfile = () => import('../components/user/UserProfile.vue')
const UserCollections = () => import('../components/user/UserCollections.vue')

// 2.安装插件 VueRouter
Vue.use(VueRouter)

// 3.配置路由和组件的映射关系
const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页' }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: About,
    meta: { title: '关于' }
  },
  {
    path: '/test/:user_id',
    name: 'Test',
    component: Test,
    meta: { title: '测试页' },
    children: [
      { path: '', redirect: 'profile' },
      { path: 'profile', component: UserProfile, meta: { title: '用户档案' } },
      { path: 'collections', component: UserCollections, meta: { title: '用户收藏' } }
    ]
  },
  {
    path: '/named-route-test',
    name: 'NamedRouteTest',
    component: () => import('../views/NamedRouteTest'),
    meta: { title: '命名路由测试页' }
  }
]

// 4.实例化 VueRouter, 传入上面的映射关系
const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

// 注册一个全局的前置守卫
router.beforeEach((to, from, next) => {
  console.log(to)
  console.log(from)

  // document.title = to.meta.title
  document.title = to.matched[0].meta.title
  next()
})

// 5.导出 router 对象, 用于 Vue 实例化参数
export default router
