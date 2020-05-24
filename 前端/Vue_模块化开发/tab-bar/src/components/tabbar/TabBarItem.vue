<template>
    <div class="tab-bar-item" @click="itemClick">
        <slot v-if="!isActive" name="item-icon"></slot>
        <slot v-else name="item-icon-active"></slot>

        <!-- 上面的v-if是在当前作用域执行, 所以可以放在slot中 (不过推荐放在一个div内),
             但是, 下面的 :class 需要写在外层的一个div中, 放在slot中无效 -->
        <!-- <div :class="{active: isActive}"> -->
        <div :style="isActive ? activeStyle : {}">
            <slot name="item-text"></slot>
        </div>
    </div>
</template>

<script>
    export default {
        name: "TabBarItem",
        props: {
            path: String,
            activeColor: {
                type: String,
                default: 'red'
            }
        },
        data () {
            return {
                // isActive: true  // 换成计算属性
                activeStyle: {
                    color: this.activeColor
                }
            }
        },
        computed: {
            isActive () {
                console.log(this.$route.path)
                // return this.$route.path.indexOf(this.path) !== -1
                return this.$route.path === this.path
            }
        },
        methods: {
            // 定义 tab-bar-item 点击事件
            itemClick () {
                console.log('itemClick', this.path)
                // this.$router.replace(this.path)
                // 解决连续单击时的错误提示
                if (this.$route.path !== this.path) {
                    this.$router.replace(this.path)
                }
            }
        }
    }
</script>

<style scoped>
    .tab-bar-item {
        flex: 1;  /* 对flex元素位置均等分 */
        text-align: center;
        height: 49px;  /* 移动端 TabBar 的高度一般是49px */
        font-size: 14px;
    }
    .tab-bar-item img {
        width: 24px;
        height: 24px;
        margin-top: 3px;
        /*margin-bottom: 3px;*/
        vertical-align: middle;
    }

    /*.active {*/
    /*    color: red;*/
    /*}*/
</style>
