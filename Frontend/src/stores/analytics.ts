import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiService } from '@/services/api'
import type { DefectTrendsResponse, MachinePerformanceResponse, DefectDistributionResponse, AnalyticsFilters } from '@/index'

export const useAnalyticsStore = defineStore('analytics', () => {
  const defectTrends = ref<DefectTrendsResponse | null>(null)
  const machinePerformance = ref<MachinePerformanceResponse | null>(null)
  const defectDistribution = ref<DefectDistributionResponse | null>(null)
  
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const filters = ref<AnalyticsFilters>({
    grouping: 'day',
    startDate: null,
    endDate: null,
    machineId: null,
  })
  
  const machineIds = computed(() => {
    if (!machinePerformance.value) return []
    return machinePerformance.value.machines.map(m => m.machine_id)
  })

  async function fetchDefectTrends() {
    try {
      loading.value = true
      error.value = null
      
      const params: any = {
        grouping: filters.value.grouping,
      }
      if (filters.value.startDate) params.start_date = filters.value.startDate
      if (filters.value.endDate) params.end_date = filters.value.endDate
      if (filters.value.machineId) params.machine_id = filters.value.machineId
      
      defectTrends.value = await apiService.getDefectTrends(params)
    } catch (e) {
      error.value = 'Failed to fetch defect trends'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchMachinePerformance() {
    try {
      loading.value = true
      error.value = null
      
      const params: any = {}
      if (filters.value.startDate) params.start_date = filters.value.startDate
      if (filters.value.endDate) params.end_date = filters.value.endDate
      
      machinePerformance.value = await apiService.getMachinePerformance(params)
    } catch (e) {
      error.value = 'Failed to fetch machine performance'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchDefectDistribution() {
    try {
      loading.value = true
      error.value = null
      
      const params: any = {}
      if (filters.value.startDate) params.start_date = filters.value.startDate
      if (filters.value.endDate) params.end_date = filters.value.endDate
      if (filters.value.machineId) params.machine_id = filters.value.machineId
      
      defectDistribution.value = await apiService.getDefectDistribution(params)
    } catch (e) {
      error.value = 'Failed to fetch defect distribution'
      console.error(e)
    } finally {
      loading.value = false
    }
  }

  async function fetchAllAnalytics() {
    await Promise.all([
      fetchDefectTrends(),
      fetchMachinePerformance(),
      fetchDefectDistribution(),
    ])
  }

  function updateFilters(newFilters: Partial<AnalyticsFilters>) {
    filters.value = { ...filters.value, ...newFilters }
  }

  function resetFilters() {
    filters.value = {
      grouping: 'day',
      startDate: null,
      endDate: null,
      machineId: null,
    }
  }

  return {
    defectTrends,
    machinePerformance,
    defectDistribution,
    loading,
    error,
    filters,
    
    machineIds,
    
    fetchDefectTrends,
    fetchMachinePerformance,
    fetchDefectDistribution,
    fetchAllAnalytics,
    updateFilters,
    resetFilters,
  }
})