# /social-create-story

1. **Identify Context**: Determine if the user is currently editing a file in a blog post directory or specified one.
2. **Execute Script**: Run the helper script to generate the story image which creates:
   - `feed-post.jpg`: 4:5 vertical post for Feed (LinkedIn, IG, FB) with glassmorphism.
   - `story-cover.jpg`: 9:16 story cover.
   - `story-tweet-X.jpg`: 9:16 story series from Twitter content.

   ```bash
   python3 .agent/scripts/generate_story.py <POST_DIRECTORY>
   ```

3. **Notify User**: Confirm the images have been created.
   - "Feed Post generated at: ..."
   - "Story Cover generated at: ..."
   - "Tweet Stories generated at: ..."

4. **Generate Schedule**: Run the schedule generator to create the posting plan.

   ```bash
   python3 .agent/scripts/generate_schedule.py <POST_DIRECTORY>
   ```

   - Notify user to check `social_schedule.json` and verify Integration IDs are set in `.env` or `.env.local`.

5. **Upload & Schedule (Auto)**:
   - Read the generated `<POST_DIRECTORY>/social_schedule.json`.
   - Call the `blog-posts` MCP tool `integrationSchedulePostTool`.
   - Pass the content of `social_schedule.json` as the `socialPost` argument.
   - Notify the user of the scheduling result.

6. **Git Sync**:
   ```bash
   git add <POST_DIRECTORY>
   git commit -m "chore(social): update assets and schedule for <POST_DIRECTORY>"
   git push origin main
   ```

   - Notify user that changes have been pushed to trigger build.

<truncated 0 bytes>
