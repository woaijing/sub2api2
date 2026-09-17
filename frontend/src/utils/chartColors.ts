// Keep categories distinct; only the leading series carries the brand color.
export const chartSeriesColors = [
  '#d97757', '#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899',
  '#e9b7a5', '#ef4444', '#6366f1', '#84cc16', '#06b6d4', '#80685c'
]

export const chartOtherColor = '#a99489'

export function chartCategoryColors(count: number): string[] {
  return Array.from({ length: count }, (_, index) => chartSeriesColors[index % chartSeriesColors.length])
}
