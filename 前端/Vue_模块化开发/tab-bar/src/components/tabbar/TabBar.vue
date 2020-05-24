<template>
    <div id="tab-bar">
        <slot></slot>
    </div>
</template>

<script>
    export default {
        name: "TabBar"
    }
</script>

<style scoped>
    #tab-bar {
        display: flex;
        background-color: #f2f2f2;
        /*  位置  */
        position: fixed;
        left: 0;
        right: 0;
        bottom: 0;
        /*  上边框阴影  */
        box-shadow: 0 0 1px 1px rgba(100, 100, 100, .2);
    }
</style>
