<script lang="ts">
	import BasicHeader from '../../components/basicHeader.svelte';
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
	import type { Appointment } from '../../services/appointments';
    import { onMount } from 'svelte';
    import { getAppointments, finishAppointment } from '../../services/management';
	import { addAlert } from '../../components/alerts/store';

    onMount(async () => {
        loading = true;
        appointments = await getAppointments();
        loading = false;
    });

	let appointments: Appointment[] = [];
	let loading = false;

    async function onClickFinishAppointment(appointmentId: number) {
        loading = true;
        try {
            await finishAppointment(appointmentId);
            const finishedAppointment = appointments.find(appointment => appointment.appointment_id === appointmentId);
            if (finishedAppointment) {
                finishedAppointment.state = 'Finished';
            }
        } catch (error) {
            addAlert({ message: 'Error finishing appointment', color: 'red' });
        } finally {
            loading = false;
        }
    }

</script>

<svelte:head>
	<title>Management :: XPTO Clinic</title>
	<meta name="description" content="Login page" />
</svelte:head>

<BasicHeader />
<div class="m-4 flex justify-center dark:text-white">
	<h1>Appointments</h1>
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
                <TableHeadCell>Patient</TableHeadCell>
				<TableHeadCell>Status</TableHeadCell>
			</TableHead>
			<TableBody tableBodyClass="divide-y">
				{#each appointments as appointment}
					<TableBodyRow>
						<TableBodyCell>{appointment.date}</TableBodyCell>
						<TableBodyCell>{appointment.time}</TableBodyCell>
						<TableBodyCell>{appointment.speciality}</TableBodyCell>
						<TableBodyCell>{appointment.doctor}</TableBodyCell>
                        <TableBodyCell>{appointment.patient_username}</TableBodyCell>
                        {#if appointment.state == 'Confirmed'}
                            <TableBodyCell tdClass="space-x-2 m-2"><span>Confirmed</span><Button color="primary" on:click={() => onClickFinishAppointment(appointment.appointment_id)}>Finish</Button></TableBodyCell>
                        {:else}
                            <TableBodyCell>{appointment.state}</TableBodyCell>
                        {/if}
					</TableBodyRow>
				{/each}
			</TableBody>
		</Table>
	{/if}
</div>
