<template>
  <div id="app">

    <router-view />

    <!-- 最后将 <tab-bar> 移到 components/MainTabBar.vue 中
    <tab-bar> ... </tab-bar>
    -->
    <main-tab-bar />

  </div>
</template>

<!--使用 @import 导入css样式文件-->
<style>
  @import "assets/css/base.css";

</style>

<script>
  // import TabBar from "./components/tabbar/TabBar"
  // import TabBarItem from "./components/tabbar/TabBarItem"

  // TabBar实现的最后一步: 将 TabBar, TabBarItem 从 App.vue 中分离, 移到 components/MainTabBar.vue 中
  // 大大缩减 App.vue 中的代码!!
  import MainTabBar from "components/MainTabBar"

  export default {
    name: 'App',
    components: {
      // TabBar,
      // TabBarItem
      MainTabBar
    }
  }
</script>
