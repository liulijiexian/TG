import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// 为传统浏览器提供支持
import legacy from '@vitejs/plugin-legacy'

// ElementPlus组件库-按需导入
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import Icons from 'unplugin-icons/vite'
import IconsResolver from 'unplugin-icons/resolver'

import viteCompression from 'vite-plugin-compression'

// https://vitejs.dev/config/
export default defineConfig({
  // 静态资源打包处理
  build: {
    // chunkSizeWarningLimit: 1500,  // 大文件报警阈值设置,不建议使用
    rollupOptions: {
      output: {
        chunkFileNames: 'static/js/[name]-[hash].js',
        entryFileNames: 'static/js/[name]-[hash].js',
        assetFileNames: 'static/[ext]/[name]-[hash].[ext]',
        manualChunks(id) {  // 静态资源分拆打包
          if (id.includes('node_modules')) {
            return id.toString().split('node_modules/')[1].split('/')[0].toString();
          }
        }
      }
    }
  },
  server: {
    host: '0.0.0.0',
    port: 8080,
    open: true,  // 启动服务时，是否自动打开浏览器，true是
  },
  plugins: [
    vue(),
    vueJsx(),
    legacy({
      targets: ['defaults', 'not IE 11'],
    }),
    // 自动导入
    AutoImport({
      resolvers: [
        ElementPlusResolver({}),
        IconsResolver(),
      ],
    }),
    // 自动注册
    Components({
      resolvers: [
        ElementPlusResolver(),
        IconsResolver({
          // {prefix}-{collection}-{icon} 使用组件解析器时，您必须遵循名称转换才能正确推断图标。
          prefix: false,  // 自动引入的Icon组件统一前缀，默认为 i，设置false为不需要前缀
          enabledCollections: ['ep'],
        }),
      ],
    }),
    Icons({
      autoInstall: true,
      compiler: 'vue3', // 编译方式
    }),
    // gzip静态资源压缩 
    [viteCompression({
      verbose: true,
      disable: false,
      threshold: 10240,
      algorithm: 'gzip',
      ext: '.gz',
    })],
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
