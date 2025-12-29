import { NextRequest, NextResponse } from "next/server";

import {
  MEDPLUM_ACCESS_TOKEN_COOKIE,
  MEDPLUM_CODE_VERIFIER_COOKIE,
  MEDPLUM_OAUTH_STATE_COOKIE,
  MEDPLUM_REFRESH_TOKEN_COOKIE,
  getCookieOptions,
  getMedplumFrontendClientId,
  getMedplumTokenUrl,
  getRedirectUri,
} from "../../lib/medplum-auth";

export async function GET(request: NextRequest) {
  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");

  const storedState = request.cookies.get(MEDPLUM_OAUTH_STATE_COOKIE)?.value;
  const codeVerifier = request.cookies.get(MEDPLUM_CODE_VERIFIER_COOKIE)?.value;

  if (!code || !state || !storedState || state !== storedState || !codeVerifier) {
    return NextResponse.redirect(new URL("/sign-in?error=oauth", request.url));
  }

  const tokenResponse = await fetch(getMedplumTokenUrl(), {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      code,
      client_id: getMedplumFrontendClientId(),
      redirect_uri: getRedirectUri(request.url),
      code_verifier: codeVerifier,
    }).toString(),
  });

  if (!tokenResponse.ok) {
    return NextResponse.redirect(new URL("/sign-in?error=token", request.url));
  }

  const tokenData = (await tokenResponse.json()) as {
    access_token?: string;
    refresh_token?: string;
    expires_in?: number;
  };

  if (!tokenData.access_token) {
    return NextResponse.redirect(new URL("/sign-in?error=token", request.url));
  }

  const response = NextResponse.redirect(new URL("/", request.url));
  const accessTokenTtl = tokenData.expires_in ?? 3600;

  response.cookies.set(MEDPLUM_ACCESS_TOKEN_COOKIE, tokenData.access_token, getCookieOptions(accessTokenTtl));
  if (tokenData.refresh_token) {
    response.cookies.set(
      MEDPLUM_REFRESH_TOKEN_COOKIE,
      tokenData.refresh_token,
      getCookieOptions(60 * 60 * 24 * 30)
    );
  }

  response.cookies.set(MEDPLUM_OAUTH_STATE_COOKIE, "", getCookieOptions(0));
  response.cookies.set(MEDPLUM_CODE_VERIFIER_COOKIE, "", getCookieOptions(0));

  return response;
}
