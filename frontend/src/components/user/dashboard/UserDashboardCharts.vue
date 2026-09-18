<template>
  <section class="console-charts" data-console-charts>
    <div class="console-chart-toolbar">
      <div class="console-date-control">
        <span>{{ t('dashboard.timeRange') }}</span>
        <DateRangePicker :start-date="startDate" :end-date="endDate" @update:startDate="$emit('update:startDate', $event)" @update:endDate="$emit('update:endDate', $event)" @change="$emit('dateRangeChange', $event)" />
      </div>
      <div class="console-chart-actions">
        <label for="console-dashboard-granularity">{{ t('dashboard.granularity') }}</label>
        <Select id="console-dashboard-granularity" class="console-granularity" :model-value="granularity" :options="[{value:'day', label:t('dashboard.day')}, {value:'hour', label:t('dashboard.hour')}]" @update:model-value="$emit('update:granularity', $event)" @change="$emit('granularityChange')" />
        <button class="console-refresh" :disabled="loading" :title="t('common.refresh')" :aria-label="t('common.refresh')" @click="$emit('refresh')">
          <Icon name="refresh" size="md" />
        </button>
      </div>
    </div>
    <div class="console-chart-grid">
      <div class="console-trend">
        <TokenUsageTrend :trend-data="trend" :loading="loading" :animation-duration="reducedMotion ? 0 : 180" />
      </div>
      <section class="console-distribution" :aria-label="t('dashboard.modelDistribution')">
        <h2>{{ t('dashboard.modelDistribution') }}</h2>
        <div v-if="loading" class="console-chart-overlay"><LoadingSpinner size="md" /></div>
        <div class="console-distribution-body">
          <div class="console-doughnut">
            <Doughnut v-if="modelData" :data="modelData" :options="doughnutOptions" />
            <div v-else class="console-chart-empty">{{ t('dashboard.noDataAvailable') }}</div>
          </div>
          <div class="console-model-table" tabindex="0" :aria-label="t('dashboard.modelDistribution')">
            <table>
              <thead>
                <tr>
                  <th>{{ t('dashboard.model') }}</th>
                  <th>{{ t('dashboard.requests') }}</th>
                  <th>{{ t('dashboard.tokens') }}</th>
                  <th>{{ t('dashboard.actual') }}</th>
                  <th>{{ t('dashboard.standard') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="model in models" :key="model.model">
                  <td class="console-model-name" :title="model.model">{{ model.model }}</td>
                  <td>{{ formatNumber(model.requests) }}</td>
                  <td>{{ formatTokens(model.total_tokens) }}</td>
                  <td class="console-model-cost">${{ formatCost(model.actual_cost) }}</td>
                  <td class="console-model-standard">${{ formatCost(model.cost) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePreferredReducedMotion } from '@vueuse/core'
import { useI18n } from 'vue-i18n'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import DateRangePicker from '@/components/common/DateRangePicker.vue'
import Select from '@/components/common/Select.vue'
import Icon from '@/components/icons/Icon.vue'
import { Doughnut } from 'vue-chartjs'
import TokenUsageTrend from '@/components/charts/TokenUsageTrend.vue'
import { chartCategoryColors } from '@/utils/chartColors'
import type { TrendDataPoint, ModelStat } from '@/types'
import { formatCostFixed as formatCost, formatNumberLocaleString as formatNumber, formatTokensK as formatTokens } from '@/utils/format'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler } from 'chart.js'

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, ArcElement, Title, Tooltip, Legend, Filler)

const props = defineProps<{ loading: boolean, startDate: string, endDate: string, granularity: string, trend: TrendDataPoint[], models: ModelStat[] }>()
defineEmits(['update:startDate', 'update:endDate', 'update:granularity', 'dateRangeChange', 'granularityChange', 'refresh'])
const { t } = useI18n()
const preferredMotion = usePreferredReducedMotion()
const reducedMotion = computed(() => preferredMotion.value === 'reduce')

const modelData = computed(() => !props.models?.length ? null : {
  labels: props.models.map((m: ModelStat) => m.model),
  datasets: [{
    data: props.models.map((m: ModelStat) => m.total_tokens),
    backgroundColor: chartCategoryColors(props.models.length)
  }]
})

const doughnutOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: reducedMotion.value ? 0 : 180 },
  cutout: '72%',
  borderWidth: 2,
  plugins: {
    legend: { display: false },
    tooltip: {
      callbacks: {
        label: (context: any) => `${context.label}: ${formatTokens(context.parsed)} tokens`
      }
    }
  }
}))
</script>

