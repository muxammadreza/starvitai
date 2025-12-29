"use client";

import { ReactNode, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

type AuthState =
  | { status: "loading" }
  | { status: "unauthenticated" }
  | { status: "authenticated"; displayName: string };

type ProfileName = {
  text?: string;
  family?: string;
  given?: string[];
};

type ProfileLike = {
  name?: ProfileName[];
  email?: string;
  id?: string;
};

function getDisplayName(profile?: ProfileLike | null): string {
  if (!profile) {
    return "Unknown user";
  }
  const name = profile.name?.[0];
  if (name?.text) {
    return name.text;
  }
  const given = Array.isArray(name?.given) ? name.given.join(" ") : "";
  if (given || name?.family) {
    return [given, name?.family].filter(Boolean).join(" ");
  }
  return profile.email ?? profile.id ?? "Unknown user";
}

export function AuthGuard({ children }: { children: ReactNode }) {
  const router = useRouter();
  const [state, setState] = useState<AuthState>({ status: "loading" });

  useEffect(() => {
    let active = true;
    fetch("/auth/me", { cache: "no-store" })
      .then(async (response) => {
        if (!active) {
          return;
        }
        if (response.status === 401) {
          setState({ status: "unauthenticated" });
          router.replace("/sign-in");
          return;
        }
        const data = await response.json();
        setState({ status: "authenticated", displayName: getDisplayName(data.profile) });
      })
      .catch(() => {
        if (!active) {
          return;
        }
        setState({ status: "unauthenticated" });
        router.replace("/sign-in");
      });

    return () => {
      active = false;
    };
  }, [router]);

  if (state.status === "loading") {
    return <div style={{ padding: "24px" }}>Checking session…</div>;
  }

  if (state.status === "unauthenticated") {
    return <div style={{ padding: "24px" }}>Redirecting to sign in…</div>;
  }

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", padding: "12px 16px" }}>
        <span>Signed in as {state.displayName}</span>
        <button
          type="button"
          onClick={() => window.location.assign("/logout")}
          style={{ border: "none", background: "transparent", cursor: "pointer" }}
        >
          Sign out
        </button>
      </div>
      {children}
    </div>
  );
}
