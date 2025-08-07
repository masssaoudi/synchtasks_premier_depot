module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2022: true,
  },
  extends: [
    'eslint:recommended',
    'plugin:vue/vue3-recommended',
    '@vue/eslint-config-prettier',
  ],
  parserOptions: {
    ecmaVersion: 2022,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: ['vue'],
  rules: {
    // 🚀 Vue.js Rules
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'warn',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    'vue/prop-name-casing': ['error', 'camelCase'],
    'vue/attribute-hyphenation': ['error', 'always'],
    'vue/v-on-event-hyphenation': ['error', 'always'],
    'vue/require-default-prop': 'warn',
    'vue/require-prop-types': 'warn',
    'vue/no-unused-components': 'warn',
    'vue/no-v-html': 'warn',
    'vue/valid-v-slot': 'error',
    'vue/no-multiple-template-root': 'off', // Vue 3 allows multiple roots

    // 🚀 JavaScript Rules
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-unused-vars': ['warn', { argsIgnorePattern: '^_' }],
    'no-undef': 'error',
    'no-var': 'error',
    'prefer-const': 'error',

    // 🚀 Code Quality
    eqeqeq: ['error', 'always'],
    curly: ['error', 'all'],
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    'no-script-url': 'error',

    // 🚀 Best Practices
    'array-callback-return': 'error',
    'consistent-return': 'warn',
    'default-case': 'warn',
    'no-case-declarations': 'error',
    'no-empty': 'warn',
    'no-extra-boolean-cast': 'error',
    'no-extra-semi': 'error',
    'no-fallthrough': 'error',
    'no-global-assign': 'error',
    'no-redeclare': 'error',
    'no-self-assign': 'error',
    'no-unreachable': 'error',
    'no-unsafe-negation': 'error',
    'use-isnan': 'error',
    'valid-typeof': 'error',

    // 🚀 ES6+ Features
    'arrow-spacing': 'error',
    'no-duplicate-imports': 'error',
    'no-useless-constructor': 'error',
    'prefer-arrow-callback': 'warn',
    'prefer-template': 'warn',
    'template-curly-spacing': 'error',
  },
  globals: {
    // 🚀 Vue 3 Composition API
    defineProps: 'readonly',
    defineEmits: 'readonly',
    defineExpose: 'readonly',
    withDefaults: 'readonly',

    // 🚀 Browser APIs
    window: 'readonly',
    document: 'readonly',
    navigator: 'readonly',
    localStorage: 'readonly',
    sessionStorage: 'readonly',

    // 🚀 Build tools
    process: 'readonly',
    __dirname: 'readonly',
    __filename: 'readonly',
  },
  overrides: [
    {
      files: ['*.vue'],
      rules: {
        'vue/component-name-in-template-casing': 'off', // Allow kebab-case in template
      },
    },
    {
      files: ['*.js'],
      rules: {
        'vue/valid-template-root': 'off',
      },
    },
    {
      files: ['*.d.ts', '*.ts'],
      parser: '@typescript-eslint/parser',
      plugins: ['@typescript-eslint'],
      rules: {
        'no-undef': 'off',
        '@typescript-eslint/no-unused-vars': 'warn',
      },
    },
  ],
  settings: {
    'import/resolver': {
      node: {
        extensions: ['.js', '.jsx', '.ts', '.tsx', '.vue'],
      },
    },
  },
};
