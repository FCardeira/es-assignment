<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import type CreateAppointment from './CreateAppointment';
	import { createEventDispatcher } from 'svelte';
	import { onMount } from 'svelte';
	import { getOccupiedTimeSlots, type Slot } from '../../../services/appointments';

	onMount(async () => {
		if(formData.date && formData.doctor) {
			occupiedTimeSlots = await getOccupiedTimeSlots(formData.date.split('-').reverse().join('/'), formData.doctor);
		}
	})

	export let formData: CreateAppointment;

    const dispatch = createEventDispatcher();

	$: timeSlots = Array.from({ length: 32 }, (_, i) => {
		let hour = Math.floor(i / 4) + 9;
		let minute = (i % 4) * 15;
		return `${hour.toString().padStart(2, '0')}:${minute.toString().padStart(2, '0')}`;
	});

	$: occupiedTimeSlots = [] as Slot[];

    $: isTimeSlotSelected = (timeSlot: string) => formData.time == timeSlot;
	$: isTimeSlotOccupied = (timeSlot: string) => occupiedTimeSlots.find((slot) => slot.time === timeSlot);

    function toggleTimeSlot(timeSlot: string) {
        if (formData.time === timeSlot) {
            dispatch('canContinue', false);
            formData.time = '';
        } else {
            formData.time = timeSlot;
            dispatch('canContinue', true);
        }
        dispatch('formchange', { ...formData });
    }

</script>

<div class="flex h-full flex-col items-center">
	<form class="flex flex-col space-y-4">
		<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Choose a time slot below</h3>
		<div class="grid grid-cols-2 gap-3 text-gray-900 dark:text-white">
			<p><span class="font-bold">Doctor:</span> {formData.doctor}</p>
			<p><span class="font-bold">Speciality:</span> {formData.speciality}</p>
			<p><span class="font-bold">Date:</span> {formData.date}</p>
		</div>
		<div class="grid grid-cols-4 gap-3">
			{#each timeSlots as timeSlot}
				{#if isTimeSlotSelected(timeSlot)}
					<Button color="primary" pill on:click={() => toggleTimeSlot(timeSlot)} disabled={isTimeSlotOccupied(timeSlot)}>{timeSlot}</Button>
				{:else}
					<Button color="alternative" pill on:click={() => toggleTimeSlot(timeSlot)} disabled={isTimeSlotOccupied(timeSlot)}>{timeSlot}</Button>
				{/if}
			{/each}
		</div>
	</form>
</div>
