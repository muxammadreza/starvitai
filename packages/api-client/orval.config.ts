import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

import { defineConfig } from 'orval';

const configDir = dirname(fileURLToPath(import.meta.url));
const mutatorPath = resolve(configDir, 'src/orval-mutator.cjs');
const tsconfigPath = resolve(configDir, 'tsconfig.json');

const openApiTarget = process.env.OPENAPI_FILE ?? 'http://localhost:8000/openapi.json';

export default defineConfig({
  starvit: {
    input: {
      target: openApiTarget,
    },
    output: {
      // mode: 'tags-split', // Simplify output mode to avoid generation issues
      target: 'src/generated/api.ts',
      schemas: 'src/generated/model',
      client: 'react-query',
      prettier: true,
      tsconfig: tsconfigPath,
      override: {
        mutator: {
          path: mutatorPath,
          name: 'customInstance',
          extension: '.cjs',
        },
      },
    },
  },
});
