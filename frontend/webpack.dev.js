const { merge } = require('webpack-merge');
const common = require('./webpack.common');


module.exports = merge(common, {
    mode: 'development',
    devtool: 'inline-source-map',
    devServer: {
        static: './dist'
    },
    module: {
        rules: [
            {
                test: /\.scss$/i,
                use: [
                    'css-loader',
                    'postcss-loader',
                    'sass-loader'
                ]
            }
        ]
    },     
});