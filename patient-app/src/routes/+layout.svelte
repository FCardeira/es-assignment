<script>
	import '../app.css';
	import Footer from '../components/+footer.svelte';
</script>

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
