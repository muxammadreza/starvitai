import { NextRequest } from "next/server";

import { GET as authCallbackGet } from "../auth/callback/route";
import { GET as authMeGet } from "../auth/me/route";
import { MEDPLUM_OAUTH_STATE_COOKIE } from "../lib/medplum-auth";

describe("auth routes", () => {
  it("redirects when state is missing or invalid", async () => {
    const request = new NextRequest("http://localhost:3002/auth/callback?code=abc&state=bad");
    const response = await authCallbackGet(request);

    expect([302, 307]).toContain(response.status);
    const location = response.headers.get("location");
    expect(location).toContain("/sign-in?error=oauth");
  });

  it("redirects when code_verifier is missing", async () => {
    const request = new NextRequest("http://localhost:3002/auth/callback?code=abc&state=expected", {
      headers: {
        cookie: `${MEDPLUM_OAUTH_STATE_COOKIE}=expected`,
      },
    });
    const response = await authCallbackGet(request);

    expect([302, 307]).toContain(response.status);
    const location = response.headers.get("location");
    expect(location).toContain("/sign-in?error=oauth");
  });

  it("returns 401 when auth cookie is missing", async () => {
    const request = new NextRequest("http://localhost:3002/auth/me");
    const response = await authMeGet(request);

    expect(response.status).toBe(401);
  });
});
