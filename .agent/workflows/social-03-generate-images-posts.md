# /social-03-generate-images-posts

1. **Identify Context**: Determine if the user is currently editing a file in a blog post directory or specified one.
2. **Execute Script**: Run the helper script to generate the story/feed images:

   ```bash
   python3 .agent/scripts/social/03_generate_assets.py <POST_DIRECTORY>
   ```

3. **Notify User**: Confirm the images have been created in the `social-media/` subdirectory.
