import js from "@eslint/js";
import globals from "globals";
import jsxA11y from "eslint-plugin-jsx-a11y";
import react from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import tseslint from "typescript-eslint";
import { defineConfig, globalIgnores } from "eslint/config";

export default defineConfig([
  globalIgnores(["dist", "coverage", "tests"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    plugins: {
      react,
      "jsx-a11y": jsxA11y,
    },
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },
    settings: {
      react: {
        version: "detect",
      },
    },
    rules: {
      ...jsxA11y.flatConfigs.recommended.rules,
      camelcase: ["error", { properties: "always" }],
      complexity: ["error", 6],
      "max-depth": ["error", 3],
      "max-params": ["error", 4],
      "max-statements": ["warn", 20],
      "no-var": "error",
      "no-console": "error",
      "no-duplicate-imports": "error",
      eqeqeq: "error",
      "no-unused-vars": "off",
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "padding-line-between-statements": [
        "warn",
        { blankLine: "always", prev: "*", next: "function" },
        { blankLine: "always", prev: "function", next: "*" },
      ],
      "init-declarations": ["error", "always"],
      "default-case": "error",
      "default-case-last": "error",
      "require-await": "error",
      "max-len": [
        "error",
        {
          code: 120,
          ignoreUrls: true,
          ignoreTemplateLiterals: true,
          ignoreStrings: false,
          ignoreComments: true,
          ignoreRegExpLiterals: true,
        },
      ],
      "no-debugger": "error",
      // quotes: ["warn", "single"],
      "no-magic-numbers": [
        "warn",
        { ignore: [0, 1], ignoreArrayIndexes: true },
      ],
      "camelcase": "warn",
      "complexity": "warn",
      "max-len": [
        "warn",
        {
          code: 120,
          ignoreUrls: true,
          ignoreTemplateLiterals: true,
          ignoreStrings: false,
          ignoreComments: true,
          ignoreRegExpLiterals: true,
        },
      ],
      "no-console": "warn",
      "no-case-declarations": "warn",
      "@typescript-eslint/no-explicit-any": "warn",
      "jsx-a11y/click-events-have-key-events": "off",
      "jsx-a11y/no-static-element-interactions": "off",
      "jsx-a11y/label-has-associated-control": "off",
      "no-unreachable": "error",
    },
  },
  {
    files: ["tests/**/*.{ts,tsx}", "**/*.test.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: {
        ...globals.browser,
        ...globals.vitest,
      },
    },
    rules: {
      "react-refresh/only-export-components": "off",
    },
  },
]);