<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import type { ChartOptions } from 'chart.js'
import type { DefectTrendsResponse, DefectTrendPoint } from '@/index'
import { format } from 'date-fns'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

interface Props {
  data: DefectTrendsResponse | null
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  loading: false,
})

const chartKey = ref(0)

const chartData = computed(() => {
  if (!props.data || !props.data.trends.length) {
    return {
      labels: [],
      datasets: [],
    }
  }

  const labels = props.data.trends.map((t: DefectTrendPoint) => {
    try {
      const date = new Date(t.timestamp)
      if (isNaN(date.getTime())) {
        return t.timestamp
      }
      if (props.data!.grouping === 'hour') {
        return format(date, 'MMM d, HH:mm')
      } else if (props.data!.grouping === 'week') {
        return format(date, 'MMM d, yyyy')
      } else {
        return format(date, 'MMM d')
      }
    } catch (e) {
      console.error('Date parsing error:', e, t.timestamp)
      return String(t.timestamp)
    }
  })

  return {
    labels,
    datasets: [
      {
        label: 'Total Defects',
        data: props.data.trends.map((t: DefectTrendPoint) => t.defect_count),
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246)',
        tension: 0.3,
        yAxisID: 'y',
      },
    ],
  }
})

const chartOptions: ChartOptions<'line'> = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      labels: { color: '#ffffff', font: { family: 'Inter', size: 11 } }
    },
  },
  scales: {
    y: {
      position: 'right',
      grid: { display: false },
      ticks: { color: '#ffffff' },
      title: { display: true, text: 'Total Defects', color: '#ffffff' }
    },
    x: {
      grid: { color: 'rgba(255, 255, 255, 0.05)' },
      ticks: { color: '#ffffff' }
    }
  }
}

watch(() => props.data, () => {
  chartKey.value++
}, { deep: true })
</script>

<template>
  <div class="card">
    <h3 class="text-lg font-semibold text-white mb-4">Number of Defects Over Time</h3>
    
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>
    
    <div v-else-if="!data || !data.trends.length" class="flex items-center justify-center h-64 text-white">
      No data available (Please check if your filters are too restrictive)
    </div>
    
    <div v-else class="h-64">
      <Line :key="chartKey" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>