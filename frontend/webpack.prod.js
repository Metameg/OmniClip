const { merge } = require('webpack-merge');
const common = require('./webpack.common');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

module.exports = merge(common, {
    mode: 'production',
    devServer: {
        static: './dist'
    },
    module: {
        rules: [
            {
                test: /\.scss$/i,
                use: [
                    {
                        loader: MiniCssExtractPlugin.loader,
                        
                    },
                    'css-loader',
                    'postcss-loader',
                    'sass-loader'
                ]
            }
        ]
    },     
    plugins: [
        new MiniCssExtractPlugin({
            filename: '[name].css'
        })
    ],
});