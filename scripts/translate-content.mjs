import { access, mkdir, readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';

const apiKey = process.env.GEMINI_API_KEY;
const overwrite = process.argv.includes('--overwrite');
const files = process.argv.slice(2).filter((argument) => argument !== '--overwrite');

if (files.length === 0) process.exit(0);

function counterpart(file) {
  const normalized = file.split(path.sep).join('/');
  const match = normalized.match(/^(src\/content\/(?:writings|memories))\/(ja\/)?(.+\.md)$/);
  if (!match) return null;
  const [, base, japanesePrefix, name] = match;
  return japanesePrefix ? `${base}/${name}` : `${base}/ja/${name}`;
}

async function exists(file) {
  try { await access(file); return true; } catch { return false; }
}

async function translate(source, target, targetLocale) {
  const prompt = `Translate this portfolio Markdown from ${targetLocale === 'ja' ? 'English to natural Japanese' : 'Japanese to natural English'}.

Return only a complete Markdown document. Preserve the YAML frontmatter structure, dates, URLs, image paths, numeric coordinates, categories, tags, and draft value exactly. Set the frontmatter locale value to "${targetLocale}". Translate title, description, summary, locationLabel, image alt text, and body prose. Do not add commentary or Markdown code fences.

SOURCE:\n${source}`;
  const response = await fetch('https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-goog-api-key': apiKey },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.2, responseMimeType: 'text/plain' },
    }),
  });
  if (!response.ok) throw new Error(`Gemini API failed (${response.status}): ${await response.text()}`);
  const payload = await response.json();
  const output = payload.candidates?.[0]?.content?.parts?.map((part) => part.text ?? '').join('').trim();
  if (!output?.startsWith('---\n') || !output.includes(`locale: ${targetLocale}`)) throw new Error('Gemini returned invalid Markdown frontmatter.');
  await mkdir(path.dirname(target), { recursive: true });
  await writeFile(target, `${output}\n`, 'utf8');
  console.log(`Created ${target}`);
}

for (const file of files) {
  const target = counterpart(file);
  if (!target || (!overwrite && await exists(target))) continue;
  if (!apiKey) throw new Error('GEMINI_API_KEY is required.');
  const source = await readFile(file, 'utf8');
  const targetLocale = file.split(path.sep).includes('ja') ? 'en' : 'ja';
  await translate(source, target, targetLocale);
}
