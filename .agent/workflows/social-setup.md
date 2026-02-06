---
description: Setup social media sidecar (social.json) for the current blog post
---

# /social-setup

1. **Identify Context**: Determine if the user is currently editing a file in a blog post directory (e.g., `content/.../index.mdx`).
2. **Execute Script**: Run the helper script to generate the JSON file.
   ```bash
   python .agent/scripts/create_social_sidecar.py .
   ```
   *(Ensure you run this terminal command in the directory found in step 1, or pass the absolute path as an argument)*

3. **Open File**: Open the newly created `social.json` file for the user to edit.
