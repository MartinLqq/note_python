import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    count: -100  // 组件中调用: $store.state.count
  },
  mutations: {  // 同步操作交给 mutations. 组件中调用: $store.commit('increment')
    increment (state) {
      state.count++
    },
    decrement (state) {
      state.count--
    },
    incrementCount (state, payload) {  // mutations 接收参数
      console.log(payload)
      state.count += payload.num
    }
  },
  actions: {  // 异步操作交给 actions, 如网络请求、定时器. 组件中调用: 见文挡
  },
  modules: {
  },

  getters: {  // 定义类似 computed属性, 先处理数据, 再返回. 组件中调用: $store.getters.prettyCount
    prettyCount (state, getters) {
      console.log(getters)
      return '**** ' + state.count + ' ****'
    },
    otherGetter (state, getters) {
      return (myParam1, myParam2) => {  // 实现 getters 传参. 动态过滤
        // ...
        return '---test getters with more params---> ' + myParam1 + myParam2 + getters.prettyCount
      }
    }
  }
})

export default store
