<script lang="ts">
	import {
		Label,
		Input,
		Button
	} from 'flowbite-svelte';
  import lodash from 'lodash';
  import BasicHeader from '../../components/basicHeader.svelte';
  import { type AxiosResponse } from 'axios';
  import axios from '../../boot/axios';
  import { addAlert } from '../../components/alerts/store';
  import { goto } from '$app/navigation';
  import { saveToken } from '$lib/auth';

  const { isNil } = lodash;

  let username: string;
  let password: string;

  $: disableSubmit = isNil(username) || isNil(password);

  async function signIn(event: Event) {
	event.preventDefault();
	if (disableSubmit) return;
	try {
		const response = await axios.post<{ username: string, password: string}, AxiosResponse<{ token: string }>>('/auth/login', { username, password })
		addAlert({
			color: 'green',
			message: 'Logged in successfully.'
		});
		saveToken(response.data.token);
		goto('/appointments');
	} catch (e) {
		addAlert({
			color: 'red',
			message: 'An error occurred while trying to log in. Please try again later.'
		});
	}
  }

</script>

<svelte:head>
	<title>Login :: XPTO Clinic</title>
	<meta name="description" content="Login page" />
</svelte:head>

<BasicHeader />
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
			<Button class="w-full1" bind:disabled={disableSubmit} on:click={signIn}>Sign in</Button>
			<p class="text-sm font-light text-gray-500 dark:text-gray-400">
				Don't have an account yet? <a
					href="/register"
					class="font-medium text-primary-600 hover:underline dark:text-primary-500">Sign up</a
				>
			</p>
		</form>
	</div>
</div>
