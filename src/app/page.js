import {allBlogs} from "contentlayer/generated";
import HomeCoverSection from "../components/Home/HomeCoverSection";
import FeaturedPosts from "../components/Home/FeaturedPosts";
import RecentPosts from "../components/Home/RecentPosts";
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/next';
import { filterBlogs } from "../utils";

export const revalidate = 3600;

export default function Home() {

  const filteredBlogs = filterBlogs(allBlogs);

  return (
    <main className="flex flex-col items-center justify-center">
      <HomeCoverSection blogs={filteredBlogs} />
      <FeaturedPosts blogs={filteredBlogs} />
      <RecentPosts blogs={filteredBlogs} />
      <Analytics />
      <SpeedInsights />
    </main>
  )
}
