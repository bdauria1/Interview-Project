<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { Bar } from 'vue-chartjs'
import { Chart as ChartJS, BarElement, CategoryScale, LinearScale, Tooltip, Legend, LineElement, PointElement } from 'chart.js'
import type { ChartOptions } from 'chart.js'
import type { DefectDistributionResponse } from '@/index'

ChartJS.register( BarElement, CategoryScale, LinearScale, LineElement, PointElement, Tooltip, Legend)

interface Props {
  data: DefectDistributionResponse | null
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
})

const chartKey = ref(0)

const barColor = 'rgba(255, 255, 255, 0.1)'
const lineColor = 'rgba(16, 185, 129, 1)'

const paretoData = computed(() => {
  if (!props.data || !props.data.distribution.length) {
    return { labels: [], datasets: [] }
  }

  const sorted = [...props.data.distribution].sort(
    (a, b) => b.count - a.count
  )

  const total = sorted.reduce((sum, d) => sum + d.count, 0)

  let cumulative = 0
  const cumulativePercentages = sorted.map(d => {
    cumulative += d.count
    return +(cumulative / total * 100).toFixed(1)
  })

  return {
    labels: sorted.map(d => d.defect_type),
    datasets: [
      {
        type: 'line' as const,
        label: 'Cumulative %',
        data: cumulativePercentages,
        borderColor: lineColor,
        backgroundColor: lineColor,
        pointRadius: 4,
        tension: 0.3,
        yAxisID: 'y1',
      },
      {
        type: 'bar' as const,
        label: 'Defect Count',
        data: sorted.map(d => d.count),
        backgroundColor: barColor,
        yAxisID: 'y',
      },
    ],
  } as any
})

const chartOptions: ChartOptions<any> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: true,
      position: 'top',
      labels: {
        color: '#ffffff', 
        font: {
          family: 'Inter, sans-serif',
          size: 11,
          weight: 'bold'
        },
        padding: 20,
        usePointStyle: true,
      },
    },
    tooltip: {
      backgroundColor: 'rgba(17, 24, 39, 0.9)',
      titleColor: '#10b981',
      bodyColor: '#ffffff',
      borderColor: 'rgba(255, 255, 255, 0.1)',
      borderWidth: 1,
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(255, 255, 255, 0.05)', 
        drawBorder: false,
      },
      ticks: {
        color: '#ffffff', 
        font: { size: 10 }
      },
      title: {
        display: true,
        text: 'Value',
        color: '#ffffff',
        font: { weight: 'bold', size: 12 }
      },
    },
    y1: {
      position: 'right',
      grid: { drawOnChartArea: false },
      ticks: {
        color: '#ffffff',
        font: { size: 10 }
      },
      title: {
        display: true,
        text: 'Secondary Metric',
        color: '#ffffff',
        font: { weight: 'bold', size: 12 }
      }
    },
    x: {
      grid: { display: false },
      ticks: {
        color: '#ffffff',
        font: { size: 10 },
        maxRotation: 45,
        minRotation: 45,
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
    <h3 class="text-lg font-semibold text-white mb-4">
      Defect Pareto Analysis
    </h3>

    <div v-if="loading" class="flex items-center justify-center h-72">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <div
      v-else-if="!data || !data.distribution.length"
      class="flex items-center justify-center h-72 text-white"
    >
      No defects detected (Please check if your filters are too restrictive)
    </div>

    <div v-else class="h-72">
      <Bar :key="chartKey" :data="paretoData" :options="chartOptions" />
    </div>
  </div>
</template>
