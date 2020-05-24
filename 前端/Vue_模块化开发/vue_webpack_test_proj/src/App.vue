<template>
    <div id='app'>
        <div id='myDiv'>
            {{ message }}
        </div>

        <!-- 使用 Header 组件 -->
        <Header/>
        <!-- 使用 Footer 组件 -->
        <Footer/>

        <calendar/>

    </div>
</template>

<script>
//导入 CSS 文件, 只需导入即生效
import CSS from './css/test.css'

//导入子组件
import Header from './components/Header'
import Footer from './components/Footer'

// vue-calendar
import VueCalendar from './components/Calendar'

//导出组件信息
export default {
    name: 'App',
    data(){
        return {
            message: 'Hello Vue webpack! In App.vue',
        }
    },
    //注册子组件
    components: {
        Header,
        Footer,
        VueCalendar
    },
}
</script>

<style scoped>
#myDiv{
    background-color: #ccc;
}
</style>
