export type ContentKind = 'writing' | 'memory';

export function contentOgImage(kind: ContentKind, id: string, locale: 'en' | 'ja') {
  return `/og/${kind}-${locale}-${id.replace(/^ja\//, '').replaceAll('/', '-')}.png`;
}

export function staticOgImage(page: 'home' | 'about' | 'work' | 'writing' | 'memories' | 'not-found', locale: 'en' | 'ja') {
  return `/og/${page}-${locale}.png`;
}
