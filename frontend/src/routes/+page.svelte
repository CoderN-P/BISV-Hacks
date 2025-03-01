<script lang="ts">
    import * as ZXing from '@zxing/library';
    import { Button} from "$lib/components/ui/button";
    import { onMount } from "svelte";
    import {ArrowLeft, Dot, Flame, CakeSlice, Box, ArrowUp} from "lucide-svelte";
    import MarkdownRenderer from "$lib/components/markdownRenderer.svelte";
    import { Input } from "$lib/components/ui/input";
    import * as Select from "$lib/components/ui/select";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { Switch } from "$lib/components/ui/switch";

    let barcodeResult: any | null = $state(null);
    
    let availableDevices = [];
    let selectedDevice = $state(null);
    let gptResponse = $state(null);
    let started = $state(false);
    let foodData = $state(null);
    let loadingFoodData = $state(false);
    let foodError = $state(false);
    
    function initializeScanner(){
        const codeReader = new ZXing.BrowserMultiFormatReader();

        codeReader.listVideoInputDevices()
            .then((videoInputDevices) => {
                if (videoInputDevices.length >= 1) {
                    videoInputDevices.forEach((element) => {
                        availableDevices.push({
                            id: element.deviceId,
                            label: element.label
                        })
                    })
                    selectedDevice = availableDevices[0]
                }
                document.getElementById('startButton').addEventListener('click', () => {
                    started = true;
         
                    codeReader.decodeFromVideoDevice(selectedDevice.id, 'video', (result, err) => {
                        if (result) {
                            barcodeResult = result
                            fetchData();
                            codeReader.reset();
                            started = false;
                        }
                        if (err && !(err instanceof ZXing.NotFoundException)) {
                            console.error(err)
                            barcodeResult = err
                        }
                    })
                })
            })
            .catch((err) => {
                console.error(err)
            })
    }
    onMount(() => {
        initializeScanner();
    })
    
    function returnHome() {
        foodData = null;
        gptResponse = null;
        barcodeResult = null;
        foodError = false;
        initializeScanner();
    }

    
    function onSelectedChange(event) {
        selectedDevice = {
            id: event.value,
            label: event.label
        };
    }
    
    
    async function fetchData() {
        if (!barcodeResult) return;
        if (foodData != null) return;
        
        loadingFoodData = true;
        
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/items/${barcodeResult}`);
        
        
        
        if (res.ok) {
            const data = await res.json();
            foodData = data;
            loadingFoodData = false;
            await getGPTResponse();
        }else{
            foodError = true;
            loadingFoodData = false;
        }
    }
    
   
    
    
    async function getGPTResponse(type: string="recipe"){
        if (!barcodeResult) return;
        
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/summary`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({item: foodData, request_type: type})
        });
        
        if (res.ok) {
            const data = await res.json();
            gptResponse = data;
        } else {
            throw new Error("Failed to fetch data")
        }
    }
