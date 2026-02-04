---
description: Validate the placement and quantity of AdBanner components in MDX posts
---

# Validate Ad Banners Workflow

1.  **Analyze the MDX File**
    - Read the target MDX file to check for `<AdBanner />` usage.
    ```bash
    # Replace with actual file path
    grep -n "<AdBanner" content/path/to/post/index.mdx
    ```

2.  **Check Quantity**
    - Count the number of ads.
    - **Rule**: Maximum of 2 ads per post.

3.  **Check Placement**
    - View the file context around the ads.
    ```bash
    # View 5 lines of context around each ad
    grep -n -C 5 "<AdBanner" content/path/to/post/index.mdx
    ```
    - **Rule**: Not in the first 2 paragraphs (Intro).
    - **Rule**: Not in the last 2 paragraphs (Conclusion).
    - **Rule**: Not adjacent to images (min 2 paragraphs distance).
    - **Rule**: Not adjacent to Headers (H2/H3).

4.  **Fix Issues**
    - If rules are violated, move the `<AdBanner />` to a compliant location (e.g., middle of a long text section).
    - If there are too many ads, remove the excess.
