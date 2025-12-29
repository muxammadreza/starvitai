import { NextRequest, NextResponse } from "next/server";

import {
  DEFAULT_MEDPLUM_SCOPE,
  MEDPLUM_CODE_VERIFIER_COOKIE,
  MEDPLUM_OAUTH_STATE_COOKIE,
  generatePkce,
  getCookieOptions,
  getMedplumAuthorizeUrl,
  getMedplumFrontendClientId,
  getRedirectUri,
} from "../lib/medplum-auth";

export async function GET(request: NextRequest) {
  const { state, codeVerifier, codeChallenge, codeChallengeMethod } = await generatePkce();
  const clientId = getMedplumFrontendClientId();
  const redirectUri = getRedirectUri(request.url);

  const authorizeUrl = new URL(getMedplumAuthorizeUrl());
  authorizeUrl.searchParams.set("response_type", "code");
  authorizeUrl.searchParams.set("client_id", clientId);
  authorizeUrl.searchParams.set("redirect_uri", redirectUri);
  authorizeUrl.searchParams.set("scope", DEFAULT_MEDPLUM_SCOPE);
  authorizeUrl.searchParams.set("state", state);
  authorizeUrl.searchParams.set("code_challenge_method", codeChallengeMethod);
  authorizeUrl.searchParams.set("code_challenge", codeChallenge);

  const response = NextResponse.redirect(authorizeUrl.toString());
  response.cookies.set(MEDPLUM_OAUTH_STATE_COOKIE, state, getCookieOptions(600));
  response.cookies.set(MEDPLUM_CODE_VERIFIER_COOKIE, codeVerifier, getCookieOptions(600));
  return response;
}
