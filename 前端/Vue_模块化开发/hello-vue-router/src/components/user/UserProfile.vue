<template>
  <div>
    <div class="profile">
      Hello User Profile!
      <p>user id: {{ $route.params.user_id }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserProfile'
}
</script>

<style scoped>
.profile{
  background-color: lightblue;
}
</style>
