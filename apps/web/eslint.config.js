import js from '@eslint/js';
import svelte from 'eslint-plugin-svelte';
import globals from 'globals';
import ts from 'typescript-eslint';

export default ts.config(
	{ ignores: ['.svelte-kit/', 'build/', 'node_modules/'] },
	js.configs.recommended,
	...ts.configs.strict,
	...svelte.configs.recommended,
	{
		languageOptions: {
			globals: { ...globals.browser, ...globals.node, __APP_VERSION__: 'readonly' }
		}
	},
	{
		files: ['**/*.svelte', '**/*.svelte.ts', '**/*.svelte.js'],
		languageOptions: {
			parserOptions: {
				projectService: true,
				extraFileExtensions: ['.svelte'],
				parser: ts.parser
			}
		}
	},
	{
		// ADR 0003: the site talks to the network only through src/lib/api/.
		files: ['src/**/*.{ts,js,svelte}'],
		ignores: ['src/lib/api/**'],
		rules: {
			'no-restricted-globals': [
				'error',
				{
					name: 'fetch',
					message: 'Use the API client in src/lib/api/ (ADR 0003).'
				},
				{
					name: 'XMLHttpRequest',
					message: 'Use the API client in src/lib/api/ (ADR 0003).'
				},
				{
					name: 'WebSocket',
					message: 'Use the API client in src/lib/api/ (ADR 0003).'
				}
			]
		}
	}
);
