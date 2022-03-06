import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
// import Sass from 'sass'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  css: {
    postcss: {
      plugins: [
        {
          postcssPlugin: 'internal:charset-removal',
          AtRule: {
            charset: (atRule) => {
              if (atRule.name === 'charset') atRule.remove();
            }
          }
        }
      ]
    }
  },
  // publicDir: "dist",
  // server: {
  //     proxy: {
  //         "/nkdb/": 'https://db.netkeiba.com',
  //         "/nkrace/": 'https://race.netkeiba.com'
  //     }
  // },
  build: {
    // outDir: "dist"
    // minify: false
    sourcemap: true
  }
})
