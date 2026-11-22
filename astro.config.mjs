// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://shonosuke100.github.io',
  i18n: {
    locales: ['en', 'ja'],
    defaultLocale: 'en',
    routing: { prefixDefaultLocale: false },
  },
  markdown: {
    // 森をテーマにした配色。紙色の背景になじむ明るい版を使う
    shikiConfig: { theme: 'everforest-light' },
  },
});
