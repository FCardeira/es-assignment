<script lang="ts">
    import { Navbar, NavBrand, DarkMode } from 'flowbite-svelte';
</script>

<Navbar fluid slot="header">
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>XPTO Clinic</span
		>
	</NavBrand>
    <DarkMode />
</Navbar>