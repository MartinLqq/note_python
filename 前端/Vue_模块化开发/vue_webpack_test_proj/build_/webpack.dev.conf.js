const baseWebpackConfig = require('./webpack.base.conf')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')
const merge = require('webpack-merge')


module.exports = merge(baseWebpackConfig, {
    plugins: [
      new UglifyJsPlugin(),
    ]
})
