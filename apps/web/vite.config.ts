import adapter from '@sveltejs/adapter-static';
import { sveltekit } from '@sveltejs/kit/vite';
import { readFileSync } from 'node:fs';
import { defineConfig } from 'vite';

const pkg = JSON.parse(readFileSync(new URL('./package.json', import.meta.url), 'utf8')) as {
	version: string;
};

export default defineConfig({
	define: {
		__APP_VERSION__: JSON.stringify(pkg.version)
	},
	plugins: [
		sveltekit({
			// Single-page app: Caddy serves index.html for every path.
			adapter: adapter({ fallback: 'index.html', strict: true })
		})
	],
	server: {
		// In development /api goes to the API container (docker compose up -d db mailpit api).
		proxy: { '/api': process.env['API_URL'] ?? 'http://localhost:8000' }
	}
});
