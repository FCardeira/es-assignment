<script lang="ts">
    import { Navbar, NavBrand, NavHamburger, NavUl, NavLi, Button, DarkMode } from 'flowbite-svelte';
    import { CalendarEditOutline } from 'flowbite-svelte-icons';
    import { page } from '$app/stores';

    $: activeUrl = $page.url.pathname;

	export let hideNewApponintmentButton = false;
</script>

<Navbar fluid slot="header">
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>XPTO Clinic</span
		>
	</NavBrand>
	<div class="flex md:order-2 space-x-2">
		<NavHamburger />
		{#if !hideNewApponintmentButton}
		<Button pill size="xs" class="my-2" href="/appointments/create">
			<CalendarEditOutline />
			<span class="ml-2">New appointment</span>
		</Button>
		{/if}
		<DarkMode />
	</div>
	<NavUl {activeUrl} class="order-1 justify-end">
		<NavLi href="/">Appointments</NavLi>
		<NavLi href="/account">Account</NavLi>
	</NavUl>
</Navbar>