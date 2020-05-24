<template>
  <div>
    <h3>这是 Test 组件</h3>
    <p>Hello {{ userId }}</p>
    <!-- <h3>{{ $route.params.user_id }}</h3>-->

    <!--  嵌套路由  -->
    <router-link :to="'/test/' + userId + '/profile'" tag="button">嵌套路由 User Profile</router-link>&nbsp;
    <router-link :to="'/test/' + userId + '/collections'" tag="button">嵌套路由 User Collections</router-link>
    <hr />

<!--    <transition>-->
      <router-view></router-view>
<!--    </transition>-->

  </div>
</template>

<script>
export default {
  name: 'Test',
  computed: {
    userId () {
      console.log('====>', this.$route.params)
      return this.$route.params.user_id
    }
  }
}
</script>

<style scoped>
</style>
