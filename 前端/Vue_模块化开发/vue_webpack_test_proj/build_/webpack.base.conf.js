const path = require('path');  //导入webpack自带的path路径处理模块
const webpack = require('webpack');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
    entry: "./src/main.js",  //打包解析的入口js文件
    output: {
        // path: "./dist/",  // 报错! 要求绝对路径
        path: path.resolve(__dirname, '../dist/'),  //最终打包后的所有资源的根目录
        filename: "bundle.js",  //最终打包后的 js 单文件的名称

        //配置所有url地址解析打包后增加 "dist/"
        // publicPath: "dist/",  //删除此项是因为之后配置了 HtmlWebpackPlugin 插件
    },
    module: {
        rules: [
        {
            test: /\.css$/,
            use: [
            { loader: "style-loader" },
            { loader: "css-loader" }
            ]
            // use: ["style-loader", "css-loader"]  //使支持 .css 样式文件的打包和使用
        },
        { test: /\.ts$/, use: 'ts-loader' },
        {
            test: /\.(png|jpg|gif|jpeg)$/,
            use: [
              {
                loader: 'url-loader',  //处理和打包url资源
                options: {
                  limit: 8192,
                  name: "img/[name]_[hash:8].[ext]"  //自定义图片文件的路径,名称
                }
              }
            ]
          },
          {
            test: /\.m?js$/,
            exclude: /(node_modules | bower_components)/,  //过滤这些文件, 不转化
            use: {
              loader: 'babel-loader',
              options: {
                presets: ['es2015']    //将 ES6 语法代码转为 ES5 语法
              }
            }
          },
          {
            test: /\.vue$/,
            use: ['vue-loader']  //使支持 .vue 组件文件
          }
        ]
    },
    resolve: {
        extensions: ['.js', '.vue', '.json'],  //导入资源时省略后缀
        alias: {
            'vue$': 'vue/dist/vue.esm.js',  //导入vue时使用包含compiler的vue版本
        }
    },
    plugins: [
      new webpack.BannerPlugin('最终版权归 Martin 所有\n\n\n'),  //注册版本声明插件
      new HtmlWebpackPlugin({   //注册打包 HTML 文件的插件
        template: 'index.html'  //不用默认的模板, 用自己的index.html, 因为默认模板中没有`<div id='app'><div>`
      }),
    ],
}
