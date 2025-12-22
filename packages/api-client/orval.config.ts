import { defineConfig } from 'orval';

export default defineConfig({
  starvit: {
    input: {
      target: 'http://localhost:8000/openapi.json',
    },
    output: {
      // mode: 'tags-split', // Simplify output mode to avoid generation issues
      target: 'src/generated/api.ts',
      schemas: 'src/generated/model',
      client: 'react-query',
      prettier: true,
      override: {
        mutator: {
          path: './src/axios-instance.ts',
          name: 'customInstance',
        },
      },
    },
  },
});
