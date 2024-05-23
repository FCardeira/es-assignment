<script lang="ts">
	import AuthenticatedHeader from '../../../components/authenticatedHeader.svelte';
	import { Button, StepIndicator, Spinner } from 'flowbite-svelte';
	import { ArrowRightOutline } from 'flowbite-svelte-icons';
	import Step1 from './step1.svelte';
	import Step2 from './step2.svelte';
	import Step3 from './step3.svelte';
	import Step4 from './step4.svelte';
	import type FormData from './CreateAppointment';
	import { scheduleAppointment, getAppointment, payAppointment } from '../../../services/appointments';
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { addAlert } from '../../../components/alerts/store';

	onMount(async () => {
		loadingStep = true;
		const pay = $page.url.searchParams.get('pay');
		if (pay) {
			currentStep = 3;
			currentAppointmentId = Number(pay);
			$page.url.searchParams.delete('pay');
			const appointment = await getAppointment(currentAppointmentId);
			if (appointment) {
				formData = {
					date: appointment.date,
					doctor: appointment.doctor,
					speciality: appointment.speciality,
					time: appointment.time
				};
			}
		}
		loadingStep = false;
	})


	let loadingStep = false;
	let currentStep = 1;
	let canContinue = true;
	let steps = [
		'Step 1 - Appointment details',
		'Step 2 - Choose a slot',
		'Step 3 - Payment',
		'Step 4 - Confirmation'
	];
	let currentAppointmentId: number = 0;
	let loading = false;

	// Date, Doctor, Specialization, Slot

	async function onClickNextStep(event: Event) {
		event.preventDefault();
		if (
			currentStep == 2 &&
			canContinue &&
			formData.date &&
			formData.doctor &&
			formData.time &&
			formData.speciality
		) {
			try {
				loading = true;
				const newAppointment = await scheduleAppointment({
					doctor: formData.doctor,
					date: formData.date,
					time: formData.time,
					speciality: formData.speciality
				});
				if (newAppointment) {
					currentAppointmentId = newAppointment.appointment_id;
				}
				currentStep++;
			} catch (error) {
				console.error(error);
			} finally {
				loading = false;
			}
		} else {
			currentStep++;
		}
	}

	function onClickPreviousStep(event: Event) {
		event.preventDefault();
		currentStep--;
	}

	async function onGoToStep(event: CustomEvent<number>) {
		if(event.detail === 4) {
			try {
				loadingStep = true;
				await payAppointment(currentAppointmentId);
				loadingStep = false;
				currentStep = 4;
			} catch (error) {
				addAlert({
					color: 'red',
					message: 'Error paying appointment'
				});
			}
		} else {
			currentStep = event.detail;
		}
	}

	$: stepComponent = (() => {
		switch (currentStep) {
			case 1:
				return Step1;
			case 2:
				return Step2;
			case 3:
				return Step3;
			case 4:
				return Step4;
			default:
				return Step1;
		}
	})();

	let formData: FormData;

	function handleFormData(event: CustomEvent<FormData>) {
		formData = { ...event.detail };
	}

	function handleCanContinue(event: CustomEvent<boolean>) {
		canContinue = event.detail;
	}

	$: disableNextButton = !canContinue;
	$: disablePreviousButton = currentStep === 1;
	$: hideNavigationButtons = currentStep === 4 || currentStep === 3;
</script>

<AuthenticatedHeader hideNewApponintmentButton />
<div class="mt-10 flex flex-col items-center space-y-10">
	<div class="flex w-full justify-center px-20">
		<StepIndicator class="grow" {currentStep} {steps} glow />
	</div>
	{#if loadingStep}
		<Spinner />
	{:else}
	<svelte:component
		this={stepComponent}
		bind:formData
		on:formchange={handleFormData}
		on:canContinue={handleCanContinue}
		on:goToStep={onGoToStep}
	/>
	{#if !hideNavigationButtons}
		<div class="flex space-x-3">
			<!--             <Button outline on:click={onClickPreviousStep} disabled={disablePreviousButton}
                ><ArrowLeftOutline class="me-2 h-5 w-5" /> Back</Button
            > -->
			{#if loading}
				<Button><Spinner class="me-3" size="4" color="white" />Loading ...</Button>
			{:else}
				<Button on:click={onClickNextStep} disabled={disableNextButton}
					>Next step <ArrowRightOutline class="ms-2 h-5 w-5" /></Button
				>
			{/if}
		</div>
	{/if}
	{/if}
</div>
