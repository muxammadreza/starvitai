import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const resolvedParams = await params;
  return proxy(request, resolvedParams);
}

export async function POST(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const resolvedParams = await params;
  return proxy(request, resolvedParams);
}

export async function PUT(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const resolvedParams = await params;
  return proxy(request, resolvedParams);
}

export async function DELETE(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const resolvedParams = await params;
  return proxy(request, resolvedParams);
}

export async function PATCH(request: NextRequest, { params }: { params: Promise<{ path: string[] }> }) {
  const resolvedParams = await params;
  return proxy(request, resolvedParams);
}

async function proxy(request: NextRequest, params: { path: string[] }) {
  const path = params.path.join("/");
  const baseUrl = process.env.STARVIT_API_INTERNAL_URL || "http://localhost:8000";
  const targetUrl = `${baseUrl}/api/${path}${request.nextUrl.search}`;

  console.log(`[Proxy] ${request.method} ${targetUrl}`);

  try {
    const headers = new Headers(request.headers);
    headers.delete("host");
    headers.delete("connection");
    
    // Pass the bearer token if present
    const authHeader = request.headers.get("authorization");
    if (authHeader) {
        headers.set("authorization", authHeader);
    }

    const body = request.method !== "GET" && request.method !== "HEAD" ? await request.blob() : null;

    const response = await fetch(targetUrl, {
      method: request.method,
      headers: headers,
      body: body,
      // @ts-expect-error - Next.js/Node fetch extension
      duplex: 'half', 
    });

    return new NextResponse(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
    });
  } catch (error) {
    console.error(`[Proxy Error] ${error}`);
    return NextResponse.json({ error: "Upstream Error" }, { status: 502 });
  }
}
