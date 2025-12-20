'use client';

import { MedplumClient } from '@medplum/core';
import { MedplumProvider } from '@medplum/react';
import { ReactNode, useState } from 'react';

export function Providers({ children }: { children: ReactNode }) {
  const [medplum] = useState(() => new MedplumClient({
    onUnauthenticated: () => {
      if (typeof window !== 'undefined' && window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    },
    baseUrl: process.env.NEXT_PUBLIC_MEDPLUM_BASE_URL,
  }));

  return (
    <MedplumProvider medplum={medplum}>
      {children}
    </MedplumProvider>
  );
}
