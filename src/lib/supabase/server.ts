import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { cookies } from "next/headers";

export async function createClient() {
  const cookieStore = await cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        async getAll() {
          return await cookieStore.getAll();
        },
        async setAll(cookiesToSet: { name: string; value: string; options: CookieOptions }[]) {
          try {
            for (const cookie of cookiesToSet) {
              await cookieStore.set({
                name: cookie.name,
                value: cookie.value,
                ...cookie.options,
              });
            }
          } catch {
            // This error is expected in Server Components
          }
        },
      },
    }
  );
}