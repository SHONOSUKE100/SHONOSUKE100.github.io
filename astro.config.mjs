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
});
