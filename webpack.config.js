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

const chatButtonOpenConfig = {
  entry: {
    main: './src/chat_button_open.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/chat_button_open.js', // <--- Will be compiled to this single file
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

const utilsConfig = {
  entry: {
    main: './src/utils.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/utils.js', // <--- Will be compiled to this single file
  },
};

const notificationConfig = {
  entry: {
    main: './src/notification/notification.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/notification.js', // <--- Will be compiled to this single file
  },
};

const notificationUserConfig = {
  entry: {
    main: './src/notification.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/notification_user.js', // <--- Will be compiled to this single file
  },
};

const notificationAdminConfig = {
  entry: {
    main: './src/notification/notification_admin.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/notification_admin.js', // <--- Will be compiled to this single file
  },
};

const disputeConfig = {
  entry: {
    main: './src/dispute.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/dispute.js',
  },
};

const profileConfig = {
  entry: {
    main: './src/profile.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/profile.js',
  },
}

const userHeaderNotificationsConfig = {
  entry: {
    main: './src/user_header_notifications.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/user_header_notifications.js',
  },
}

const socialMedia = {
  entry: {
    main: './src/social_media.ts',
  },
  output: {
    path: path.resolve(__dirname, './app/static'),
    filename: 'js/social_media.js',
  },
}

const configs = [
  baseConfig,
  userConfig,
  eventConfig,
  homeConfig,
  chatConfig,
  chatButtonOpenConfig,
  adminConfig,
  utilsConfig,
  notificationConfig,
  notificationAdminConfig,
  notificationUserConfig,
  disputeConfig,
  profileConfig,
  userHeaderNotificationsConfig,
  socialMedia,
].map(conf => merge(defaultConfig, conf));

module.exports = configs;
