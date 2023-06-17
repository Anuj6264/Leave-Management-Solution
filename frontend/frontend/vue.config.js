// const { defineConfig } = require('@vue/cli-service')
// module.exports = defineConfig({
//   transpileDependencies: true,
//   lintOnSave: false,
//   devServer: {
//     proxy: {
//       '/api': {
//         target: 'http://localhost:5000',
//         changeOrigin: true,
//         secure: false,
//         pathRewrite: {
//           '^/api': ''
//         },
//         ws:true
//       }
//     }
//   }
// })

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

