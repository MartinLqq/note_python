<template>
  <div id="app">
    <h1>我是 App 组件</h1>
    <h4>props / count: {{ count }}</h4>
    <h4>vuex / count: {{ $store.state.count }}</h4>
    <button @click="count++">加1</button>
    <button @click="count--">减1</button>

    <hr />
    <hello-vuex :count="count" />

    <hr />
    <hello />

  </div>
</template>

<style>
</style>
<script>
  import HelloVuex from "./components/HelloVuex";
  import Hello from "./components/Hello";

  export default {
    name: 'App',
    data () {
      return {
        count: 0
      }
    },
    components: {
      HelloVuex,
      Hello
    }
  }
</script>
