<script lang="ts">
	import { getHealth, type Health } from '#lib/api/client.ts';

	let health = $state<Health | null>(null);
	let failure = $state<string | null>(null);

	async function load(): Promise<void> {
		try {
			health = await getHealth();
			failure = null;
		} catch (error) {
			failure = error instanceof Error ? error.message : String(error);
		}
	}

	$effect(() => {
		void load();
	});

	const today = new Intl.DateTimeFormat('uk-UA', {
		day: 'numeric',
		month: 'long',
		year: 'numeric'
	}).format(new Date());

	type Row = { part: string; value: string; ok: boolean | null };

	let rows = $derived<Row[]>([
		{ part: 'Сайт', value: __APP_VERSION__, ok: true },
		{
			part: 'API',
			value: health ? health.version : (failure ?? 'перевіряю…'),
			ok: health ? true : failure ? false : null
		},
		{
			part: 'Рушій розрахунків',
			value: health?.engine['engine'] ?? '—',
			ok: health ? true : null
		},
		{
			part: 'База PostgreSQL',
			value: health?.database.postgres ?? health?.database.error ?? '—',
			ok: health ? health.database.status === 'ok' : null
		},
		{
			part: 'PostGIS',
			value: health?.database.postgis ?? '—',
			ok: health ? health.database.postgis !== null : null
		}
	]);
</script>

<svelte:head>
	<title>AllinFarm</title>
</svelte:head>

<header>
	<span class="brand">AllinFarm</span>
	<span class="meta">{today}</span>
</header>

<main>
	<h1>Каркас працює</h1>
	<p class="lead">
		Це порожня оболонка системи: сайт, API, рушій і база запущені й бачать одне одного. Розділи
		з'являтимуться крок за кроком.
	</p>

	<table>
		<thead>
			<tr>
				<th scope="col">Частина</th>
				<th scope="col">Стан</th>
				<th scope="col" class="num">Версія</th>
			</tr>
		</thead>
		<tbody>
			{#each rows as row (row.part)}
				<tr>
					<td>{row.part}</td>
					<td class:bad={row.ok === false} class:wait={row.ok === null}>
						{row.ok === null ? 'перевіряю' : row.ok ? 'працює' : 'помилка'}
					</td>
					<td class="num">{row.value}</td>
				</tr>
			{/each}
		</tbody>
	</table>
</main>

<style>
	header {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		padding: 16px 24px;
		border-bottom: 1px solid var(--rule);
	}

	.brand {
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.meta {
		color: var(--muted);
	}

	main {
		max-width: 640px;
		margin: 0 auto;
		padding: 48px 24px;
	}

	h1 {
		font-family: 'Source Serif 4', Georgia, serif;
		font-weight: 600;
		font-size: 32px;
		line-height: 40px;
		margin: 0 0 8px;
	}

	.lead {
		color: var(--muted);
		margin: 0 0 32px;
	}

	table {
		width: 100%;
		border-collapse: collapse;
	}

	th {
		text-align: left;
		font-weight: 400;
		color: var(--muted);
		border-bottom: 1px solid var(--fg);
		padding: 4px 0;
	}

	td {
		padding: 8px 0;
		border-bottom: 1px solid var(--rule);
	}

	.num {
		text-align: right;
	}

	.bad {
		color: var(--irzha);
	}

	.wait {
		color: var(--muted);
	}
</style>
