import { NextRequest } from "next/server";
import { createSupabaseServerClient } from "./server";

export function createSupabaseMiddlewareClient(request: NextRequest) {
  return createSupabaseServerClient();
}

export function middleware(request: NextRequest) {
  return createSupabaseMiddlewareClient(request);
}
