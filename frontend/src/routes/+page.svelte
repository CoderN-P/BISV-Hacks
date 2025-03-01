<script lang="ts">
    import * as ZXing from '@zxing/library';
    import { Button} from "$lib/components/ui/button";
    import { onMount } from "svelte";
    import { ArrowLeft, Dot } from "lucide-svelte";
    import { Input } from "$lib/components/ui/input";
    import * as Select from "$lib/components/ui/select";
    import { Skeleton } from "$lib/components/ui/skeleton";
    import { Switch } from "$lib/components/ui/switch";

    let barcodeResult = $state(null);
    
    let scannedBarcodes = $state(new Set());
    
    let availableDevices = [];
    
    let selectedDevice = $state(null);
    
    let gptResponse = $state(null);
    
    let started = $state(false);
    
    let foodData = $state(null);

    let invalid_barcode = $state(false);
    
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
                        if (result && !scannedBarcodes.has(result.getText())) {
                            scannedBarcodes.add(result.getText());
                            console.log(scannedBarcodes)
                            barcodeResult = result
                            fetchData();
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
        if (foodData) return;
        
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/items/${barcodeResult}`);
        
        if (res.ok) {
            invalid_barcode = false;
            const data = await res.json();
            foodData = data;
        }else{
            invalid_barcode = true;
            throw new Error("Failed to fetch data")
        }
        
        gptResponse = getGPTResponse();
    }
    
    
    async function getGPTResponse(){
        if (!barcodeResult) return;
        
        const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/summary`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({item: foodData, request_type: "recipe"})
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
            <Switch class="bg-black"/>
        </div>
        
        <p class="text-lg text-gray-600 mt-1">Understand your food. Scan the barcode label to get started!</p>
        {#if invalid_barcode}
            <p class="p-4 text-red-500 mt-1">Invalid barcode!</p>
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
                    {#if gptResponse}
                        <p class="text-2xl font-semibold">Summary</p>
                        <p class="text-base text-gray-500">{gptResponse.description}</p>
                        
                        <p class="text-2xl font-semibold mt-4">Similar products</p>
                        <div class="flex flex-wrap gap-2 mt-4">
                            {#each gptResponse.recommended_products as product}
                                <div class="bg-gray-100 border border-gray-200 rounded-full p-2">
                                    <p class="text-sm">{product}</p>
                                </div>
                            {/each}
                        </div>
                    {:else }
                        <Skeleton class="w-1/2 h-4"/>
                        <Skeleton class="w-2/3 h-4"/>
                        <Skeleton class="w-1/2 h-4"/>
                    {/if}
                </div>
                    
            </div>
            
            {/if}
        
    </div>
</div>
