<template>
    <div>
        <h1>我是App的子组件: HelloVuex 组件</h1>
        <h4>props / count: {{ count }}</h4>
        <h4>vuex / count: {{ $store.state.count }}</h4>
        <h4>vuex / PrettyCount: {{ $store.getters.prettyCount }}</h4>
        <p>{{ $store.getters.otherGetter('hello ', 'getters!') }}</p>

        <button @click="vuexAdd">vuex加1</button>
        <button @click="vuexSub">vuex减1</button>
        <button @click="addCount(10)">vuex +10</button>
    </div>
</template>

<script>
    export default {
        name: "HelloVuex",
        props: {
            count: Number
        },
        methods: {
            vuexAdd () {
                // 不要直接用这种方式, 因为 Devtools 检测不到更新
                // this.$store.state.count++

                // 提交给 Mutations 中的 increment 方法来更新
                this.$store.commit('increment')
            },
            vuexSub () {
                this.$store.commit('decrement')
            },
            addCount (num) {
                // this.$store.commit('incrementCount', {num: num})  // mutations 传参
                this.$store.commit({
                    type: 'incrementCount',
                    num,
                })
            }
        }
    }
</script>

<style scoped>
    h1 {
       color: lightseagreen;
    }
</style>
