<script lang="ts">
	import { Navbar, NavBrand } from 'flowbite-svelte';
</script>

<svelte:head>
	<title>Appointments :: XPTO Clinic</title>
	<meta name="description" content="Appointments page" />
</svelte:head>

<Navbar fluid slot="header">
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>XPTO Clinic</span
		>
	</NavBrand>
</Navbar>
<h1>Your appointments</h1>
