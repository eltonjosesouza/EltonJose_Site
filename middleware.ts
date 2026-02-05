import { type NextRequest, NextResponse } from "next/server";
import { updateSession } from "@/src/lib/supabase/middleware";
import { type SupabaseClient } from "@supabase/supabase-js";
import { type Database } from "@/src/types/supabase";

const ROLE_ROUTES = {
  admin: ["/admin"],
  editor: ["/editor", "/admin/posts"],
  revisor: ["/revisor"],
  assinante: ["/premium"],
  doador: ["/premium", "/doadores"],
};

export async function middleware(request: NextRequest) {
  // Update session using the utility
  const { supabaseResponse, user, supabase } = await updateSession(request);

  if (request.nextUrl.pathname.startsWith("/admin")) {
    console.log("Middleware: Checking /admin access");
    console.log("Middleware: User found?", !!user);
    if (user)
      console.log(
        "Middleware: User Role?",
        (user.app_metadata as any)?.role || "unknown",
      );
  }

  const typedSupabase = supabase as unknown as SupabaseClient<Database>;

  // Public routes that don't need auth checks beyond session refresh
  const publicRoutes = ["/", "/login", "/signup", "/blog", "/about"];
  const isPublicRoute = publicRoutes.some(
    (route) =>
      request.nextUrl.pathname === route ||
      request.nextUrl.pathname.startsWith(`${route}/`),
  );

  // Allow static assets and api auth routes
  if (
    request.nextUrl.pathname.startsWith("/_next") ||
    request.nextUrl.pathname.startsWith("/api/") ||
    request.nextUrl.pathname.includes(".")
  ) {
    return supabaseResponse;
  }

  // If user is not signed in and tries to access protected route
  if (!user && !isPublicRoute) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    url.searchParams.set("redirect", request.nextUrl.pathname);
    return NextResponse.redirect(url);
  }

  // If user is signed in, check role permissions for specific routes
  if (user) {
    // Explicitly type the result to avoid 'never' inference
    const { data: profile } = (await typedSupabase
      .from("profiles")
      .select("role")
      .eq("id", user.id)
      .single()) as {
      data: { role: Database["public"]["Enums"]["user_role"] } | null;
      error: any;
    };

    if (profile) {
      const pathname = request.nextUrl.pathname;
      const userRole = profile.role;

      // Admin has access to everything
      if (userRole === "admin") {
        return supabaseResponse;
      }

      // Check specific role routes
      for (const [role, routes] of Object.entries(ROLE_ROUTES)) {
        const isRestrictedRoute = routes.some((route) =>
          pathname.startsWith(route),
        );

        if (isRestrictedRoute) {
          // If route requires a role the user doesn't have (and user is not admin)
          if (userRole !== role) {
            // Special case: 'premium' route accessible by 'assinante' OR 'doador'
            if (pathname.startsWith("/premium")) {
              if (userRole === "assinante" || userRole === "doador") {
                return supabaseResponse;
              }
            }

            const url = request.nextUrl.clone();
            url.pathname = "/unauthorized";
            return NextResponse.redirect(url);
          }
        }
      }
    }
  }

  return supabaseResponse;
}

export const config = {
  matcher: [
    /*
     * Match all request paths except for:
     * 1. _next/static (static files)
     * 2. _next/image (image optimization files)
     * 3. favicon.ico (favicon file)
     * Feel free to modify this pattern to include more paths.
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
