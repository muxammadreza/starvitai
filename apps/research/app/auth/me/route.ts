import { NextRequest, NextResponse } from "next/server";

import { MEDPLUM_ACCESS_TOKEN_COOKIE, getMedplumAuthMeUrl } from "../../lib/medplum-auth";

export async function GET(request: NextRequest) {
  const accessToken = request.cookies.get(MEDPLUM_ACCESS_TOKEN_COOKIE)?.value;
  if (!accessToken) {
    return NextResponse.json({ error: "Unauthenticated" }, { status: 401 });
  }

  const response = await fetch(getMedplumAuthMeUrl(), {
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
  });

  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
