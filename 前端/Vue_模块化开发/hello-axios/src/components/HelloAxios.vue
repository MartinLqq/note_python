<template>
    <div>
        axios 请求结果: {{ resp }}
    </div>
</template>

<script>
    import {request1,request2,request3,request4,request} from "../network/request";

    export default {
        name: "HelloAxios",
        data () {
            return {
                resp: ''
            }
        },
        created() {
            // 1. 使用第一种封装
            // reques1t({
            //     url: '/home/multidata'
            // }, resp => {
            //     this.resp = resp
            // }, error => {
            //     alert('请求失败!')
            // })

            // 2. 使用第二种封装
            // request2({
            //     baseConfig: {
            //         url: '/home/multidata'
            //     },
            //     success: resp => {
            //         this.resp = resp
            //     },
            //     fail: error => {
            //         alert(error)
            //     }
            // })

            // // 3. 使用第三种封装
            // request3({
            //     url: '/home/multidata',
            // }).then(res => {
            //     this.resp = res
            // }).catch(err => {
            //     alert(err)
            // })

            // 4. 使用第四种封装
            // 把上面 request3 改成 request4, 用法一样
            // request4({
            //     url: '/home/multidata',
            // }).then(res => {
            //     this.resp = res
            // }).catch(err => {
            //     alert(err)
            // })

            // 5. 使用第五种封装
            request({
                url: '/home/multidata'
            }).then(res => {
                this.resp = res
            }).catch(err => {
                alert(err)
            })
        }
    }
</script>
