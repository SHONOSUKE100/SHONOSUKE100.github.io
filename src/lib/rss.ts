import { publishedWritings, writingHref, type Locale } from './writing';

const escape = (value: string) => value.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

/** 記事一覧の RSS 2.0 フィードを作る。 */
export async function writingFeed(locale: Locale, site: URL) {
  const posts = await publishedWritings(locale);
  const ja = locale === 'ja';
  const home = new URL(ja ? '/ja/writing/' : '/writing/', site).href;
  const items = posts.map((post) => {
    const url = new URL(writingHref(post), site).href;
    return `<item><title>${escape(post.data.title)}</title><link>${url}</link><guid>${url}</guid><pubDate>${post.data.publishedAt.toUTCString()}</pubDate><description>${escape(post.data.description)}</description><category>${escape(post.data.category)}</category></item>`;
  }).join('');
  const xml = `<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>${ja ? 'Sho Ikeda の記事' : 'Sho Ikeda — Writing'}</title><link>${home}</link><description>${ja ? '感じたこと・学んだこと・考えたこと' : 'Thoughts on software, AI, law, and learning.'}</description><language>${locale}</language><lastBuildDate>${new Date().toUTCString()}</lastBuildDate>${items}</channel></rss>`;
  return new Response(xml, { headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' } });
}
