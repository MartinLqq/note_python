<template>
    <tab-bar>
        <tab-bar-item path="/home" activeColor="blue">
            <!-- 如果要在标签src属性中使用路径别名, 必须在前面加一个 ~ -->
            <img slot="item-icon" src="~assets/img/tabbar/home.svg" alt="">
            <img slot="item-icon-active" src="~assets/img/tabbar/home-active.svg" alt="">
            <div slot="item-text">首页</div>
        </tab-bar-item>
        <tab-bar-item path="/category" activeColor="green">
            <img slot="item-icon" src="~assets/img/tabbar/categories.svg" alt="">
            <img slot="item-icon-active" src="~assets/img/tabbar/categories-active.svg" alt="">
            <div slot="item-text">分类</div>
        </tab-bar-item>
        <tab-bar-item path="/cart">
            <img slot="item-icon" src="~assets/img/tabbar/cart.svg" alt="">
            <img slot="item-icon-active" src="~assets/img/tabbar/cart-active.svg" alt="">
            <div slot="item-text">购物车</div>
        </tab-bar-item>
        <tab-bar-item path="/profile">
            <img slot="item-icon" src="~assets/img/tabbar/profile.svg" alt="">
            <img slot="item-icon-active" src="~assets/img/tabbar/profile-active.svg" alt="">
            <div slot="item-text">我的</div>
        </tab-bar-item>
    </tab-bar>
</template>

<script>
    import TabBar from "components/tabbar/TabBar";
    import TabBarItem from "components/tabbar/TabBarItem";

    export default {
        name: "MainTabBar",
        components: {
            TabBar,
            TabBarItem
        }
    }
</script>
