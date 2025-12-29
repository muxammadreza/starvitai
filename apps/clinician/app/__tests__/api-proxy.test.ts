import { NextRequest } from "next/server";
import { vi } from "vitest";

import { GET as proxyGet } from "../api/[...path]/route";
import { MEDPLUM_ACCESS_TOKEN_COOKIE } from "../lib/medplum-auth";

describe("api proxy", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("injects Authorization from cookie and strips cookie header", async () => {
    const fetchSpy = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      void input;
      void init;
      return new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "content-type": "application/json" },
      });
    });
    vi.stubGlobal("fetch", fetchSpy);

    const request = new NextRequest("http://localhost:3001/api/protected", {
      headers: {
        cookie: `${MEDPLUM_ACCESS_TOKEN_COOKIE}=token-123`,
      },
    });

    await proxyGet(request, { params: Promise.resolve({ path: ["protected"] }) });

    expect(fetchSpy).toHaveBeenCalledTimes(1);
    const init = fetchSpy.mock.calls[0]?.[1] as RequestInit | undefined;
    const headers = init?.headers instanceof Headers ? init.headers : new Headers(init?.headers);

    expect(headers.get("authorization")).toBe("Bearer token-123");
    expect(headers.get("cookie")).toBeNull();
  });
});
