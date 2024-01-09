//webpack.config.js
const path = require('path');
const {merge} = require('webpack-merge');

const defaultConfig = {
  resolve: {
    extensions: ['.ts', '.tsx', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        loader: 'ts-loader',
      },
    ],
  },
};

const baseConfig = {
  entry: {
    main: './src/base.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/base.js', // <--- Will be compiled to this single file
  },
};

const userConfig = {
  entry: {
    main: './src/user.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/user.js', // <--- Will be compiled to this single file
  },
};

const homeConfig = {
  entry: {
    main: './src/home.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/home.js', // <--- Will be compiled to this single file
  },
};

const eventConfig = {
  entry: {
    main: './src/event.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/event.js', // <--- Will be compiled to this single file
  },
};

const chatConfig = {
  entry: {
    main: './src/chat.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/chat.js', // <--- Will be compiled to this single file
  },
};

const adminConfig = {
  entry: {
    main: './src/admin.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/admin.js', // <--- Will be compiled to this single file
  },
};

const configs = [
  baseConfig,
  userConfig,
  eventConfig,
  homeConfig,
  chatConfig,
  adminConfig,
].map(conf => merge(defaultConfig, conf));

module.exports = configs;
