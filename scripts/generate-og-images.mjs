import { readFile, readdir, mkdir } from 'node:fs/promises';
import { relative, resolve } from 'node:path';
import { Resvg } from '@resvg/resvg-js';
import sharp from 'sharp';

const root = process.cwd();
const publicDirectory = resolve(root, 'public');
const ogVersion = process.env.GITHUB_SHA?.slice(0, 12) ?? 'local';
const outputDirectory = resolve(publicDirectory, 'og', ogVersion);
const font = await readFile(resolve(root, 'src/assets/fonts/NotoSansCJKjp-Regular.otf'));
const profile = `data:image/png;base64,${(await readFile(resolve(publicDirectory, 'images/profile.png'))).toString('base64')}`;

async function filesIn(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const nested = await Promise.all(entries.map(async (entry) => {
    const path = resolve(directory, entry.name);
    return entry.isDirectory() ? filesIn(path) : [path];
  }));
  return nested.flat();
}

function frontmatter(source) {
  const match = source.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const value = (key) => match[1].match(new RegExp(`^${key}:\\s*["']?(.+?)["']?\\s*$`, 'm'))?.[1]?.replace(/^['"]|['"]$/g, '');
  return {
    title: value('title'),
    locale: value('locale'),
    description: value('description'),
    summary: value('summary'),
    draft: value('draft'),
    ogImage: value('ogImage'),
  };
}

function contentImageName(kind, locale, id) {
  return `${kind}-${locale}-${id.replace(/^ja\//, '').replaceAll('/', '-')}.png`;
}

function escapeXml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}

function titleLines(title, locale) {
  if (locale === 'ja') {
    const length = title.length > 17 ? 14 : 17;
    return title.match(new RegExp(`.{1,${length}}`, 'g'))?.slice(0, 3) ?? [title];
  }
  const words = title.split(' ');
  const lines = [];
  let line = '';
  for (const word of words) {
    if (`${line} ${word}`.trim().length > 24 && line) {
      lines.push(line);
      line = word;
    } else line = `${line} ${word}`.trim();
  }
  if (line) lines.push(line);
  return lines.slice(0, 3);
}

function cardMarkup({ title, label, locale }, offset = 0) {
  const isJapanese = locale === 'ja';
  const lines = titleLines(title, locale);
  const titleSize = isJapanese ? 66 : 72;
  const lineHeight = isJapanese ? 84 : 86;
  const text = lines.map((line, index) => `<tspan x="76" dy="${index === 0 ? 0 : lineHeight}">${escapeXml(line)}</tspan>`).join('');
  return `<g transform="translate(0 ${offset})">
    <rect width="1200" height="630" fill="#f8f2e8"/>
    <rect x="865" width="335" height="630" fill="#031d27"/>
    <text x="76" y="104" fill="#b76800" font-family="Noto Sans CJK JP" font-size="27" font-weight="700" letter-spacing="2">■  ${escapeXml(label)}</text>
    <text x="76" y="220" fill="#08232d" font-family="Noto Sans CJK JP" font-size="${titleSize}" font-weight="700">${text}</text>
    <text x="76" y="558" fill="#08232d" font-family="Noto Sans CJK JP" font-size="25" font-weight="700" letter-spacing="3">SHO IKEDA</text>
    <image href="${profile}" x="898" y="220" width="270" height="405" preserveAspectRatio="xMidYMax meet"/>
  </g>`;
}

const labels = {
  en: { home: 'Portfolio', about: 'About', work: 'Projects', writing: 'Writing', memories: 'Memory Map', 'not-found': '404 / Lost route', writingItem: 'Writing', memoryItem: 'Memory' },
  ja: { home: 'ポートフォリオ', about: 'プロフィール', work: 'プロジェクト', writing: '記事', memories: '思い出の地図', 'not-found': '404 / 迷子のページ', writingItem: '記事', memoryItem: '思い出' },
};
const staticCards = [
  ['home', 'Sho Ikeda — Build, Learn, Explore', 'Sho Ikeda — つくる、学ぶ、探究する'],
  ['about', 'About Sho', 'Sho Ikedaについて'],
  ['work', 'Selected Projects', 'プロジェクト'],
  ['writing', 'Field Notes', '記事'],
  ['memories', 'Memory Map', '思い出の地図'],
  ['not-found', 'Wrong Turn', '道に迷いました'],
];

await mkdir(outputDirectory, { recursive: true });
const cards = staticCards.flatMap(([page, enTitle, jaTitle]) => [
  { filename: `${page}-en.png`, title: enTitle, label: labels.en[page], locale: 'en' },
  { filename: `${page}-ja.png`, title: jaTitle, label: labels.ja[page], locale: 'ja' },
]);

for (const [kind, sourceDirectory, labelKey] of [
  ['writing', resolve(root, 'src/content/writings'), 'writingItem'],
  ['memory', resolve(root, 'src/content/memories'), 'memoryItem'],
]) {
  for (const path of (await filesIn(sourceDirectory)).filter((file) => file.endsWith('.md'))) {
    const data = frontmatter(await readFile(path, 'utf8'));
    if (data.draft === 'true' || !data.title || !['en', 'ja'].includes(data.locale)) continue;
    const id = relative(sourceDirectory, path).replace(/\.md$/, '');
    cards.push({
      filename: contentImageName(kind, data.locale, id),
      title: data.title,
      label: labels[data.locale][labelKey],
      locale: data.locale,
    });
  }
}

const spriteSvg = `<svg width="1200" height="${cards.length * 630}" viewBox="0 0 1200 ${cards.length * 630}" xmlns="http://www.w3.org/2000/svg">${cards.map((card, index) => cardMarkup(card, index * 630)).join('')}</svg>`;
const sprite = new Resvg(spriteSvg, { font: { fontBuffers: [font], loadSystemFonts: false } }).render().asPng();
await Promise.all(cards.map((card, index) => sharp(sprite).extract({ left: 0, top: index * 630, width: 1200, height: 630 }).png().toFile(resolve(outputDirectory, card.filename))));
console.log(`Generated Open Graph images in ${relative(root, outputDirectory)}.`);
