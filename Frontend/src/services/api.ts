import axios from 'axios'
import type { ProductInspectionListResponse, ProductInspection, DefectTrendsResponse, MachinePerformanceResponse, DefectDistributionResponse,TimeGrouping } from '@/index'

const API_URL = import.meta.env.VITE_API_URL

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const apiService = {
  async getInspections(params?: {
    page?: number
    page_size?: number
    machine_id?: string
    has_defects?: boolean
  }): Promise<ProductInspectionListResponse> {
    const { data } = await api.get<ProductInspectionListResponse>('/api/inspections', { params })
    return data
  },

  async getInspection(inspectionId: number): Promise<ProductInspection> {
    const { data } = await api.get<ProductInspection>(`/api/inspections/${inspectionId}`)
    return data
  },

  async getMachineInspectionCount(machineId: string): Promise<{ machine_id: string; inspection_count: number }> {
    const { data } = await api.get(`/api/inspections/machine/${machineId}/count`)
    return data
  },

  async getDefectTrends(params?: {
    grouping?: TimeGrouping
    start_date?: string
    end_date?: string
    machine_id?: string
  }): Promise<DefectTrendsResponse> {
    const { data } = await api.get<DefectTrendsResponse>('/api/analytics/defect-trends', { params })
    return data
  },

  async getMachinePerformance(params?: {
    start_date?: string
    end_date?: string
  }): Promise<MachinePerformanceResponse> {
    const { data } = await api.get<MachinePerformanceResponse>('/api/analytics/machine-performance', { params })
    return data
  },

  async getDefectDistribution(params?: {
    start_date?: string
    end_date?: string
    machine_id?: string
  }): Promise<DefectDistributionResponse> {
    const { data} = await api.get<DefectDistributionResponse>('/api/analytics/defect-distribution', { params })
    return data
  }
}

export default api