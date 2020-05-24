<template>
    <div>
        <h3>这是 Footer.vue 的内容</h3>
        <div>{{ message }}</div>
    </div>
</template>
<script>
export default {
    name: 'Footer',
    data(){
        return {
            message: 'Hello Footer',
        }
    },
    template: '<Footer/>',
}
</script>
<style scoped>
h3{
    color: green;
}
</style>