<style scoped>
.console-charts { margin-top: 12px; border-top: 1px solid var(--console-line); }
.console-chart-toolbar { display: flex; align-items: center; justify-content: space-between; gap: 12px; flex-wrap: wrap; padding: 16px 0; }
.console-date-control, .console-chart-actions { display: flex; align-items: center; gap: 10px; min-width: 0; }
.console-date-control > span, .console-chart-actions label { font-size: 12px; color: var(--console-muted); flex-shrink: 0; }
.console-granularity { width: 108px; }
.console-refresh { display: grid; place-items: center; width: 38px; height: 38px; flex-shrink: 0; color: var(--console-muted); border: 1px solid var(--console-line); border-radius: 6px; background: var(--console-surface); }
.console-refresh:hover { color: var(--console-accent); }
.console-refresh:focus-visible { outline: 2px solid var(--console-accent); outline-offset: 3px; }
.console-refresh:disabled { opacity: .45; cursor: wait; }
.console-chart-grid { display: grid; grid-template-columns: minmax(0, 1.15fr) minmax(0, 1fr); gap: 24px; padding-bottom: 24px; border-bottom: 1px solid var(--console-line); }
.console-trend, .console-distribution { min-width: 0; background: var(--console-surface); }
.console-trend :deep(.card) { border: 0; border-radius: 0; box-shadow: none; background: transparent; padding: 16px; }
.console-trend :deep(h3), .console-distribution h2 { margin: 0 0 18px; font-size: 14px; font-weight: 600; color: var(--console-text); }
.console-trend :deep(.h-48) { height: 240px; }
.console-distribution { position: relative; padding: 16px; }
.console-distribution-body { display: flex; flex-direction: column; align-items: center; gap: 14px; }
.console-doughnut { width: 120px; height: 120px; flex-shrink: 0; }
.console-chart-empty { display: grid; place-items: center; height: 100%; font-size: 12px; color: var(--console-muted); text-align: center; }
.console-chart-overlay { position: absolute; inset: 0; z-index: 1; display: grid; place-items: center; background: var(--console-surface); opacity: .85; }
.console-model-table { width: 100%; max-height: 122px; overflow: auto; scrollbar-gutter: stable; }
.console-model-table:focus-visible { outline: 2px solid var(--console-accent); outline-offset: 2px; }
.console-model-table table { width: 100%; font-size: 11px; font-variant-numeric: tabular-nums; }
.console-model-table th { padding: 0 8px 8px; color: var(--console-muted); font-weight: 500; white-space: nowrap; text-align: right; }
.console-model-table th:first-child { text-align: left; padding-left: 0; }
.console-model-table td { border-top: 1px solid var(--console-line); padding: 7px 8px; text-align: right; white-space: nowrap; }
.console-model-table td.console-model-name { max-width: 160px; text-align: left; padding-left: 0; font-weight: 500; overflow: hidden; text-overflow: ellipsis; }
.console-model-cost { color: var(--console-amber); }
.console-model-standard { color: var(--console-muted); }
@media (max-width: 1200px) {
  .console-chart-grid { grid-template-columns: minmax(0, 1fr); gap: 16px; }
  .console-distribution-body { flex-direction: row; gap: 24px; }
  .console-model-table { max-height: 200px; }
}
@media (max-width: 640px) {
  .console-chart-toolbar { align-items: stretch; }
  .console-date-control { width: 100%; flex-wrap: wrap; }
  .console-chart-actions { width: 100%; justify-content: flex-end; }
  .console-chart-grid { gap: 12px; }
  .console-distribution-body { flex-direction: column; gap: 16px; }
  .console-trend :deep(.card), .console-distribution { padding: 14px 10px; }
  .console-trend :deep(.h-48) { height: 250px; }
}
</style>
