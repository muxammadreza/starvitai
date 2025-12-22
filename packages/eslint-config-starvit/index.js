import js from "@eslint/js";
import turboPlugin from "eslint-plugin-turbo";

export default [
  js.configs.recommended,
  turboPlugin.configs["flat/recommended"],
  {
    rules: {
      "turbo/no-undeclared-env-vars": "error",
    },
  },
];
