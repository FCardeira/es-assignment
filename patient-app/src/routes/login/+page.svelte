<script lang="ts">
	import {
		Navbar,
		NavBrand,
		Label,
		Input,
		Button
	} from 'flowbite-svelte';
  import lodash from 'lodash';

  const { isNil } = lodash;

  let username: string;
  let password: string;

  $: disableSubmit = isNil(username) || isNil(password);
</script>

<Navbar fluid>
	<NavBrand href="/">
		<span class="self-center whitespace-nowrap text-xl font-semibold dark:text-white">XPTO Clinic</span
		>
	</NavBrand>
</Navbar>
<div class="flex h-full flex-col items-center justify-center">
	<div class="space-y-4 p-6 sm:p-8 md:space-y-6">
		<form class="flex flex-col space-y-6">
			<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Log-in</h3>
			<Label class="space-y-2">
				<span>Your username</span>
				<Input type="text" name="username" placeholder="Username" required bind:value={username} />
			</Label>
			<Label class="space-y-2">
				<span>Your password</span>
				<Input type="password" name="password" placeholder="•••••" required bind:value={password} />
			</Label>
			<Button type="submit" class="w-full1" bind:disabled={disableSubmit}>Sign in</Button>
			<p class="text-sm font-light text-gray-500 dark:text-gray-400">
				Don't have an account yet? <a
					href="/register"
					class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</a
				>
			</p>
		</form>
	</div>
</div>
