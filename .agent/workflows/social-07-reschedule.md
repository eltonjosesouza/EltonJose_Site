# /social-07-reschedule

1. **Identify Context**: Determine the active blog post directory.
2. **Prompt User**: Ask if they want to schedule for "NOW" or a specific "DATE" (YYYY-MM-DD).
3. **Execute Script**: Run the update timing script based on user input:
   - To set to NOW:

     ```bash
     python3 .agent/scripts/social/07_update_timing.py <POST_DIRECTORY> --now
     ```

   - To set to specific DATE:
     ```bash
     python3 .agent/scripts/social/07_update_timing.py <POST_DIRECTORY> --date <YYYY-MM-DD>
     ```

4. **Notify User**: Confirm the `social_schedule.json` has been updated. (This does NOT update the server, only the local file. Run `/social-06-send-posts` to push changes if not yet posted, or manually update via Postiz UI if already posted).
