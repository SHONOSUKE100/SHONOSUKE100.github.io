export type ContentKind = 'writing' | 'memory';
const ogVersion = process.env.GITHUB_SHA?.slice(0, 12) ?? 'local';

export function contentOgImage(kind: ContentKind, id: string, locale: 'en' | 'ja') {
  return `/og/${ogVersion}/${kind}-${locale}-${id.replace(/^ja\//, '').replaceAll('/', '-')}.png`;
}

export function staticOgImage(page: 'home' | 'about' | 'work' | 'writing' | 'memories' | 'not-found', locale: 'en' | 'ja') {
  return `/og/${ogVersion}/${page}-${locale}.png`;
}
