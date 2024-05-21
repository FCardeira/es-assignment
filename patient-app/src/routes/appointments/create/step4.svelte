<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import type CreateAppointment from './CreateAppointment';
	import { createEventDispatcher } from 'svelte';
	export let formData: CreateAppointment;

    const dispatch = createEventDispatcher();

    function goToStart() {
        dispatch('formchange', {});
        dispatch('goToStep', 1);
    }


</script>

<div class="flex h-full flex-col items-center">
    <h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Thank you for scheduling your appointment!</h3>
    <p class="text-gray-600 dark:text-gray-400">You will receive a confirmation email shortly.</p>

    <div class="flex flex-col space-y-4 mt-6">
        <h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Appointment details</h3>
        <div class="grid grid-cols-2 gap-3 text-gray-900 dark:text-white">
            <p><span class="font-bold">Doctor:</span> {formData.doctor}</p>
            <p><span class="font-bold">Speciality:</span> {formData.speciality}</p>
            <p><span class="font-bold">Date:</span> {formData.date}</p>
            <p><span class="font-bold">Time:</span> {formData.time}</p>
        </div>

        <div class="flex flex-col space-y-3">
            <Button color="primary" href="/">Go to appointments</Button>
            <Button color="light" on:click={goToStart}>Schedule another appointment</Button>
        </div>
    </div>
</div>
