const baseWebpackConfig = require('./webpack.base.conf')
const merge = require('webpack-merge')


module.exports = merge(baseWebpackConfig, {
    devServer: {
      contentBase: './dist',  //本地开发服务器服务于dist/路径
      inline: true   //代码改动时实时更新服务
      // port:        //端口号
      // historyApiFallback:    //在SPA页面中, 依赖HTML5的history模式
    }
})
