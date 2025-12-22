import starvitConfig from "@starvit/eslint-config";

export default [
  ...starvitConfig,
  {
    ignores: ["**/node_modules/**", "**/dist/**", "**/.next/**"],
  },
];
