# /social-05-populate-json-posts

1. **Identify Context**: Determine the active blog post directory.
2. **Open File**: Open `social_schedule.json` for the user to review.
3. **Notify User**: Inform the user that the file is open for manual population/Review.
   - Suggest checking:
     - `date`: ISO8601 datetime for scheduling
     - `posts[0].integration.id`: Integration ID from Postiz
     - `posts[0].value[0].content`: Post text (HTML formatting) with hashtags
     - `posts[0].value[0].image`: Image array with local paths (will be uploaded)
     - `posts[0].settings`: Platform-specific settings (post_type, url, etc.)
   - **REQUIRED - Add missing fields:**
     - `tags`: Add relevant tags array (e.g., `["tecnologia", "ai", "dev"]`)
     - **LinkedIn**: Append the blog post URL to `posts[0].value[0].content` (e.g., `"<p>Read more: https://site.com/blogs/post-slug</p>"`)
   - Model reference: See `.agent/scripts/social/models/docs.md` for field details
