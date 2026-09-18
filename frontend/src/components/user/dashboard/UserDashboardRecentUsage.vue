<template>
  <section class="console-recent">
    <header class="console-recent-heading">
      <h2>{{ t('dashboard.recentUsage') }}</h2>
      <span>{{ t('dashboard.last7Days') }}</span>
    </header>
    <div v-if="loading" class="console-recent-loading"><LoadingSpinner size="lg" /></div>
    <div v-else-if="data.length === 0" class="console-recent-empty">
      <EmptyState :title="t('dashboard.noUsageRecords')" :description="t('dashboard.startUsingApi')" />
    </div>
    <template v-else>
      <ol class="console-request-list">
        <li v-for="log in data" :key="log.id" class="console-request">
          <div class="console-request-model">
            <Icon name="beaker" size="md" />
            <div>
              <p>{{ log.model }}</p>
              <time :datetime="log.created_at">{{ formatDateTime(log.created_at) }}</time>
            </div>
          </div>
          <div class="console-request-tokens">
            <span>{{ (log.input_tokens + log.output_tokens).toLocaleString() }}</span>
            <span class="console-request-label">tokens</span>
          </div>
          <div class="console-request-cost">
            <div><span class="console-request-label">{{ t('dashboard.actual') }}</span><span class="console-actual">${{ formatCost(log.actual_cost) }}</span></div>
            <div><span class="console-request-label">{{ t('dashboard.standard') }}</span><span class="console-standard">${{ formatCost(log.total_cost) }}</span></div>
          </div>
        </li>
      </ol>
      <router-link to="/usage" class="console-view-all">{{ t('dashboard.viewAllUsage') }}<Icon name="arrowRight" size="sm" /></router-link>
    </template>
  </section>
</template>

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'
import EmptyState from '@/components/common/EmptyState.vue'
import Icon from '@/components/icons/Icon.vue'
import { formatDateTime } from '@/utils/format'
import type { UsageLog } from '@/types'

defineProps<{
  data: UsageLog[]
  loading: boolean
}>()
const { t } = useI18n()
const formatCost = (c: number) => c.toFixed(4)
</script>

<style scoped>
.console-recent { min-width: 0; padding-top: 20px; }
.console-recent-heading { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 12px; }
.console-recent-heading h2 { font-size: 14px; font-weight: 600; }
.console-recent-heading > span { font-size: 12px; color: var(--console-muted); }
.console-recent-loading { display: flex; justify-content: center; padding: 48px 0; }
.console-recent-empty { padding: 24px 0; }
.console-request-list { border-top: 1px solid var(--console-line); }
.console-request { display: grid; grid-template-columns: minmax(0, 1.6fr) minmax(100px, .5fr) minmax(180px, .65fr); gap: 20px; align-items: center; padding: 14px 12px; border-bottom: 1px solid var(--console-line); font-variant-numeric: tabular-nums; }
.console-request:hover { background: var(--console-surface); }
.console-request-model { display: flex; align-items: center; gap: 12px; min-width: 0; }
.console-request-model > :deep(svg) { flex-shrink: 0; color: var(--console-muted); }
.console-request-model > div { min-width: 0; }
.console-request-model p { font-size: 13px; font-weight: 500; overflow-wrap: anywhere; }
.console-request-model time { display: block; margin-top: 4px; font-size: 11px; color: var(--console-muted); }
.console-request-tokens { display: flex; align-items: baseline; justify-content: flex-end; flex-wrap: wrap; gap: 5px; font-size: 13px; overflow-wrap: anywhere; min-width: 0; }
.console-request-label { font-size: 11px; color: var(--console-muted); }
.console-request-cost { display: flex; flex-direction: column; gap: 3px; min-width: 0; }
.console-request-cost > div { display: flex; justify-content: flex-end; align-items: baseline; gap: 12px; font-size: 13px; }
.console-request-cost > div > span:last-child { min-width: 88px; text-align: right; overflow-wrap: anywhere; }
.console-actual { color: var(--console-amber); font-weight: 600; }
.console-standard { color: var(--console-muted); }
.console-view-all { display: flex; align-items: center; justify-content: flex-end; gap: 8px; min-height: 44px; padding-top: 8px; font-size: 12px; font-weight: 500; color: var(--console-accent); }
.console-view-all:focus-visible { outline: 2px solid var(--console-accent); outline-offset: 2px; }
@media (max-width: 640px) {
  .console-request { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 8px 12px; padding: 14px 0; }
  .console-request-model { grid-column: 1 / -1; align-items: flex-start; }
  .console-request-model > :deep(svg) { margin-top: 2px; }
  .console-request-tokens { justify-content: flex-start; padding-left: 32px; }
  .console-request-cost > div { gap: 6px; }
  .console-request-cost > div > span:last-child { min-width: 0; }
}
</style>
