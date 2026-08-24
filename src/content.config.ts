import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const writings = defineCollection({
  loader: glob({ base: './src/content/writings', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    locale: z.enum(['en', 'ja']),
    description: z.string(),
    publishedAt: z.coerce.date(),
    updatedAt: z.coerce.date().optional(),
    category: z.enum(['software-design', 'ai-engineering', 'law-technology', 'learning-data', 'engineering-systems', 'design']),
    tags: z.array(z.string()).min(1).max(3),
    draft: z.boolean().default(false),
    ogImage: z.string().optional(),
  }),
});

const memories = defineCollection({
  loader: glob({ base: './src/content/memories', pattern: '**/*.md' }),
  schema: z.object({
    title: z.string(),
    locale: z.enum(['en', 'ja']),
    date: z.coerce.date(),
    summary: z.string(),
    categories: z.array(z.enum(['nature', 'study', 'travel', 'reflection'])).min(1),
    latitude: z.number().min(-90).max(90),
    longitude: z.number().min(-180).max(180),
    locationLabel: z.string(),
    elevationMeters: z.number().nonnegative().optional(),
    images: z.array(z.object({ src: z.string(), alt: z.string() })).default([]),
    ogImage: z.string().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { writings, memories };
