// See https://svelte.dev/docs/kit/types#app.d.ts
declare global {
	/** Site version from package.json, set at build time. */
	const __APP_VERSION__: string;

	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
