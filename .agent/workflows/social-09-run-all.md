# /social-09-run-all

**Sequence: 01 -> 06**

1. **Setup (01)**:
   - Invoke: `@[/social-01-setup]`
   - Result: `social.json` created.

2. **Populate Content (02)**:
   - Invoke: `@[/social-02-populate-content]`
   - Result: Twitter Thread & LinkedIn Post generated.

3. **Generate Images (03)**:
   - Invoke: `@[/social-03-generate-images]`
   - Result: Images created in `social-media/`.

4. **Generate Schedule (04)**:
   - Invoke: `@[/social-04-generate-schedule]`
   - Result: `social_schedule.json` created.

5. **Populate/Review Schedule (05)**:
   - Invoke: `@[/social-05-populate-json-posts]`
   - Result: Review `social_schedule.json` and confirm with user.

6. **Send Posts (06)**:
   - Invoke: `@[/social-06-send-posts]`
   - Result: Posts uploaded and scheduled on Postiz.
