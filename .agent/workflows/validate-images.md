---
description: Validate and generate missing images for MDX blog posts
---

# Validate and Generate Images Workflow

1.  **Analyze the MDX File**
    Read the target MDX file to understand the context and identify referenced images.
    ```bash
    # Replace with actual file path
    cat content/path/to/post/index.mdx
    ```

2.  **Check for Image Existence**
    Extract the image paths from the `image:` frontmatter and `<Image src="..." />` components. Check if these files exist in the `public` directory.
    ```bash
    # Example check
    ls -F public/blogs/image-name.ext
    ```

3.  **Generate Missing Images**
    For any image that does not exist:
    *   Construct a detailed prompt based on the blog post context and the image alt text/name.
    *   Use the `generate_image` tool to create the image.
    *   Ensure the style is consistent (e.g., "Modern Tech/AI", "Clean Line Art").

4.  **Verify Creation**
    Confirm that the images have been successfully created and placed in the correct directory.
    ```bash
    ls -F public/blogs/
    ```
