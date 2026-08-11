import { access, readdir } from 'node:fs/promises';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const direction = process.argv[2];
if (!['en-to-ja', 'ja-to-en'].includes(direction)) throw new Error('Direction must be en-to-ja or ja-to-en.');

const sourceLocale = direction === 'en-to-ja' ? 'en' : 'ja';
const roots = ['src/content/writings', 'src/content/memories'];

async function exists(file) {
  try { await access(file); return true; } catch { return false; }
}

async function markdownFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const files = await Promise.all(entries.map(async (entry) => {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) return markdownFiles(file);
    return entry.isFile() && entry.name.endsWith('.md') ? [file] : [];
  }));
  return files.flat();
}

function latestCommitTime(file) {
  try {
    return Number(execFileSync('git', ['log', '-1', '--format=%ct', '--', file], { encoding: 'utf8' }).trim()) || 0;
  } catch { return 0; }
}

const selected = [];
for (const root of roots) {
  const files = await markdownFiles(root);
  for (const file of files) {
    const normalized = file.split(path.sep).join('/');
    const isJapanese = normalized.includes('/ja/');
    if ((sourceLocale === 'ja') !== isJapanese) continue;
    const target = isJapanese
      ? normalized.replace('/ja/', '/')
      : normalized.replace(`${root}/`, `${root}/ja/`);
    if (!await exists(target) || latestCommitTime(normalized) > latestCommitTime(target)) selected.push(normalized);
  }
}

process.stdout.write(selected.join('\n'));
