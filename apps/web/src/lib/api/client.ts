/**
 * The only place in the site that talks to the network.
 * ESLint forbids `fetch` everywhere else (ADR 0003).
 */

export interface DatabaseHealth {
	status: 'ok' | 'error';
	postgres: string | null;
	postgis: string | null;
	error: string | null;
}

export interface Health {
	status: 'ok' | 'degraded';
	version: string;
	engine: Record<string, string>;
	database: DatabaseHealth;
}

export class ApiError extends Error {
	constructor(
		message: string,
		readonly status: number
	) {
		super(message);
		this.name = 'ApiError';
	}
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
	const response = await fetch(`/api${path}`, {
		...init,
		headers: { Accept: 'application/json', ...init?.headers }
	});
	const body: unknown = await response.json().catch(() => null);
	if (!response.ok && response.status !== 503) {
		throw new ApiError(`API ${path}: ${response.status}`, response.status);
	}
	return body as T;
}

export function getHealth(): Promise<Health> {
	return request<Health>('/health');
}
