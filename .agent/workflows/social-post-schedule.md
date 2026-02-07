# /social-post-schedule

1. **Context Identification**
   - Identify the target blog post directory. If unsure, ask the user.

2. **Timing Configuration (Optional)**
   - Ask the user if they want to post **NOW** or schedule for a **Specific Date**.
   - If **NOW**:
     ```bash
     python3 .agent/scripts/update_schedule_timing.py <POST_DIRECTORY> --now
     ```
   - If **DATE** (YYYY-MM-DD):
     ```bash
     python3 .agent/scripts/update_schedule_timing.py <POST_DIRECTORY> --date <YYYY-MM-DD>
     ```
   - If **NO CHANGE**, skip this step.

3. **Read Schedule**
   - Read the file `<POST_DIRECTORY>/social_schedule.json`.

4. **Execute Scheduling**
   - Call the `blog-posts` MCP tool `integrationSchedulePostTool`.
   - Pass the content of `social_schedule.json` as the `socialPost` argument.
   - **Note**: The JSON file is an array of post objects, which matches the `socialPost` schema.

5. **Confirmation**
   - Notify the user of the result.

6. **Git Sync**:
   ```bash
   git add <POST_DIRECTORY>
   git commit -m "chore(social): update schedule status for <POST_DIRECTORY>"
   git push origin main
   ```

   - Notify user that changes have been pushed to trigger build.