</script>
<div class="w-screen h-screen">
    <div class="max-w-xl px-4 mx-auto mb-4 flex flex-col h-full">
        <div class="flex gap-2 flex-row items-center justify-between mt-8">
            <div class="flex flex-row gap-2 items-center">
                <img src="/images/foodlyze-high-resolution-logo.png" class="rounded-full h-10 w-10"/>
                <p class="font-semibold text-5xl">Foodlyze</p>
            </div>
            <Switch />
        </div>
        
        
        <p class="text-lg text-gray-600 mt-1">Understand your food. Scan the barcode label to get started!</p>
       
        {#if !foodData && !loadingFoodData && !foodError} 
            <div class="flex flex-row items-center gap-4 mt-8">
                {#if started}
               <Select.Root {onSelectedChange}>
                   <Select.Trigger>
                       <Select.Value placeholder="Select Camera"/>
                   </Select.Trigger>
                   <Select.Content>
                       {#each availableDevices as device}
                            <Select.Item value={device.id}>{device.label}</Select.Item>
                       {/each}
                   </Select.Content>
               </Select.Root>
                  {/if}
             
                    <div class="flex flex-row w-full items-center ">
                        
                        <Button variant="primary" class="hover:bg-gray-800 mr-4 bg-black text-white rounded-full" id="startButton">Start Scanning</Button>
                        {#if !started}
                            <p class="font-medium text-lg mr-4 ">OR</p>
                        <Input bind:value={barcodeResult} placeholder="Enter code" class="w-1/2 mr-2 rounded-full "/>
                            <button on:click={fetchData} disabled={!barcodeResult} class=" rounded-full bg-green-500 flex p-2 items-center">
                                <ArrowUp class="text-white "/>
                            </button>
                        {/if}
                    </div>
            </div>

            {#if started}
                <div class="flex justify-center mt-4 items-center">
                    <video id="video"  class="rounded-lg w-full"></video>
                </div>
            {/if}
            
            <div class="flex flex-col gap-2 mt-8 mb-4">
                <p class="text-2xl font-semibold">What is it?</p>
                <p class="text-base text-gray-500">
                Foodlyze is an AI-powered app that scans barcodes to analyze food ingredients, providing a healthiness score and an easy-to-understand explanation. By making food transparency accessible to all, Foodlyze empowers individuals, especially those in low-income communities, to make healthier, more informed choices about their diet.
                </p>
                
                <p class="text-2xl font-semibold mt-4">How does it work?</p>
                <p class="text-base text-gray-500 mb-8">
                    Click the "Start Scanning" button to begin scanning the barcode of a food item. Once the barcode is scanned, Foodlyze will provide you with information about the food item, including its name, ingredients, and nutritional information. 
                </p>
            </div>
        {:else if loadingFoodData}
            <div class="flex justify-center h-full items-center">
                <div class="w-32 h-32 border-4 border-green-500
                        border-t-transparent rounded-full 
                        animate-spin">
                </div>
            </div>
        {:else if foodError}
            <button on:click={returnHome} class="flex flex-row items-center gap-2 mt-4">
                <ArrowLeft class="text-green-500 h-4 w-4"/>
                <p class="text-lg text-green-500 hover:underline hover:text-green-600">Return Home</p>
            </button>
            <div class="flex justify-center h-full items-center">
                <p class="text-2xl font-semibold text-red-500">Sorry! We couldn't find that</p>
            </div>
        {:else}
            <button on:click={returnHome} class="flex flex-row items-center gap-2 mt-4">
                <ArrowLeft class="text-green-500 h-4 w-4"/>
                <p class="text-lg text-green-500 hover:underline hover:text-green-600">Return Home</p>
            </button>
            <div class="flex flex-col gap-1 mt-8">
                <div class="flex flex-row justify-between w-full items-center">
                    <div class="flex flex-col gap-1">
                        <p class="text-3xl font-semibold">{foodData.product_name}</p>
                        <div class="flex flex-row gap-4 items-center">
                            <p class="text-lg text-gray-500">{foodData.code}</p> 
                            <Dot class="w-6 text-gray-500 h-6"/>
                            {foodData.url}
                            <a href={foodData.url} class="text-lg text-blue-500 hover:underline hover:text-blue-600">View Source</a>
                        </div>
                    </div>
                    <img src={foodData.image_url} alt="food" class="rounded-lg w-20 h-20"/>
                </div>
                
                <div class="flex flex-row mt-4 justify-between rounded-lg border border-gray-100 p-4 items-center">
                    <div class="flex flex-row gap-2 items-center">
                        {#if gptResponse}
                            {#if gptResponse.score < 3}
                                <div class="w-6 h-6 rounded-full bg-red-500"/>
                                
                            {:else if gptResponse.score < 7}
                                <div class="w-6 h-6 rounded-full bg-orange-500"/>
                            {:else}
                                <div class="w-6 rounded-full h-6 bg-green-500"/>
                            {/if}
              
                            <p class="text-lg font-semibold">{gptResponse.score}/10</p>
                        {:else}
                            <Skeleton class="bg-gray-100 w-4 h-4"/>
                        {/if}
                    </div>

                    {#if gptResponse}
                        {#if gptResponse.score < 3}
                            <p class="text-lg text-red-500">Bad</p>
                        {:else if gptResponse.score < 7}
                            <p class="text-lg text-orange-500">Mid</p>
                        {:else}
                            <p class="text-lg text-green-500">healthy</p>
                        {/if}
                    {:else}
                        <Skeleton class="bg-gray-100 w-24 h-4"/>
                    {/if}
                </div>
               <!--- <img src={foodData.image_url} alt="food" class="rounded-lg"/> -->
                
                <div class="flex flex-col  mt-4 rounded-lg border border-gray-100 ">
                    <div class="flex flex-col w-full   p-4 gap-2">
                        <div class="flex flex-row gap-2 items-center justify-between">
                            <div class="flex flex-row gap-2 items-center">
                                <Flame class="w-8 h-8 text-red-500"/>
                                <p class="text-xl font-semibold">Calories</p>
                                {#if gptResponse}
                                    {#if gptResponse.calories.score === "good"}
                                        <p class="text-lg text-green-500">healthy</p>
                                    {:else if gptResponse.calories.score === "bad"}
                                        <p class="text-lg text-red-500">unhealthy</p>
                                    {:else}
                                        <p class="text-lg text-orange-500">mid</p>
                                    {/if}
                                {:else}
                                    <Skeleton class="bg-gray-100 w-16 h-4"/>
                                {/if}
                            </div>
                            <p class="text-xl float-right text-gray-600">{foodData.kcal} kcal</p>
                        </div>
                        {#if gptResponse}
                            <p class="text-sm text-gray-500">{gptResponse.calories.summary}</p>
                        {:else}
                            <Skeleton class="bg-gray-100 w-56 h-4"/>
                        {/if}
                    </div>
                    
                    <div class="flex flex-col w-full p-4 gap-2 border-t border-gray-200 ">
                        <div class="flex flex-row gap-2 items-center justify-between">
                            <div class="flex flex-row gap-2 items-center">
                                <CakeSlice class="w-8 h-8 text-orange-500"/>
                                <p class="text-xl font-semibold"> Fat</p>
                                {#if gptResponse}
                                    {#if gptResponse.fat.score === "good"}
                                        <p class="text-lg text-green-500">healthy</p>
                                    {:else if gptResponse.fat.score === "bad"}
                                        <p class="text-lg text-red-500">unhealthy</p>
                                    {:else}
                                        <p class="text-lg text-orange-500">mid</p>
                                    {/if}
                                {:else}
                                    <Skeleton class="bg-gray-100 w-16 h-4"/>
                                {/if}
                            </div>
                            <p class="text-xl float-right text-gray-600">{foodData.fat_100g} g</p>
                        </div>
                        {#if gptResponse}
                            <p class="text-sm text-gray-500">{gptResponse.fat.summary}</p>
                        {:else}
                            <Skeleton class="bg-gray-100 w-56 h-4"/>
                        {/if}
                    </div>

                    <div class="flex flex-col w-full border-t border-gray-200  p-4 gap-2">
                        <div class="flex flex-row gap-2 items-center justify-between">
                            <div class="flex flex-row gap-2 items-center">
                                <Box class="w-8 h-8 text-blue-500"/>
                                <p class="text-xl font-semibold">Sugar</p>
                                {#if gptResponse}
                                    {#if gptResponse.sugars.score === "good"}
                                        <p class="text-lg text-green-500">healthy</p>
                                    {:else if gptResponse.sugars.score === "bad"}
                                        <p class="text-lg text-red-500">unhealthy</p>
                                    {:else}
                                        <p class="text-lg text-orange-500">mid</p>
                                    {/if}
                                {:else}
                                    <Skeleton class="bg-gray-100 w-16 h-4"/>
                                {/if}
                            </div>
                            <p class="text-xl float-right text-gray-600">{foodData.sugars_100g} g</p>
                        </div>
                        {#if gptResponse}
                            <p class="text-sm text-gray-500">{gptResponse.sugars.summary}</p>
                        {:else}
                            <Skeleton class="bg-gray-100 w-56 h-4"/>
                        {/if}
                    </div>
                </div>
                
                <div class="w-full mt-4 flex flex-col">
                    {#if gptResponse}
                        <p class="text-2xl font-semibold">Summary</p>
                        <MarkdownRenderer md={gptResponse.description}/>
                        
                        <p class="text-2xl font-semibold mt-4">Recommended additions</p>
                        <div class="flex flex-wrap gap-2 mt-4 mb-4">
                            {#each gptResponse.recommended_products as product}
                                <div class="bg-gray-100 border border-gray-200 rounded-full p-2">
                                    <p class="text-sm">{product}</p>
                                </div>
                            {/each}
                        </div>
                    {:else }
                        <Skeleton class="bg-gray-100 mb-1 w-2/3 h-4"/>
                        <Skeleton class="bg-gray-100 mb-1 w-1/2 h-4"/>
                        <Skeleton class="bg-gray-full w-h-4"/>
                    {/if}
                </div>
                    
            </div>
            
            {/if}
        
    </div>
</div>
