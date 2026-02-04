import { compareDesc, parseISO } from "date-fns";

export const cx = (...classNames) => classNames.filter(Boolean).join(" ");

export const sortBlogs = (blogs) => {
  return blogs
    .slice()
    .sort((a, b) =>
      compareDesc(parseISO(a.publishedAt), parseISO(b.publishedAt))
    );
};

export const filterBlogs = (blogs) => {
  return blogs.filter((blog) => {
    const isPublished = blog.isPublished;
    const publishedDate = new Date(blog.publishedAt);
    const today = new Date();
    // Reset time part to ensure we only compare dates, or just compare timestamps if needed.
    // However, blog.publishedAt is likely yyyy-mm-dd. parseISO handles it.
    // Let's use compareDesc to be safe with date-fns or simple date comparison.
    // If publishedAt is "2026-02-09", new Date("2026-02-09") is UTC.
    // "today" is local time.
    // Let's stick to a simple string comparison or date-fns if possible, but simplest is:
    return isPublished && new Date(blog.publishedAt) <= new Date();
  });
};
