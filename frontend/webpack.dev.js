const { merge } = require('webpack-merge');
const common = require('./webpack.common');


module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        static: 'app/static/dist'
    },
    module: {
        rules: [
            {
                test: /\.scss$/i,
                use: [
                    'style-loader',
                    'css-loader',
                    'postcss-loader',
                    'sass-loader'
                ]
            }
        ]
    },   
    devServer: {
        hot: true
    } 
    // output: {
    //     publicPath: path.resolve(__dirname, '..', 'static', 'dist')
    // }
});