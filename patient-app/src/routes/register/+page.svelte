<script lang="ts">
	import { Checkbox, Label, Input, Button, Navbar, NavBrand } from 'flowbite-svelte';
    import lodash from 'lodash';

    const { isNil } = lodash;

	let termsAccepted = false;
    let username: string;
    let password: string;
    let confirmPassword: string;
    let email: string;
    let phoneNumber: string;

    $: disableSubmit = isNil(username) || isNil(password) || isNil(confirmPassword) || isNil(email) || isNil(phoneNumber) || !termsAccepted || !passwordsMatch;
    $: passwordsMatch = password === confirmPassword;

</script>

<Navbar fluid>
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white"
			>XPTO Clinic</span
		>
	</NavBrand>
</Navbar>
<div class="flex items-center justify-center">
	<form class="flex flex-col space-y-4">
		<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Create an account</h3>
		<Label class="space-y-2">
			<span>Your username</span>
			<Input type="text" name="username" placeholder="Username" required bind:value={username} />
		</Label>
		<div class="flex space-x-3">
			<Label class="space-y-2">
				<span>Your password</span>
				<Input type="password" name="password" placeholder="•••••" required bind:value={password} />
			</Label>
			<Label class="space-y-2">
				<span>Confirm password</span>
				<Input type="password" name="confirm-password" placeholder="•••••" required bind:value={confirmPassword} />
			</Label>
		</div>
        {#if !passwordsMatch}
            <p class="text-sm font-light text-red-500 dark:text-red-400">Passwords do not match</p>
        {/if}
		<div class="flex space-x-3">
			<Label class="space-y-2">
				<span>Your email</span>
				<Input type="email" name="email" placeholder="name@company.com" required bind:value={email} />
			</Label>
			<Label class="space-y-2">
				<span>Your phone number</span>
				<Input type="text" name="phone-number" placeholder="+351 911 911 911" required bind:value={phoneNumber} />
			</Label>
		</div>
		<div class="flex items-start">
			<Checkbox bind:checked={termsAccepted}>
				I accept the <a
					class="font-medium text-primary-600 hover:underline dark:text-primary-500"
					href="/"
				>
					Terms and Conditions</a
				></Checkbox
			>
		</div>
		<Button type="submit" class="w-full1" bind:disabled={disableSubmit}>Create an account</Button>
		<div class="text-sm font-medium text-gray-500 dark:text-gray-300">
			Already have an account? <a
				href="/login"
				class="font-medium text-primary-600 hover:underline dark:text-primary-500">Login here</a
			>
		</div>
	</form>
</div>
