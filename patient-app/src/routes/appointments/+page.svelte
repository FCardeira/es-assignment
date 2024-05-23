<script lang="ts">
	import { Table, TableHead, TableHeadCell, TableBody, TableBodyCell, TableBodyRow } from 'flowbite-svelte';
	import AuthenticatedHeader from '../../components/authenticatedHeader.svelte';

	let appointments = [
		{
			date: '2021-10-01',
			time: '10:00',
			speciality: 'Cardiology',
			doctor: 'Dr. John Doe',
			status: 'Scheduled'
		},
		{
			date: '2021-10-02',
			time: '11:00',
			speciality: 'Dermatology',
			doctor: 'Dr. Jane Doe',
			status: 'Pending payment'
		},
		{
			date: '2021-10-03',
			time: '12:00',
			speciality: 'Neurology',
			doctor: 'Dr. John Doe',
			status: 'Paid'
		}
	];

</script>

<svelte:head>
	<title>Appointments :: XPTO Clinic</title>
	<meta name="description" content="Appointments page" />
</svelte:head>

<AuthenticatedHeader />
<div class="flex m-4 justify-center dark:text-white">
	<h1>Appointments</h1>
</div>
<div class="flex mx-4 justify-center">
	<Table shadow>
		<TableHead>
			<TableHeadCell>Date</TableHeadCell>
			<TableHeadCell>Time</TableHeadCell>
			<TableHeadCell>Speciality</TableHeadCell>
			<TableHeadCell>Doctor</TableHeadCell>
			<TableHeadCell>Payment</TableHeadCell>
		</TableHead>
		<TableBody tableBodyClass="divide-y">
			{#each appointments as appointment}
			<TableBodyRow>
				<TableBodyCell>{appointment.date}</TableBodyCell>
				<TableBodyCell>{appointment.time}</TableBodyCell>
				<TableBodyCell>{appointment.speciality}</TableBodyCell>
				<TableBodyCell>{appointment.doctor}</TableBodyCell>
				<TableBodyCell>{appointment.status}</TableBodyCell>
			</TableBodyRow>
			{/each}
		</TableBody>
	</Table>
</div>
