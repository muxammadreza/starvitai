import { NextRequest, NextResponse } from "next/server";

import {
  MEDPLUM_ACCESS_TOKEN_COOKIE,
  MEDPLUM_CODE_VERIFIER_COOKIE,
  MEDPLUM_OAUTH_STATE_COOKIE,
  MEDPLUM_REFRESH_TOKEN_COOKIE,
  getCookieOptions,
  getMedplumLogoutUrl,
} from "../lib/medplum-auth";

export async function GET(request: NextRequest) {
  const accessToken = request.cookies.get(MEDPLUM_ACCESS_TOKEN_COOKIE)?.value;
  if (accessToken) {
    try {
      await fetch(getMedplumLogoutUrl(), {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    } catch (error) {
      console.error("Medplum logout failed", error);
    }
  }

  const response = NextResponse.redirect(new URL("/sign-in", request.url));

  response.cookies.set(MEDPLUM_ACCESS_TOKEN_COOKIE, "", getCookieOptions(0));
  response.cookies.set(MEDPLUM_REFRESH_TOKEN_COOKIE, "", getCookieOptions(0));
  response.cookies.set(MEDPLUM_OAUTH_STATE_COOKIE, "", getCookieOptions(0));
  response.cookies.set(MEDPLUM_CODE_VERIFIER_COOKIE, "", getCookieOptions(0));

  return response;
}
