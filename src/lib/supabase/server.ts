import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export const createSupabaseServerClient = () => {
  const supabaseUrl = process.env.SUPABASE_URL ?? "";
  const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY ?? "";

  return createServerClient({
    supabaseUrl,
    supabaseKey,
    cookies,
  });
};
