import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";
import { fixupPluginRules } from "@eslint/compat";
import path from "path";
import { fileURLToPath } from "url";
import globals from "globals";
import nextPlugin from "@next/eslint-plugin-next";
import reactPlugin from "eslint-plugin-react";
import hooksPlugin from "eslint-plugin-react-hooks";
import turboPlugin from "eslint-plugin-turbo";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default [
    {
        ignores: [".next/**", "dist/**", "node_modules/**"],
    },
    js.configs.recommended,
    turboPlugin.configs["flat/recommended"],
    ...compat.extends("plugin:@typescript-eslint/recommended"),
    {
        files: ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx"],
        plugins: {
            "react": reactPlugin,
            "react-hooks": fixupPluginRules(hooksPlugin),
            "@next/next": fixupPluginRules(nextPlugin),
        },
        rules: {
            ...reactPlugin.configs.recommended.rules,
            ...hooksPlugin.configs.recommended.rules,
            ...nextPlugin.configs.recommended.rules,
            ...nextPlugin.configs["core-web-vitals"].rules,
            "react/react-in-jsx-scope": "off",
        },
        settings: {
            react: {
                version: "detect",
            }
        },
        languageOptions: {
            globals: {
                ...globals.browser,
                ...globals.node,
            }
        }
    }
];

