<template>
  <div id="app">
    <h1>App.vue</h1>
    <hr />

    <h3>HelloAxios组件内容:</h3>
    <hello-axios />

  </div>
</template>

<script>
import HelloAxios from "./components/HelloAxios";

export default {
  name: 'App',
  components: {
    HelloAxios
  }
}
</script>
