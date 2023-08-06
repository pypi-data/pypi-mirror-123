const path = require('path');

module.exports = {
  entry: {
    'admin-form': './wagtail_maps/static_src/admin-form.js',
  },
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'wagtail_maps/static/wagtail_maps/js'),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        use: { loader: 'babel-loader' },
      },
    ],
  },
  devtool: 'source-map',
  stats: {
    chunks: false,
    hash: false,
    colors: true,
    reasons: false,
    version: false,
  },
};
