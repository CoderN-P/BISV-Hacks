<script lang="ts">
    import * as ZXing from '@zxing/library';
    import { Button} from "$lib/components/ui/button";
    import { onMount } from "svelte";
    import * as Select from "$lib/components/ui/select";

    let barcodeResult = $state(null);
    
    let availableDevices = [];
    
    let selectedDevice = $state(null);
    
    let started = $state(false);
    
    let foodData = $state(null);
    
    
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
                    codeReader.decodeFromVideoDevice(selectedDevice.id, 'video', (result, err) => {
                        if (result) {
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
            const data = await res.json();
            foodData = data;
        }
    }
                
   
</script>

<div class="w-screen h-screen">
    <div class="max-w-xl mx-auto flex flex-col h-full">
        <p class="font-semibold text-5xl  mt-8">Foodlyze</p>
        <p class="text-lg text-gray-600 mt-1">Understand your food. Scan the barcode label to get started!</p>

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
                
                <Button variant="primary" class="bg-black text-white" id="startButton">Start Scanning</Button>
            </div>
    
            <div class="flex justify-center mt-4 items-center">
                <video id="video"  class="rounded-lg w-full"></video>
            </div>
        {:else}
            <div class="flex flex-col gap-4 mt-8">
                <p class="text-lg font-semibold">Food Details</p>
                <div class="flex flex-row gap-2">
                    <img src={foodData.image_url} alt="food" class="rounded-lg"/>
                    <div class="flex flex-col gap-2">
                        <p class="text-xl font-semibold">{foodData.product_name}</p>
                        
                        <p class="text-sm font-semibold">Calories: {foodData.calories}</p>
                        <p class="text-sm font-semibold">Fat: {foodData.fat}</p>
                        <p class="text-sm font-semibold">Carbs: {foodData.carbs}</p>
                        <p class="text-sm font-semibold">Protein: {foodData.protein}</p>
                    </div>
                </div>
            </div>
            {/if}
        
    </div>
</div>
