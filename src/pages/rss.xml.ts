import type { APIRoute } from 'astro';
import { writingFeed } from '../lib/rss';

export const GET: APIRoute = ({ site }) => writingFeed('en', site!);
