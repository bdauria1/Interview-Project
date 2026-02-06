<script setup lang="ts">
import { ref, watch } from 'vue'
import { VueDatePicker } from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import type { AnalyticsFilters, TimeGrouping } from '@/index'

interface Props {
  filters: AnalyticsFilters
  machineIds: string[]
}

const props = defineProps<Props>()
const emit = defineEmits<{
  update: [filters: Partial<AnalyticsFilters>]
  refresh: []
}>()

const localGrouping = ref<TimeGrouping>(props.filters.grouping)
const localMachineId = ref<string>(props.filters.machineId || '')
const localStartDate = ref(props.filters.startDate || null)
const localEndDate = ref(props.filters.endDate || null)

watch([localGrouping, localMachineId], () => {
  emit('update', { 
    grouping: localGrouping.value, 
    machineId: localMachineId.value || null 
  })
})

function handleDateChange() {
  emit('update', {
    startDate: localStartDate.value ? new Date(localStartDate.value).toISOString() : null,
    endDate: localEndDate.value ? new Date(localEndDate.value).toISOString() : null,
  })
}
</script>

<template>
  <div class="bg-[#0a0e14]/80 border border-white-800 backdrop-blur-md rounded-2xl p-6 mb-8 shadow-2xl">
    
    <div class="flex items-center gap-2 mb-6">
      <div class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
      <h2 class="text-[10px] font-bold uppercase tracking-[0.2em] text-emerald-500/80">
        System Control Panel
      </h2>
    </div>

    <div class="flex flex-col lg:flex-row lg:items-end gap-6">
      <div class="flex-1 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div class="flex flex-col">
          <label class="text-[10px] font-bold uppercase tracking-widest text-white mb-2 ml-1">Interval</label>
          <select v-model="localGrouping" class="unified-input">
            <option value="hour">Hourly</option>
            <option value="day">Daily</option>
            <option value="week">Weekly</option>
          </select>
        </div>

        <div class="flex flex-col">
          <label class="text-[10px] font-bold uppercase tracking-widest text-white mb-2 ml-1">Machine Unit</label>
          <select v-model="localMachineId" class="unified-input">
            <option value="">All Active Units</option>
            <option v-for="id in machineIds" :key="id" :value="id">{{ id }}</option>
          </select>
        </div>

        <div class="flex flex-col">
          <label class="text-[10px] font-bold uppercase tracking-widest text-white mb-2 ml-1">Analysis Start</label>
          <VueDatePicker 
            v-model="localStartDate"
            dark
            teleport="body"
            placeholder="Select Start"
            input-class-name="unified-input-date"
            @update:model-value="handleDateChange"
          />
        </div>

        <div class="flex flex-col">
          <label class="text-[10px] font-bold uppercase tracking-widest text-white mb-2 ml-1">Analysis End</label>
          <VueDatePicker 
            v-model="localEndDate"
            dark
            teleport="body"
            placeholder="Select End"
            input-class-name="unified-input-date"
            @update:model-value="handleDateChange"
          />
        </div>
      </div>

      <div class="flex items-center gap-4">
        <button @click="emit('refresh')" 
                class="inline-flex items-center justify-center px-8 h-[42px] text-[10px] font-bold uppercase tracking-widest text-white bg-[#059669] hover:bg-emerald-500 rounded-lg transition-all active:scale-95 whitespace-nowrap">
          Execute Analysis
        </button>
      </div>
    </div>
  </div>
</template>