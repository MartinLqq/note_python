<template>
  <div>
    <div class="collections">
      Hello User Collections!
      <p>user id: {{ $route.params.user_id }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UserCollections'
}
</script>

<style scoped>
.collections{
  background-color: lightseagreen;
}
</style>
