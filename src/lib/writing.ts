import { getCollection, type CollectionEntry } from 'astro:content';

export type Locale = 'en' | 'ja';
export type Writing = CollectionEntry<'writings'>;

const categoryLabels: Record<Writing['data']['category'], Record<Locale, string>> = {
  'software-design': { en: 'Software Design', ja: 'ソフトウェア設計' },
  'ai-engineering': { en: 'AI Engineering', ja: 'AI エンジニアリング' },
  'law-technology': { en: 'Law & Technology', ja: '法とテクノロジー' },
  'learning-data': { en: 'Learning & Data', ja: '学びとデータ' },
  'engineering-systems': { en: 'Engineering Systems', ja: 'システム開発' },
  design: { en: 'Design', ja: 'デザイン' },
};

export function categoryLabel(category: Writing['data']['category'], locale: Locale) {
  return categoryLabels[category][locale];
}

/** 2026.11.22 のように、桁をそろえた日付にする（言語によらず同じ形）。 */
export function formatDate(date: Date) {
  const pad = (n: number) => String(n).padStart(2, '0');
  return `${date.getFullYear()}.${pad(date.getMonth() + 1)}.${pad(date.getDate())}`;
}

/** 本文から読了時間（分）を見積もる。日本語は1分 500 字、英語は1分 220 語で数える。 */
export function readingMinutes(body: string | undefined, locale: Locale) {
  const text = (body ?? '')
    .replace(/^---[\s\S]*?---/, '')
    .replace(/```[\s\S]*?```/g, '')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '')
    .replace(/<!--[\s\S]*?-->/g, '');
  const amount = locale === 'ja' ? text.replace(/\s/g, '').length / 500 : text.split(/\s+/).filter(Boolean).length / 220;
  return Math.max(1, Math.round(amount));
}

export function readingLabel(minutes: number, locale: Locale) {
  return locale === 'ja' ? `約${minutes}分` : `${minutes} min read`;
}

export function slugOf(post: Writing) {
  return post.id.replace(/^ja\//, '');
}

export function writingHref(post: Writing) {
  return post.data.locale === 'ja' ? `/ja/writing/${slugOf(post)}/` : `/writing/${slugOf(post)}/`;
}

/** 公開済みの記事を、新しい順に返す。 */
export async function publishedWritings(locale: Locale) {
  const posts = await getCollection('writings', ({ data }) => !data.draft && data.locale === locale);
  return posts.sort((a, b) => b.data.publishedAt.getTime() - a.data.publishedAt.getTime());
}
