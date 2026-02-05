-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE post_reviews ENABLE ROW LEVEL SECURITY;
ALTER TABLE donations ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;

-- ============================================
-- PROFILES POLICIES
-- ============================================

-- Everyone can view public profiles
CREATE POLICY "Public profiles are viewable by everyone"
  ON profiles FOR SELECT
  USING (true);

-- Users can update their own profile (except role)
CREATE POLICY "Users can update own profile"
  ON profiles FOR UPDATE
  USING (auth.uid() = id)
  WITH CHECK (auth.uid() = id AND role = (SELECT role FROM profiles WHERE id = auth.uid()));

-- Only admins can change roles
CREATE POLICY "Only admins can change roles"
  ON profiles FOR ALL
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- ============================================
-- POSTS POLICIES
-- ============================================

-- Public can view published non-premium posts
CREATE POLICY "Published posts are public"
  ON posts FOR SELECT
  USING (status = 'published' AND is_premium = FALSE);

-- Premium users can view premium posts
CREATE POLICY "Premium users can view premium posts"
  ON posts FOR SELECT
  USING (
    status = 'published' AND is_premium = TRUE AND has_premium_access()
  );

-- Authors can view their own posts
CREATE POLICY "Authors can view own posts"
  ON posts FOR SELECT
  USING (author_id = auth.uid());

-- Editors and admins can view all posts
CREATE POLICY "Editors can view all posts"
  ON posts FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role IN ('editor', 'admin')
    )
  );

-- Editors and admins can create posts
CREATE POLICY "Editors can create posts"
  ON posts FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role IN ('editor', 'admin')
    )
  );

-- Authors can update their own drafts
CREATE POLICY "Authors can update own drafts"
  ON posts FOR UPDATE
  USING (author_id = auth.uid() AND status = 'draft')
  WITH CHECK (author_id = auth.uid());

-- Editors and admins can update any post
CREATE POLICY "Editors can update any post"
  ON posts FOR UPDATE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role IN ('editor', 'admin')
    )
  );

-- Only admins can delete posts
CREATE POLICY "Only admins can delete posts"
  ON posts FOR DELETE
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- ============================================
-- POST_REVIEWS POLICIES
-- ============================================

-- Revisors, editors, and admins can view reviews
CREATE POLICY "Reviewers can view reviews"
  ON post_reviews FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role IN ('revisor', 'editor', 'admin')
    )
  );

-- Revisors, editors, and admins can create reviews
CREATE POLICY "Reviewers can create reviews"
  ON post_reviews FOR INSERT
  WITH CHECK (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role IN ('revisor', 'editor', 'admin')
    )
  );

-- ============================================
-- DONATIONS POLICIES
-- ============================================

-- Users can view their own donations
CREATE POLICY "Users can view own donations"
  ON donations FOR SELECT
  USING (user_id = auth.uid());

-- Admins can view all donations
CREATE POLICY "Admins can view all donations"
  ON donations FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- System can insert donations (via service role)
CREATE POLICY "System can insert donations"
  ON donations FOR INSERT
  WITH CHECK (true);

-- ============================================
-- SUBSCRIPTIONS POLICIES
-- ============================================

-- Users can view their own subscriptions
CREATE POLICY "Users can view own subscriptions"
  ON subscriptions FOR SELECT
  USING (user_id = auth.uid());

-- Admins can view all subscriptions
CREATE POLICY "Admins can view all subscriptions"
  ON subscriptions FOR SELECT
  USING (
    EXISTS (
      SELECT 1 FROM profiles
      WHERE id = auth.uid() AND role = 'admin'
    )
  );

-- System can manage subscriptions (via service role)
CREATE POLICY "System can manage subscriptions"
  ON subscriptions FOR ALL
  WITH CHECK (true);
