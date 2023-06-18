module.exports = {
  devServer: {
       headers: {
        "Access-Control-Allow-Origin" : "*",
        "Access-Control-Allow-Credentials": true
        },
        proxy: {
          '/api': {
            target: 'http://localhost:5000',
            changeOrigin: true,
            secure: false,
            pathRewrite: {
              '^/api': ''
            },
          }
        }
      }
}

