import { encryptSHA256, getRandomString } from "@medplum/core";

export const MEDPLUM_ACCESS_TOKEN_COOKIE = "medplum_access_token";
export const MEDPLUM_REFRESH_TOKEN_COOKIE = "medplum_refresh_token";
export const MEDPLUM_OAUTH_STATE_COOKIE = "medplum_oauth_state";
export const MEDPLUM_CODE_VERIFIER_COOKIE = "medplum_code_verifier";

export const DEFAULT_MEDPLUM_SCOPE = "openid profile offline_access";

export type PkceDetails = {
  state: string;
  codeVerifier: string;
  codeChallenge: string;
  codeChallengeMethod: "S256";
};

export function getMedplumBaseUrl(): string {
  return process.env.MEDPLUM_BASE_URL ?? "https://api.medplum.com";
}

export function getMedplumAuthorizeUrl(): string {
  return new URL("/oauth2/authorize", getMedplumBaseUrl()).toString();
}

export function getMedplumTokenUrl(): string {
  return process.env.MEDPLUM_OAUTH_TOKEN_URL ?? new URL("/oauth2/token", getMedplumBaseUrl()).toString();
}

export function getMedplumLogoutUrl(): string {
  return new URL("/oauth2/logout", getMedplumBaseUrl()).toString();
}

export function getMedplumAuthMeUrl(): string {
  return process.env.MEDPLUM_AUTH_ME_URL ?? new URL("/auth/me", getMedplumBaseUrl()).toString();
}

export function getMedplumFrontendClientId(): string {
  const clientId = process.env.MEDPLUM_FRONTEND_CLIENT_ID;
  if (!clientId) {
    throw new Error("MEDPLUM_FRONTEND_CLIENT_ID is not configured");
  }
  return clientId;
}

export function getRedirectUri(requestUrl: string): string {
  return new URL("/auth/callback", requestUrl).toString();
}

export function getCookieOptions(maxAgeSeconds?: number) {
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    ...(maxAgeSeconds !== undefined ? { maxAge: maxAgeSeconds } : {}),
  };
}

export async function generatePkce(): Promise<PkceDetails> {
  const state = getRandomString();
  let verifier = "";
  while (verifier.length < 64) {
    verifier += getRandomString().replace(/[^a-zA-Z0-9]/g, "");
  }
  const codeVerifier = verifier.slice(0, 96);
  const hash = await encryptSHA256(codeVerifier);
  const codeChallenge = Buffer.from(new Uint8Array(hash)).toString("base64url");

  return {
    state,
    codeVerifier,
    codeChallenge,
    codeChallengeMethod: "S256",
  };
}
