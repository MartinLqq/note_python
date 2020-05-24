<template>
    <div>
        <h1>我是App的子组件: Hello 组件</h1>
        <h4>vuex / count: {{ $store.state.count }}</h4>
    </div>
</template>

<script>
    export default {
        name: "Hello"
    }
</script>

<style scoped>
    h1 {
        color: lightblue;
    }
</style>
