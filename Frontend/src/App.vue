<script setup lang="ts">
import { onMounted } from 'vue'
import { useAnalyticsStore } from '@/stores/analytics'
import DefectTrendChart from '@/components/DefectTrendChart.vue'
import MachinePerformanceChart from '@/components/MachinePerformanceChart.vue'
import DefectDistributionChart from '@/components/DefectDistributionChart.vue'
import FilterControls from '@/components/FilterControls.vue'

const store = useAnalyticsStore()

onMounted(() => {
  store.fetchAllAnalytics()
})

function handleFilterUpdate(newFilters: any) {
  store.updateFilters(newFilters)
}

function handleRefresh() {
  store.fetchAllAnalytics()
}
</script>

<template>
  <div class="min-h-screen bg-[#05070a] text-white selection:bg-emerald-500/30">
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] bg-emerald-900/10 blur-[120px] rounded-full"></div>
      <div class="absolute top-[20%] -right-[10%] w-[30%] h-[30%] bg-blue-900/10 blur-[120px] rounded-full"></div>
    </div>

    <header class="relative z-10 border-b border-green/5 bg-gray-950/50 backdrop-blur-md">
      <div class="max-w-7xl mx-auto px-6 py-8">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-emerald-500 text-[10px] font-bold uppercase tracking-[0.3em] mb-1">Intelligence Layer</p>
            <h1 class="text-4xl font-extrabold tracking-tight">KREVERA</h1>
          </div>
        </div>
      </div>
    </header>

    <main class="relative z-10 max-w-7xl mx-auto px-6 py-10">
      <FilterControls
        :filters="store.filters"
        :machine-ids="store.machineIds"
        @update="handleFilterUpdate"
        @refresh="handleRefresh"
      />

      <div class="space-y-8 mt-10">
        <div class="bg-gray-900/50 border border-green/10 backdrop-blur-md rounded-3xl p-8 shadow-2xl">
           <DefectTrendChart :data="store.defectTrends" :loading="store.loading" />
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="bg-gray-900/40 border border-green/5 backdrop-blur-sm rounded-3xl p-8 shadow-2xl">
            <MachinePerformanceChart :data="store.machinePerformance" :loading="store.loading" />
          </div>
          <div class="bg-gray-900/40 border border-green/5 backdrop-blur-sm rounded-3xl p-8 shadow-2xl">
            <DefectDistributionChart :data="store.defectDistribution" :loading="store.loading" />
          </div>
        </div>
      </div>
    </main>
  </div>
</template>