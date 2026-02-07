# /social-08-reset-post

1. **Identify Context**: Determine the active blog post directory.
2. **List Existing Files**: Check which files exist in the post directory.
3. **Confirm Action**: Warn the user which files will be deleted (`social.json`, `social_schedule.json`, `social-media/`). (The `.mdx` file will NOT be touched).
4. **Execute Deletion One by One**:

   ```bash
   # Check and remove social.json if exists
   if [ -f "<POST_DIRECTORY>/social.json" ]; then
     echo "🗑️  Removing social.json..."
     rm "<POST_DIRECTORY>/social.json"
   fi

   # Check and remove social_schedule.json if exists
   if [ -f "<POST_DIRECTORY>/social_schedule.json" ]; then
     echo "🗑️  Removing social_schedule.json..."
     rm "<POST_DIRECTORY>/social_schedule.json"
   fi

   # Check and remove social-media directory if exists
   if [ -d "<POST_DIRECTORY>/social-media" ]; then
     echo "🗑️  Removing social-media/ directory..."
     rm -rf "<POST_DIRECTORY>/social-media"
   fi
   ```

5. **Notify User**: Confirm which files were removed and that the post is clean for a fresh start.
