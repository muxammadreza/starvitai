'use client';

import { SignInForm } from '@medplum/react';
import { useRouter } from 'next/navigation';

export default function LoginPage() {
  const router = useRouter();

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <SignInForm
        onSuccess={() => router.push('/')}
        googleClientId={process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID}
      >
        <h1>Starvit Clinician Login</h1>
      </SignInForm>
    </div>
  );
}
