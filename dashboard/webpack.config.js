/**
 * Webpack Configuration for Engineering Dashboard Module
 * 
 * This configuration resolves all module paths correctly for the dashboard components.
 */

const path = require('path');

module.exports = {
  mode: 'development',
  entry: './src/index.js',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'dist'),
    library: 'Dashboard'
  },
  resolve: {
    alias: {
      // Map relative paths to actual file locations
      'components': path.resolve(__dirname, 'components'),
      'types': path.resolve(__dirname, 'src/types.ts')
    },
    extensions: ['.js', '.jsx', '.ts', '.tsx']
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx|ts|tsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      }
    ]
  },
  experiments: {
    // Enable TypeScript support for JSX files
    typeScript: true
  }
};
