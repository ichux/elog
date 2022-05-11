module.exports = {
  "root": true,
  "env": {
    "browser": true,
    "es2021": true
  },
  "extends": [
    "airbnb-base",
    "plugin:prettier/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": [
    "@typescript-eslint",
    "prettier"
  ],
  "rules": {
    "prettier/prettier": "error",
    "no-unused-vars": "warn",
    "no-console": "off",
    "func-names": "off",
    "no-process-exit": "off",
    "object-shorthand": "off",
    "class-methods-use-this": "off",
    "import/no-unresolved": "off",
    "import/no-extensions": "off",
    "import/extensions": "off",
  },
  overrides: [
    {
      "files": ["src/**/*.d.ts"],
      "rules": {
        "no-unused-vars": "off",
      },
    },
  ],
}
