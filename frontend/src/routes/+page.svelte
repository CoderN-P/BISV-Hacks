<script lang="ts">
    import * as ZXing from '@zxing/library';
    import { Button} from "$lib/components/ui/button";
    import { onMount } from "svelte";
    import { ArrowLeft, Dot } from "lucide-svelte";
    import { Input } from "$lib/components/ui/input";
    import * as Select from "$lib/components/ui/select";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { Switch } from "$lib/components/ui/switch";
	import { get } from 'svelte/store';
	import { LOG } from '@zxing/library/esm/core/datamatrix/encoder/constants';

    let barcodeResult: any | null = $state(null);
    
    let invalidBarcodes = $state(new Set());
    
    let availableDevices = [];
    
    let selectedDevice = $state(null);
    
    let gptResponse = $state(null);
    
    let started = $state(false);
    
    let foodData = $state(null);

    let invalid_barcode = $state(false);

    let productFound = $state(false);

    let gptSummary = $state(null);
    let gptRecipe = $state(null);
    let gptResponses: boolean = $state(false);
    
    function delay(ms: number) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    
    onMount(() => {
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
                    console.log(started)
                    codeReader.decodeFromVideoDevice(selectedDevice.id, 'video', (result, err) => {
                        if(result != null){
                            console.log(result)
                        }
                        if (result && !invalidBarcodes.has(result.getText())) {
                            console.log(invalidBarcodes)
                            barcodeResult = result
                            try {
                                fetchData();
                            } catch (e) {
                                console.error(e)
                                invalidBarcodes.add(result.getText());
                            }
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
    });

    
    function onSelectedChange(event) {
        console.log(event)
        selectedDevice = {
            id: event.value,
            label: event.label
        };
    }
    
    
    async function fetchData() {
        if (!barcodeResult) return;
        if (foodData != null) return;
        
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/items/${barcodeResult}`);
        
        if (res.ok) {
            invalid_barcode = false;
            const data = await res.json();
            foodData = data;
        }else{
            invalid_barcode = true;
            throw new Error("Failed to fetch data")
        }
        productFound = true;
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
            return data
        } else {
            throw new Error("Failed to fetch data")
        }
    }
                
    $effect(() => {
        if (productFound) {
            fetchGPTResponses();
        }
    });

    async function fetchGPTResponses() {
        gptSummary = await getGPTResponse("summary");
        gptRecipe = await getGPTResponse("recipe");
        gptResponses = true;
    }
</script>
<div class="w-screen h-screen">
    <div class="max-w-xl px-4 mx-auto mb-4 flex flex-col h-full">
        <div class="flex gap-2 flex-row items-center justify-between mt-8">
            <div class="flex flex-row gap-2 items-center">
                <img src="/images/foodlyze-high-resolution-logo.png" class="rounded-full h-10 w-10"/>
                <p class="font-semibold text-5xl">Foodlyze</p>
            </div>
            <Switch class="bg-black"/>
        </div>
        
        <p class="text-lg text-gray-600 mt-1">Understand your food. Scan the barcode label to get started!</p>
        {#if invalid_barcode}
            <div class="flex flex-row items-center gap-2 mt-4">
                <p class="text-lg text-red-500">Invalid barcode. Please try again.</p>
            </div>
        {/if}
        {#if !foodData}
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
                <div class="flex flex-row w-full justify-center">
                    <Button variant="primary" class="hover:bg-gray-800 bg-black text-white rounded-full" id="startButton">Start Scanning</Button>
                </div>
                
            </div>

            {#if started}
                <div class="flex justify-center mt-4 items-center">
                    <video id="video"  class="rounded-lg w-full"></video>
                </div>
            {/if}
            
            <div class="flex flex-col gap-2 mt-8">
                <p class="text-2xl font-semibold">What is it?</p>
                <p class="text-base text-gray-500">
                Foodlyze is an AI-powered app that scans barcodes to analyze food ingredients, providing a healthiness score and an easy-to-understand explanation. By making food transparency accessible to all, Foodlyze empowers individuals, especially those in low-income communities, to make healthier, more informed choices about their diet.
                </p>
                
                <p class="text-2xl font-semibold mt-4">How does it work?</p>
                <p class="text-base text-gray-500">
                    Click the "Start Scanning" button to begin scanning the barcode of a food item. Once the barcode is scanned, Foodlyze will provide you with information about the food item, including its name, ingredients, and nutritional information. If you would like to learn more about the food item, click the "View Source" link to view the product on Open Food Facts.
                </p>
            </div>
        {:else}
            <button on:click={() => foodData = null} class="flex flex-row items-center gap-2 mt-4">
                <ArrowLeft class="text-green-500 h-4 w-4"/>
                <p class="text-lg text-green-500 hover:underline hover:text-green-600">Return Home</p>
            </button>
            <div class="flex flex-col gap-1 mt-8">
                <div class="flex flex-row justify-between w-full items-center">
                    <div class="flex flex-col gap-1">
                        <p class="text-3xl font-semibold">{foodData.product_name}</p>
                        <div class="flex flex-row gap-2 items-center">
                            <p class="text-lg text-gray-500">{foodData.code}</p> 
                            <Dot class="w-6 text-gray-500 h-6"/>
                            <a href={foodData.url} class="text-lg text-blue-500 hover:underline hover:text-blue-600">View Source</a>
                        </div>
                    </div>
                    <img src={foodData.image_url} alt="food" class="rounded-lg w-24 h-24"/>
                </div>
               <!--- <img src={foodData.image_url} alt="food" class="rounded-lg"/> -->
                
                <div class="flex flex-col gap-2 mt-4">
                    <div class="flex flex-row gap-4">
                        <p><span class="text-5xl font-bold">{foodData.kcal}</span> <span class="text-3xl font-semibold">kcal</span></p>
                    </div>
                </div>
                
                <div class="w-full mt-4 flex flex-col">
                    {#if gptResponses}
                        <p class="text-2xl font-semibold">Summary</p>
                        <p class="text-base text-gray-500">{gptSummary?.description}</p>
                        
                        <p class="text-2xl font-semibold mt-4">Similar products</p>
                        <div class="flex flex-wrap gap-2 mt-4">
                            {#each gptSummary?.recommended_products as product}
                                <div class="bg-gray-100 border border-gray-200 rounded-full p-2">
                                    <p class="text-sm">{product}</p>
                                </div>
                            {/each}
                        </div>
                        <p class="text-2xl font-semibold mt-4">Recipe</p>
                        <p class="text-base text-gray-500">{gptRecipe?.description}</p>

                        <div class="flex flex-col gap-2 mt-4">
                            <p class="text-xl font-semibold">Ingredients</p>
                            <ul class="list-disc list-inside">
                                {#each gptRecipe?.recommended_products as ingredient}
                                    <li>{ingredient}</li>
                                {/each}
                            </ul>
                        </div>
                    
                    {/if}
                </div>
                    
            </div>
            
            {/if}
        
    </div>
</div>
