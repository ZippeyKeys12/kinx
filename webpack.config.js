const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');

module.exports = {
    mode: process.env.production ? 'production' : 'development',
    entry: './src/client/main.ts',
    output: {
        path: path.resolve(__dirname, 'dist'),
        filename: 'bundle.js'
    },
    module: {
        rules: [{
            test: /\.vue$/,
            loader: 'vue-loader'
        }, {
            test: /\.js$/,
            loader: 'babel-loader',
            exclude: /node_modules/
        }, {
            test: /\.(ts|tsx)?$/,
            loader: 'ts-loader',
            exclude: /node_modules/,
            options: {
                appendTsSuffixTo: [
                    /\.vue$/
                ]
            }
        }, {
            test: /\.css$/,
            use: [
                'vue-style-loader',
                'css-loader'
            ],
            exclude: /\.module\.css$/
        }, {
            test: /\.scss$/,
            use: [
                'vue-style-loader',
                'css-loader',
                'sass-loader'
            ]
        }, {
            test: /\.x?html$/,
            loader: 'html-loader'
        }]
    },
    resolve: {
        modules: ['node_modules'],
        extensions: [
            '.js',
            '.vue',
            '.tsx',
            '.ts'
        ]
    },
    // externals: ['vue'],
    devServer: {
        contentBase: path.join(__dirname, 'dist'),
        compress: true,
        hot: true,
        https: true,
        port: 9000
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: 'index.html',
            template: 'src/client/index.html',
            inject: true,
            minify: {
                removeComments: true,
                removeScriptTypeAttributes: true,
                removeAttributeQuotes: true,
                useShortDoctype: true,
                decodeEntities: true,
                collapseWhitespace: true,
                minifyCSS: true
            }
        }),
        new VueLoaderPlugin(),
        new VuetifyLoaderPlugin()
    ]
};