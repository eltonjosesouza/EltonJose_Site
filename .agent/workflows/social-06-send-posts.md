# /social-06-send-posts

1. **Identify Context**: Determine the active blog post directory.

2. **Generate Schedule (if needed)**: If `social_schedule.json` does not exist, generate it using the model templates:

   ```bash
   python3 .agent/scripts/social/04_generate_schedule.py <POST_DIRECTORY>
   ```

   This script loads templates from `.agent/scripts/social/models/`:
   - `linkedin-post.json` - LinkedIn post with carousels
   - `facebook-json.json` - Facebook post with link
   - `instagram-post.json` - Instagram feed post
   - `instagram-story.json` - Instagram story

3. **Execute Script**: Run the API script to upload images and schedule posts:

   ```bash
   python3 .agent/scripts/social/06_send_posts.py <POST_DIRECTORY>
   ```

   The script auto-detects format:
   - **Model format** (new): Uses `posts`, `value`, `image` structure from templates
   - **Legacy format**: Converts `postsAndComments`, `attachments` to API format

4. **Special Handling**: The script automatically handles platform-specific requirements:
   - **Instagram Stories**:
     - Multiple images are sent as separate scheduled posts with 1-minute intervals (e.g., 09:00, 09:01, 09:02, etc.)
     - Each story is configured to **repeat for 2 days** (posts on day 1, day 2, and day 3)
   - **Instagram Feed**: Supports multiple images in a single post (carousel)
   - **Facebook Feed**: Single post with link and images

5. **Notify User**: Inform the user of the scheduling result (watch for "SUCCESS" or errors).

## Model Templates

Reference models are stored in `.agent/scripts/social/models/`:

- See `docs.md` for detailed documentation
- Models define the exact API payload structure for each platform
- Scripts use these as templates and fill in post-specific data
