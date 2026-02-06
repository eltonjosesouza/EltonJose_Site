import { format, parseISO } from "date-fns";
import Link from "next/link";
import React from "react";
import { slug } from "github-slugger";
import ViewCounter from "./ViewCounter";

import SharePost from "./SharePost";

const BlogDetails = ({ blog, slug: blogSlug }) => {
  return (
    <div className="px-2  md:px-10 bg-accent dark:bg-accentDark text-light dark:text-dark py-2 flex items-center justify-around flex-wrap text-lg sm:text-xl font-medium mx-5  md:mx-10 rounded-lg">
      <time className="m-3">
        {format(parseISO(blog.publishedAt), "dd/MM/yyyy")}
      </time>
      <span className="m-3">
        <ViewCounter slug={blogSlug} />
      </span>
      <div className="m-3">{blog.readingTime.text.replace('min read', 'minutos de leitura')}</div>
      <Link href={`/categories/${slug(blog.tags[0])}`} className="m-3">
        #{blog.tags[0]}
      </Link>
      <SharePost slug={blogSlug} title={blog.title} description={blog.description} />
    </div>
  );
};

export default BlogDetails;
