# PLAN-seo-supabase-fix

> **Goal**: Fix Supabase stability issues and perform comprehensive SEO/GEO optimization.

---

## Phase 0: Socratic Gate (User Input Required)

We need to clarify the "Supabase" architecture before fixing it.

> [!IMPORTANT]
> **Please answer these questions:**
> 1.  **Supabase Setup**: Are you using a **local Docker** Supabase instance (with Studio, Kong, etc.) OR are you connecting to the **hosted Supabase Cloud**?
>     - *Observation*: I only see a `postgres` container running. I do not see the standard Supabase stack (Kong, Studio, GoTrue).
> 2.  **The "Stop" Symptom**: When you say "stops working", what happens?
>     - Does the site return 500 errors?
>     - Does the database connection fail?
>     - Do you have to restart Docker to fix it?
> 3.  **SEO Goal**: Are you focusing on Google Ranking (Traditional SEO) or trying to get cited by AI (GEO)?

---

## Phase 1: Analysis & Discovery

### 1.1 Supabase Stability Investigation
- [ ] **Audit Docker Logs**: Check `postgres` and app logs for connection timeouts or crashes.
- [ ] **Resource Check**: Verify if containers are hitting memory limits (`docker stats`).
- [ ] **Config Review**: Check `docker-compose.yml` for healthcheck configurations and restart policies.

### 1.2 SEO Audit (using `seo-specialist` agent)
- [ ] **Technical Audit**: Run `seo_checker.py` (if available) or manual audit.
    - Check metadata (Title, Description).
    - Check Sitemap & Robots.txt.
    - Check Semantic HTML structure.
- [ ] **Performance Audit**: Check Core Web Vitals (LCP, CLS, INP) constraints.
- [ ] **GEO Audit**: Check for "AI-friendly" content structures (Lists, Tables, Citations).

---

## Phase 2: Implementation Plan

### 2.1 Fix Supabase/Postgres Stability
- [ ] **Option A (If OOM)**: Increase container memory limits.
- [ ] **Option B (If Connection)**: Optimize connection pool strings in `.env`.
- [ ] **Option C (If Architecture)**: Re-deploy full Supabase stack if components are missing.

### 2.2 Implement SEO Improvements
- [ ] **Metadata**: Update `layout.tsx` / `head.js` with optimized tags.
- [ ] **Sitemap**: Configure `next-sitemap` properly.
- [ ] **Structured Data**: Add JSON-LD schemas for Blog/Article.
- [ ] **Performance**: Optimize images (`next/image`) and fonts.

---

## Phase 3: Verification

- [ ] **Stability Test**: Load test the database connection.
- [ ] **SEO Verification**: Run Lighthouse Audit and validate meta tags.
- [ ] **Deployment**: Verify Vercel build passes with new configs.

---

## Agent Assignments

- **Supabase Fix**: `backend-specialist` + `systematic-debugging`
- **SEO Audit**: `seo-specialist` + `frontend-design`
