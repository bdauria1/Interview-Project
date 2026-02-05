export type TimeGrouping = 'hour' | 'day' | 'week'

export interface AnalyticsFilters {
  grouping: TimeGrouping
  startDate: string | null
  endDate: string | null
  machineId: string | null
}

export interface ProductInspection {
  id: number
  timestamp: string
  machine_id: string
  reject: boolean
  cycle_time: number
}

export interface ProductInspectionListResponse {
  inspections: ProductInspection[]
  total_count: number
  page: number
  page_size: number
}

export interface DefectTrendPoint {
  timestamp: string
  total_inspections: number
  rejected_inspections: number
  rejection_rate: number
  defect_count: number
}

export interface DefectTrendsResponse {
  trends: DefectTrendPoint[]
  grouping: TimeGrouping
}

export interface MachinePerformance {
  machine_id: string
  total_inspections: number
  rejected_count: number
  rejection_rate: number
  avg_cycle_time: number | null
  avg_injection_pressure: number | null
  avg_barrel_temp: number | null
  alarm_rate: number
}

export interface MachinePerformanceResponse {
  machines: MachinePerformance[]
}

export interface DefectTypeStats {
  defect_type: string
  count: number
  rejection_rate: number
}

export interface DefectDistributionResponse {
  distribution: {
    defect_type: string
    count: number
  }[]
  defect_stats: DefectTypeStats[]
  total_defects: number
}