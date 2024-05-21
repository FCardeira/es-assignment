<script lang="ts">
	import { Button } from 'flowbite-svelte';
	import type CreateAppointment from './CreateAppointment';
	import { AppleSolid } from 'flowbite-svelte-icons';
	import { createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

    function pay() {
        dispatch('goToStep', 4);
    }

	export let formData: CreateAppointment;
</script>

<div class="flex h-full flex-col items-center">
	<form class="flex flex-col space-y-4">
		<h3 class="p-0 text-xl font-medium text-gray-900 dark:text-white">Choose a payment method</h3>
		<div class="flex flex-col space-y-3">
            <Button color="light" on:click={pay}>
                <img src="/icons/mastercard.svg" class="me-2 h-5 w-8" alt="Visa" />
                Checkout with MasterCard
            </Button>
            <Button color="light" on:click={pay}>
                <img src="/icons/visa.svg" class="me-2 h-5 w-8" alt="Visa" />
                Checkout with Visa
            </Button>
            <Button color="light" on:click={pay}>
                <img src="/icons/mbway.svg" class="me-2 h-5 w-8 text-white" alt="MBway" />
                Checkout with MBWay
            </Button>
            <Button on:click={pay} color="dark" class="text-gray-900 bg-[#F7BE38] dark:bg-[#F7BE38] dark:hover:bg-[#F7BE38]/90 hover:bg-[#F7BE38]/90 focus:ring-4 focus:outline-none focus:ring-[#F7BE38]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-[#F7BE38]/50">
                <img src="/icons/paypal.svg" class="me-2 h-5 w-5" alt="PayPal" />
                Check out with PayPal
            </Button>
            <Button on:click={pay} color="dark" class="text-white bg-[#050708] hover:bg-[#050708]/80 focus:ring-4 focus:outline-none focus:ring-[#050708]/50 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:bg-black dark:hover:bg-[#050708]/40 dark:focus:ring-gray-600">
                <AppleSolid class="me-2 h-5 w-5" />
                Check out with Apple Pay
            </Button>
        </div>
	</form>
</div>
