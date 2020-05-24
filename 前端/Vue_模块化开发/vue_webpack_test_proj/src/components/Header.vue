<template>
    <div>
        <h3>这是 Header.vue 的内容</h3>
        <div>{{ message }}</div>
    </div>
</template>
<script>
export default {
    name: 'Header',
    data(){
        return {
            message: 'Hello Header',
        }
    },
    template: '<Header/>',
}
</script>
<style scoped>
h3{
    color: blue;
}
</style>
