<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js'
import type { ChartOptions } from 'chart.js'
import type { MachinePerformanceResponse, MachinePerformance } from '@/index'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

interface Props {
  data: MachinePerformanceResponse | null
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
})

const chartKey = ref(0)

const chartData = computed(() => {
  if (!props.data || !props.data.machines.length) {
    return {
      labels: [],
      datasets: [],
    }
  }

  const labels = props.data.machines.map((m: MachinePerformance) => m.machine_id)

  return {
    labels,
    datasets: [
      {
        label: 'Avg Cycle Time (s)',
        data: props.data.machines.map((m: MachinePerformance) => m.avg_cycle_time || 0),
        backgroundColor: 'rgba(239, 68, 68, 0.7)',
      },
      {
        label: 'Avg Injection Pressure (PSI)',
        data: props.data.machines.map((m: MachinePerformance) => (m.avg_injection_pressure || 0) / 100),
        backgroundColor: 'rgba(59, 130, 246, 0.7)',
      },
      {
        label: 'Avg Barrel Temp (°F)',
        data: props.data.machines.map((m: MachinePerformance) => (m.avg_barrel_temp || 0) / 10),
        backgroundColor: 'rgba(16, 185, 129, 0.7)',
      },
    ],
  }
})

const chartOptions: ChartOptions<'bar'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#ffffff',
        font: { size: 11, weight: 'bold' },
        padding: 20
      },
    },
    tooltip: {
      backgroundColor: '#1f2937',
      titleColor: '#10b981',
      bodyColor: '#ffffff',
      borderColor: '#374151',
      borderWidth: 1,
      callbacks: {
        label: function(context) {
          let label = context.dataset.label || ''
          if (label) label += ': '
          if (context.parsed.y !== null) label += context.parsed.y.toFixed(2)
          return label
        }
      }
    }
  },
  scales: {
    x: {
      grid: {
        color: 'rgba(75, 85, 99, 0.2)',
      },
      ticks: {
        color: '#ffffff',
        font: { size: 10 }
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(75, 85, 99, 0.2)',
      },
      ticks: {
        color: '#ffffff',
        font: { size: 10 }
      },
      title: {
        display: true,
        text: 'Value',
        color: '#ffffff',
        font: { size: 12, weight: 'bold' }
      },
    },
  },
}

watch(() => props.data, () => {
  chartKey.value++
}, { deep: true })
</script>

<template>
  <div class="card">
    <h3 class="text-lg font-semibold text-white mb-4">Machine Performance Metrics</h3>
    
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-else-if="!data || !data.machines.length" class="flex items-center justify-center h-64 text-white">
      No data available (Please check if your filters are too restrictive)
    </div>
    
    <div v-else class="h-64">
      <Bar :key="chartKey" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>