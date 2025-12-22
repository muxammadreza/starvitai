import config from "@starvit/eslint-config";

/** @type {import("eslint").Linter.Config[]} */
export default [
  { ignores: ["dist/**", "node_modules/**"] },
  ...config,
];
