<script lang="ts">
	import AuthenticatedHeader from '../../../components/authenticatedHeader.svelte';
	import { Button, StepIndicator } from 'flowbite-svelte';
	import { ArrowRightOutline, ArrowLeftOutline } from 'flowbite-svelte-icons';
	import Step1 from './step1.svelte';
	import Step2 from './step2.svelte';
	import Step3 from './step3.svelte';
	import Step4 from './step4.svelte';
	import type FormData from './CreateAppointment';

	let currentStep = 1;
	let canContinue = true;
	let steps = [
		'Step 1 - Appointment details',
		'Step 2 - Choose a slot',
		'Step 3 - Payment',
		'Step 4 - Confirmation'
	];

	// Date, Doctor, Specialization, Slot

	function onClickNextStep(event: Event) {
		event.preventDefault();
		currentStep++;
	}

	function onClickPreviousStep(event: Event) {
		event.preventDefault();
		currentStep--;
	}

    function onGoToStep(event: CustomEvent<number>) {
        currentStep = event.detail;
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
	<svelte:component
		this={stepComponent}
		bind:formData
		on:formchange={handleFormData}
		on:canContinue={handleCanContinue}
        on:goToStep={onGoToStep}
	/>
    {#if !hideNavigationButtons}
        <div class="flex space-x-3">
            <Button outline on:click={onClickPreviousStep} disabled={disablePreviousButton}
                ><ArrowLeftOutline class="me-2 h-5 w-5" /> Back</Button
            >
            <Button on:click={onClickNextStep} disabled={disableNextButton}
                >Next step <ArrowRightOutline class="ms-2 h-5 w-5" /></Button
            >
        </div>
    {/if}
</div>
