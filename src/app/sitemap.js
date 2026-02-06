import { allBlogs } from 'contentlayer/generated';

export default async function sitemap() {
  const siteUrl = 'https://www.eltonjose.com.br';

  // Blog posts
  const blogs = allBlogs.map((post) => ({
    url: `${siteUrl}${post.url}`,
    lastModified: post.publishedAt || post.updatedAt || new Date().toISOString(),
    changeFrequency: 'weekly',
    priority: 0.7,
  }));

  // Static pages
  const routes = [
    '',
    '/about',
    '/contact',
    '/blogs',
    '/courses',
    '/privacy-policy',
    '/terms',
  ].map((route) => ({
    url: `${siteUrl}${route}`,
    lastModified: new Date().toISOString(),
    changeFrequency: route === '' ? 'daily' : 'monthly',
    priority: route === '' ? 1.0 : 0.8,
  }));

  return [...routes, ...blogs];
}
