<script>
	import '../app.css';
	import Footer from '../components/+footer.svelte';
	import Alerts from '../components/alerts/Alerts.svelte';
	import { goto } from '$app/navigation';
    import { page } from '$app/stores';
	import { isSignedIn } from '$lib/auth';
	import { browser } from '$app/environment';

	$: if (browser && isSignedIn() && $page.url.pathname === '/') {
		goto('/appointments');
	} else if (browser && !isSignedIn() && $page.url.pathname !== '/login' && $page.url.pathname !== '/register' && $page.url.pathname !== '/management') {
		goto('/login');
	}

	export const ssr = false;

</script>

<Alerts />
<div class="flex flex-col h-screen">
<header>
	<slot name="header"></slot>
</header>
<main class="grow">
	<slot></slot>
</main>
<Footer />
</div>

<style></style>
