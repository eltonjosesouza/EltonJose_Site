---
description: Generate creative social media content (Threads, LinkedIn) for a blog post and populate social.json
---

# /social-generate

1. **Identify Context**: Determine the active blog post directory.
2. **Read Content**: Read the `index.mdx` file to understand the full content of the post.
3. **Generate Content (Agent Action)**:
   - **Twitter Thread**: Create a 5-8 tweet thread summarizing the key points. Use a hook in the first tweet.
   - **LinkedIn Post**: Create a professional, engaging post (approx 200 words) suitable for a tech audience.
   - **Hashtags**: Refine or expand specific hashtags based on the content.
4. **Update JSON**:
   - Read the existing `social.json`.
   - Update the `promotion.twitter_thread`, `promotion.summary_professional` (LinkedIn), and `promotion.hashtags` fields with the generated content.
   - Use `write_to_file` to save the updated JSON.
5. **Notify User**: Inform the user that the content has been generated and is ready for review in `social.json`.

**Prompting Strategy for Content:**
- **Twitter**: Viral style, punchy, "👇 Thread".
- **LinkedIn**: Thought leadership, professional but accessible, "O que você acha disso?".
