# /social-04-generate-json-posts

1. **Identify Context**: Determine if the user is currently editing a file in a blog post directory.
2. **Execute Script**: Run the schedule generator to create `social_schedule.json` using model templates:

   ```bash
   python3 .agent/scripts/social/04_generate_schedule.py <POST_DIRECTORY>
   ```

   The script loads templates from `.agent/scripts/social/models/`:
   - `linkedin-post.json` - LinkedIn post structure
   - `instagram-post.json` - Instagram feed post structure
   - `instagram-story.json` - Instagram story structure
   - `facebook-json.json` - Facebook post structure

3. **Output Format**: The script generates posts with the model-based structure:

   **All Platforms:**
   - `type`: "schedule" or "now"
   - `date`: ISO8601 datetime
   - `posts`: Array with `integration`, `value`, and `settings`
   - `value[0].content`: Post text with hashtags
   - `value[0].image`: Array of objects with `id` and `path`

   **Platform-specific Settings:**
   - LinkedIn: `{"__type": "linkedin", "post_as_images_carousel": true}`
   - Instagram Story: `{"__type": "instagram", "post_type": "story"}`
   - Instagram Feed: `{"__type": "instagram", "post_type": "post", "collaborators": []}`
   - Facebook: `{"__type": "facebook", "url": "<post_url>"}`

4. **Notify User**: Confirm the `social_schedule.json` has been created and remind them to check:
   - `date` values are correct
   - `posts[0].integration.id` values match their Postiz setup
   - Content is in Brazilian Portuguese
   - Hashtags are included in `posts[0].value[0].content`
