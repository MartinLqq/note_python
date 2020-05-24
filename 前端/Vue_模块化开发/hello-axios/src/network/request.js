
/*

    封装 axios 请求, 推荐使用第五种方式

*/

import axios from 'axios'

// 第一种封装: 传三个参数
export function request1 (config, success, fail) {
    const instance = axios.create({
        baseURL: 'http://123.207.32.32:8000',
        timeout: 5000,
    })
    instance(config)
        .then(resp => {
            // 执行回调函数
            success(resp)
        })
        .catch(error => {
            fail(error)
        })
}

// 第二种封装: 传一个参数
export function request2 (config) {
    const instance = axios.create({
        baseURL: 'http://123.207.32.32:8000',
        timeout: 5000,
    })
    instance(config.baseConfig)
        .then(resp => {
            // 执行回调函数
            config.success(resp)
        })
        .catch(error => {
            config.fail(error)
        })
}

// 第三种封装: 返回 Promise 对像
export function request3 (config) {

    return new Promise((resolve, reject) => {
        const instance = axios.create({
            baseURL: 'http://123.207.32.32:8000',
            timeout: 5000,
        })
        instance(config)
            .then(res => {
                // 执行回调函数
                resolve(res)
            })
            .catch(err => {
                reject(err)
            })
    })
}

// 第四种封装:  直接返回 axios 实例调用结果 (就是一个Promise对象)
// 第三种封装显得多此一举
export function request4 (config) {
    const instance = axios.create({
        baseURL: 'http://123.207.32.32:8000',
        timeout: 5000,
    })
    return instance(config)
}

// 第五种封装, 使用拦截器
// 第四种封装:  直接返回 axios 实例调用结果 (就是一个Promise对象)
// 第三种封装显得多此一举
export function request (config) {
    const instance = axios.create({
        baseURL: 'http://123.207.32.32:8000',
        timeout: 5000,
    })

    // 添加请求拦截器
    instance.interceptors.request.use(config => {
        /*
             a. 修改请求头
             b. 显示正在请求的提示界面(动画) (show)
             c. 根据url进行权限检查, 检查不通过时跳转页面
         */
        console.log(config)
        //返回 config
        return config
    }, err => {
        alert(err)
    });
    // 添加响应拦截器
    instance.interceptors.response.use(res => {
        console.log(res)
        //一般返回 res.data
        return res.data
    }, err => {
        alert(err)
    })

    return instance(config)
}
