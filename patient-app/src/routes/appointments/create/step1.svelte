<script lang="ts">
	import { Label, Input, Select } from 'flowbite-svelte';
    import type CreateAppointment from './CreateAppointment';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	// Array of physiotherapy specializations
	let specializations = [
		{ name: 'Physiotherapy', value: 'Physiotherapy' },
		{ name: 'Osteopathy', value: 'Osteopathy' },
		{ name: 'Chiropractic', value: 'Chiropractic' },
		{ name: 'Acupuncture', value: 'Acupuncture' },
		{ name: 'Massage Therapy', value: 'Massage Therapy' }
	];

	// Array of doctors
	let doctors = [
		{
			name: 'Dr. John Doe',
			value: 'Dr. John Doe'
		},
		{
			name: 'Dr. Jane Doe',
			value: 'Dr. Jane Doe'
		},
		{
			name: 'Dr. John Smith',
			value: 'Dr. John Smith'
		},
		{
			name: 'Dr. Jane Smith',
			value: 'Dr. Jane Smith'
		},
		{
			name: 'Dr. Rose Tyler',
			value: 'Dr. Rose Tyler'
		},
		{
			name: 'Dr. Martha Jones',
			value: 'Dr. Martha Jones'
		},
		{
			name: 'Dr. Donna Noble',
			value: 'Dr. Donna Noble'
		},
		{
			name: 'Dr. Jack Harkness',
			value: 'Dr. Jack Harkness'
		},
		{
			name: 'Dr. River Song',
			value: 'Dr. River Song'
		},
		{
			name: 'Dr. Clara Oswald',
			value: 'Dr. Clara Oswald'
		},
		{
			name: 'Dr. Who',
			value: 'Dr. Who'
		}
	];

    let selectedDoctor: string;
	let selectedSpecialization: string;

    export let formData: CreateAppointment = {
        date: '',
        doctor: '',
        speciality: ''
    };

	$: {
        if (!formData.date || !formData.doctor || !formData.speciality) {
            dispatch('canContinue', false);
        } else {
			dispatch('canContinue', true);
		}
    }

</script>

<div class="flex h-full flex-col items-center">
	<form class="flex flex-col space-y-4">
		<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Schedule an appointment</h3>
		<Label class="space-y-2">
			<span>Appointment date</span>
			<Input type="date" name="date" placeholder="Date" required bind:value={formData.date} />
		</Label>
		<div class="grid grid-cols-2 gap-3">
			<Label class="space-y-2">
				<span>Doctor</span>
				<Select items={doctors} bind:value={formData.doctor} name="doctor" required />
			</Label>
			<Label class="space-y-2">
				<span>Speciality</span>
				<Select
					items={specializations}
					bind:value={formData.speciality}
					name="specialization"
					required
				/>
			</Label>
		</div>
	</form>
</div>
