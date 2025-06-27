// Prettier 3.6 Configuration (2025 Best Practices)
export default {
  // Core formatting
  semi: true,
  singleQuote: true,
  trailingComma: 'all',
  tabWidth: 2,
  printWidth: 100, // 2025: Increased from 80 for modern screens
  useTabs: false,
  
  // Code style
  arrowParens: 'always',
  endOfLine: 'lf',
  bracketSpacing: true,
  bracketSameLine: false,
  
  // JSX specific
  jsxSingleQuote: false,
  
  // 2025 New features
  experimentalTernaries: false, // Keep stable for now
  
  // Prose handling
  proseWrap: 'preserve',
  
  // Plugin configuration
  plugins: [
    // 'prettier-plugin-tailwindcss', // Uncomment if using Tailwind CSS
  ],
  
  // File-specific overrides
  overrides: [
    {
      files: '*.md',
      options: {
        proseWrap: 'always',
        printWidth: 80,
      },
    },
    {
      files: '*.json',
      options: {
        printWidth: 120,
      },
    },
    {
      files: ['*.yml', '*.yaml'],
      options: {
        tabWidth: 2,
        singleQuote: false,
      },
    },
  ],
};