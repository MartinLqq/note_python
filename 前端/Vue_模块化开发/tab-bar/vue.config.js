/*
    这里是一些自定义配置, vue-cli3自动根据此文件名来查找和更新配置
*/

const path = require('path')
const resolve = dir => path.join(__dirname, dir)

module.exports = {
    chainWebpack: config => {

        //vue-cli3 起别名
        config.resolve.alias
            //第一个参数: 别名, 第二个参数: 路径
            .set('components', resolve('src/components'))
            .set('assets', resolve('src/assets'))
            .set('views', resolve('src/views'))
        /* 注:
            1. store, router 没有必要设置别名;
            2. src已默认设置为'@'
        */
    }
}
