<script lang="ts">
	import {
		Table,
		TableHead,
		TableHeadCell,
		TableBody,
		TableBodyCell,
		TableBodyRow,
		Spinner,
		Button
	} from 'flowbite-svelte';
	import AuthenticatedHeader from '../../components/authenticatedHeader.svelte';
	import { onMount } from 'svelte';
	import { getUserAppointments, type Appointment } from '../../services/appointments';
	import { CreditCardOutline } from 'flowbite-svelte-icons';
	import { goto } from '$app/navigation';

	let appointments: Appointment[] = [];
	let loading = false;

	function goToPayment(appointmentId: number) {
		console.log('Go to payment', appointmentId);
		goto(`/appointments/create?pay=${appointmentId}`);
	}

	onMount(async () => {
		console.log('Appointments page mounted');
		loading = true;
		appointments = await getUserAppointments();
		loading = false;
	});
</script>

<svelte:head>
	<title>Appointments :: XPTO Clinic</title>
	<meta name="description" content="Appointments page" />
</svelte:head>

<AuthenticatedHeader />
<div class="m-4 flex justify-center dark:text-white">
	<h1>Your Appointments</h1>
</div>
<div class="mx-4 flex justify-center">
	{#if loading}
		<Spinner />
	{:else if appointments.length === 0}
		<p class="dark:text-white">No appointments found</p>
	{:else}
		<Table shadow>
			<TableHead>
				<TableHeadCell>Date</TableHeadCell>
				<TableHeadCell>Time</TableHeadCell>
				<TableHeadCell>Speciality</TableHeadCell>
				<TableHeadCell>Doctor</TableHeadCell>
				<TableHeadCell>Status</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each appointments as appointment}
					<TableBodyRow>
						<TableBodyCell>{appointment.date}</TableBodyCell>
						<TableBodyCell>{appointment.time}</TableBodyCell>
						<TableBodyCell>{appointment.speciality}</TableBodyCell>
						<TableBodyCell>{appointment.doctor}</TableBodyCell>
						{#if appointment.state == 'Waiting for payment'}
							<TableBodyCell tdClass="flex items-center space-x-2 m-2"
								><span>{appointment.state}</span>
								<Button class="!p-2" on:click={() => goToPayment(appointment.appointment_id)}
									><CreditCardOutline class="h-6 w-6" /></Button
								>
							</TableBodyCell>
						{:else}
							<TableBodyCell>{appointment.state}</TableBodyCell>
						{/if}
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	{/if}
</div>
