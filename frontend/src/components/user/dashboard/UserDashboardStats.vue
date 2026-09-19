<template>
  <section class="console-stats" :aria-label="t('dashboard.title')">
    <div v-if="section !== 'platforms'" class="console-lead-grid" :class="{ 'console-lead-grid--simple': isSimple }">
      <div v-if="!isSimple" class="console-metric console-metric--balance">
        <p class="console-label">{{ t('dashboard.balance') }} <span>USD</span></p>
        <p class="console-value">${{ formatBalance(balance) }}</p>
        <div class="console-metric-foot">
          <span>{{ t('dashboard.recentTotal') }} / {{ t('dashboard.actual') }}</span>
          <strong>${{ formatCost(stats?.total_actual_cost || 0) }}</strong>
          <span>{{ t('dashboard.standard') }} ${{ formatCost(stats?.total_cost || 0) }}</span>
        </div>
      </div>
      <div class="console-metric console-metric--total">
        <p class="console-label">{{ t('dashboard.recentTokens') }}</p>
        <p class="console-value">{{ formatTokens(stats?.total_tokens || 0) }} <small>tokens</small></p>
        <dl class="console-token-split">
          <div><dt>{{ t('dashboard.input') }}</dt><dd>{{ formatTokens(stats?.total_input_tokens || 0) }}</dd></div>
          <div><dt>{{ t('dashboard.output') }}</dt><dd>{{ formatTokens(stats?.total_output_tokens || 0) }}</dd></div>
          <div><dt>{{ t('dashboard.cache') }}</dt><dd>{{ formatTokens((stats?.total_cache_creation_tokens || 0) + (stats?.total_cache_read_tokens || 0)) }}</dd></div>
        </dl>
      </div>
      <slot name="actions" />
    </div>

    <div v-if="section !== 'platforms'" class="console-stat-strip" :class="{ 'console-stat-strip--models': $slots.models }">
      <div class="console-metric console-metric--tokens">
        <p class="console-label">{{ t('dashboard.todayTokens') }}</p>
        <p class="console-value">{{ formatTokens(stats?.today_tokens || 0) }}</p>
        <div class="console-metric-foot">
          <span>{{ t('dashboard.input') }} {{ formatTokens(stats?.today_input_tokens || 0) }} / {{ t('dashboard.output') }} {{ formatTokens(stats?.today_output_tokens || 0) }}</span>
          <span>{{ t('dashboard.cache') }} {{ formatTokens((stats?.today_cache_creation_tokens || 0) + (stats?.today_cache_read_tokens || 0)) }}</span>
        </div>
      </div>
      <div class="console-metric console-metric--cost">
        <p class="console-label"><Icon name="dollar" size="sm" />{{ t('dashboard.todayCost') }}</p>
        <p class="console-value" :title="t('dashboard.actual')">${{ formatCost(stats?.today_actual_cost || 0) }}</p>
        <div class="console-metric-foot"><span>{{ t('dashboard.standard') }}</span><strong>${{ formatCost(stats?.today_cost || 0) }}</strong></div>
      </div>
      <div class="console-metric">
        <p class="console-label"><Icon name="chart" size="sm" />{{ t('dashboard.todayRequests') }}</p>
        <p class="console-value">{{ stats?.today_requests || 0 }}</p>
        <div class="console-metric-foot"><span>{{ t('dashboard.recentTotal') }}</span><strong>{{ formatNumber(stats?.total_requests || 0) }}</strong></div>
      </div>
      <div class="console-metric">
        <p class="console-label"><Icon name="key" size="sm" />{{ t('dashboard.apiKeys') }}</p>
        <p class="console-value">{{ stats?.total_api_keys || 0 }}</p>
        <div class="console-metric-foot"><span class="console-active">{{ stats?.active_api_keys || 0 }} {{ t('common.active') }}</span></div>
      </div>
      <slot name="models" />
    </div>

    <div v-if="section !== 'platforms'" class="console-telemetry">
      <div class="console-reading">
        <p class="console-label">{{ t('dashboard.performance') }}</p>
        <p class="console-reading-value">{{ formatTokens(stats?.rpm || 0) }} <span>RPM</span> / {{ formatTokens(stats?.tpm || 0) }} <span>TPM</span></p>
      </div>
      <div class="console-reading">
        <p class="console-label">{{ t('dashboard.avgResponse') }}</p>
        <p class="console-reading-value">{{ formatDuration(stats?.average_duration_ms || 0) }}</p>
      </div>
    </div>

    <section v-if="section !== 'summary' && !isSimple && platformCards.length > 0" class="console-platforms">
      <header class="console-section-heading">
        <h2>{{ t('dashboard.last30Days') }}</h2>
        <span>{{ t('dashboard.platformCount', { count: platformCards.length }) }}</span>
      </header>
      <div class="console-platform-grid">
        <article v-for="item in platformCards" :key="item.platform" class="console-platform">
          <header class="console-platform-heading">
            <span class="console-platform-name">
              <PlatformIcon :platform="item.platform as GroupPlatform" size="lg" />
              <span>{{ platformLabel(item.platform) }}</span>
            </span>
            <span class="console-spend" :title="t('dashboard.actual')">${{ formatCost(item.total_actual_cost) }}</span>
          </header>
          <dl class="console-platform-ledger">
            <div><dt>{{ t('dashboard.todayCost') }}</dt><dd>${{ formatCost(item.today_actual_cost) }}</dd></div>
            <div><dt>{{ t('dashboard.requests') }}</dt><dd>{{ item.total_requests > 0 ? formatNumber(item.total_requests) : '-' }}</dd></div>
            <div><dt>{{ t('dashboard.tokens') }}</dt><dd>{{ item.total_tokens > 0 ? formatTokens(item.total_tokens) : '-' }}</dd></div>
          </dl>
          <div v-if="hasAnyLimit(item.quota)" class="console-quota">
            <p class="console-label">{{ t('dashboard.platformQuota.title') }}</p>
            <template v-for="w in (['daily', 'weekly', 'monthly'] as const)" :key="w">
              <div v-if="quotaVal(item.quota, `${w}_limit_usd`) != null" class="console-quota-window">
                <template v-if="(quotaVal(item.quota, `${w}_limit_usd`) as number) === 0">
                  <div class="console-quota-label"><span>{{ t(`dashboard.platformQuota.${w}`) }}</span><span class="console-disabled">{{ t('dashboard.platformQuota.disabled') }}</span></div>
                  <div class="console-quota-track"><div class="console-quota-fill bg-red-500" style="width: 100%" /></div>
                </template>
                <template v-else>
                  <div class="console-quota-label">
                    <span>{{ t(`dashboard.platformQuota.${w}`) }}</span>
                    <span>${{ formatUsd((quotaVal(item.quota, `${w}_usage_usd`) as number) ?? 0) }} / ${{ formatUsd(quotaVal(item.quota, `${w}_limit_usd`) as number) }}</span>
                  </div>
                  <div class="console-quota-track">
                    <div class="console-quota-fill"
                      :class="quotaBarClass(calcPercent((quotaVal(item.quota, `${w}_usage_usd`) as number) ?? 0, quotaVal(item.quota, `${w}_limit_usd`) as number))"
                      :style="{ width: calcPercent((quotaVal(item.quota, `${w}_usage_usd`) as number) ?? 0, quotaVal(item.quota, `${w}_limit_usd`) as number) + '%' }" />
                  </div>
                  <p v-if="quotaVal(item.quota, `${w}_window_resets_at`)" class="console-reset">{{ t('dashboard.platformQuota.resetsAt', { time: formatResetTime(quotaVal(item.quota, `${w}_window_resets_at`) as string) }) }}</p>
                </template>
              </div>
            </template>
          </div>
        </article>
      </div>
    </section>
    <p v-else-if="section === 'platforms' && !isSimple" class="console-platform-empty">{{ t('dashboard.platformBreakdownEmpty') }}</p>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
import PlatformIcon from '@/components/common/PlatformIcon.vue'
import type { UserDashboardStats as UserStatsType } from '@/api/usage'
import type { PlatformQuotaItem, GroupPlatform } from '@/types'

interface FusedPlatformCard {
  platform: string
  total_actual_cost: number
  today_actual_cost: number
  total_requests: number
  total_tokens: number
  quota?: PlatformQuotaItem
}

const props = defineProps<{
  stats: UserStatsType
  balance: number
  isSimple: boolean
  platformQuotas?: PlatformQuotaItem[] | null
  section?: 'summary' | 'platforms'
}>()
const { t } = useI18n()

const PLATFORM_LABELS: Record<string, string> = {
  anthropic: 'Claude',
  openai: 'OpenAI',
  gemini: 'Gemini',
  antigravity: 'Antigravity',
  grok: 'Grok',
  kimi: 'Kimi',
  zhipu: 'Zhipu GLM',
  deepseek: 'DeepSeek',
  minimax: 'MiniMax',
}

const platformLabel = (p: string) => PLATFORM_LABELS[p] ?? p

const platformCards = computed<FusedPlatformCard[]>(() => {
  // 建立 by_platform Map
  const byPlat = new Map<string, NonNullable<UserStatsType['by_platform']>[number]>()
  for (const item of props.stats?.by_platform ?? []) byPlat.set(item.platform, item)

  // 建立 quota Map
  const byQuota = new Map<string, PlatformQuotaItem>()
  for (const q of props.platformQuotas ?? []) byQuota.set(q.platform, q)

  // Platform windows can differ from totals. Never synthesize spend from their difference.
  const platforms = new Set<string>([...byPlat.keys(), ...byQuota.keys()])

  const PLATFORM_ORDER = ['anthropic', 'openai', 'gemini', 'antigravity', 'grok']
  const cards: FusedPlatformCard[] = []

  for (const p of platforms) {
    const stat = byPlat.get(p)
    cards.push({
      platform: p,
      total_actual_cost: stat?.total_actual_cost ?? 0,
      today_actual_cost: stat?.today_actual_cost ?? 0,
      total_requests: stat?.total_requests ?? 0,
      total_tokens: stat?.total_tokens ?? 0,
      quota: byQuota.get(p),
    })
  }

  // 排序：按 PLATFORM_ORDER，未知平台按名称排序
  cards.sort((a, b) => {
    const ai = PLATFORM_ORDER.indexOf(a.platform)
    const bi = PLATFORM_ORDER.indexOf(b.platform)
    if (ai === -1 && bi === -1) return a.platform.localeCompare(b.platform)
    if (ai === -1) return 1
    if (bi === -1) return -1
    return ai - bi
  })

  return cards
})

// Quota helpers

type QuotaWindow = 'daily' | 'weekly' | 'monthly'
type QuotaField = `${QuotaWindow}_limit_usd` | `${QuotaWindow}_usage_usd` | `${QuotaWindow}_window_resets_at`

function quotaVal(q: PlatformQuotaItem | undefined, key: QuotaField): PlatformQuotaItem[QuotaField] {
  return q?.[key]
}

function hasAnyLimit(q: PlatformQuotaItem | undefined): boolean {
  if (!q) return false
  return q.daily_limit_usd != null || q.weekly_limit_usd != null || q.monthly_limit_usd != null
}

function calcPercent(usage: number, limit: number): number {
  if (!limit || limit <= 0) return 0
  return Math.min(100, Math.max(0, Math.round((usage / limit) * 100)))
}

function quotaBarClass(p: number): string {
  if (p >= 95) return 'bg-red-500'
  if (p >= 75) return 'bg-amber-500'
  return 'bg-green-500'
}

// 与 formatBalance 一致使用 Intl.NumberFormat 做半偶舍入，避免 toFixed 在不同 JS 引擎
// 下偶发截断而非四舍五入（与后端展示精度不一致）。
const usdFormatter = new Intl.NumberFormat('en-US', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})
function formatUsd(n: number): string {
  if (!Number.isFinite(n)) return '0.00'
  return usdFormatter.format(n)
}

function formatResetTime(iso: string | null | undefined): string {
  if (!iso) return ''
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return d.toLocaleString(undefined, {
    month: 'numeric',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  })
}

const formatBalance = (b: number) =>
  new Intl.NumberFormat('en-US', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(b)

const formatNumber = (n: number) => n.toLocaleString()
const formatCost = (c: number) => c.toFixed(4)
const formatTokens = (t: number) => {
  if (t >= 1_000_000_000) return `${(t / 1_000_000_000).toFixed(2)}B`
  if (t >= 1_000_000) return `${(t / 1_000_000).toFixed(1)}M`
  if (t >= 1000) return `${(t / 1000).toFixed(1)}K`
  return t.toString()
}
const formatDuration = (ms: number) => ms >= 1000 ? `${(ms / 1000).toFixed(2)}s` : `${ms.toFixed(0)}ms`
</script>

<style scoped>
.console-stats { min-width: 0; }
.console-platform-empty { padding: 48px 0; color: var(--console-muted); font-size: 14px; text-align: center; }
.console-stat-strip, .console-telemetry {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-bottom: 1px solid var(--console-line);
}
.console-stat-strip { background: var(--console-surface); border-top: 1px solid var(--console-line); box-shadow: inset 0 1px 0 color-mix(in srgb, var(--console-accent) 12%, transparent); }
.console-stat-strip--simple { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.console-metric, .console-reading { min-width: 0; padding: 20px; }
.console-metric + .console-metric, .console-reading + .console-reading { border-left: 1px solid var(--console-line); }
.console-label { display: flex; align-items: center; gap: 7px; font-size: 12px; font-weight: 500; color: var(--console-muted); }
.console-value { margin: 10px 0 5px; font-size: 28px; line-height: 1.25; font-weight: 650; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.console-metric--balance .console-value, .console-active { color: var(--console-accent); }
.console-metric--cost .console-value, .console-spend { color: var(--console-amber); }
.console-detail { margin-top: 4px; font-size: 12px; line-height: 1.6; color: var(--console-muted); font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.console-detail--wrap { display: flex; flex-wrap: wrap; gap: 0 8px; }
.console-detail.console-active { color: var(--console-accent); }
.console-reading { padding-top: 16px; padding-bottom: 16px; }
.console-reading-value { margin-top: 7px; font-size: 20px; font-weight: 600; font-variant-numeric: tabular-nums; overflow-wrap: anywhere; }
.console-reading-value span { font-size: 11px; color: var(--console-muted); font-weight: 500; }
.console-section-heading { display: flex; justify-content: space-between; align-items: baseline; flex-wrap: wrap; gap: 8px; padding: 20px 0 12px; }
.console-section-heading h2 { font-size: 14px; font-weight: 600; }
.console-section-heading > span { font-size: 12px; color: var(--console-muted); }
.console-platform-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0 24px; }
.console-platform { min-width: 0; padding: 16px 0; border-top: 1px solid var(--console-line); }
.console-platform--other { border-top-style: dashed; }
.console-platform-heading { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; font-size: 13px; font-weight: 600; font-variant-numeric: tabular-nums; }
.console-platform-name { display: inline-flex; align-items: center; gap: 8px; min-width: 0; overflow-wrap: anywhere; }
.console-platform-name :deep(svg) { color: var(--console-text); flex-shrink: 0; }
.console-platform-ledger { margin-top: 12px; }
.console-platform-ledger > div, .console-quota-label { display: flex; align-items: baseline; justify-content: space-between; gap: 8px; font-size: 12px; line-height: 1.6; font-variant-numeric: tabular-nums; }
.console-platform-ledger dt { color: var(--console-muted); }
.console-platform-ledger dd, .console-quota-label > span:last-child { text-align: right; overflow-wrap: anywhere; min-width: 0; }
.console-quota { margin-top: 12px; border-top: 1px solid var(--console-line); padding-top: 10px; }
.console-quota-window { margin-top: 8px; }
.console-quota-track { height: 4px; margin-top: 4px; overflow: hidden; background: var(--console-line); }
.console-quota-fill { height: 100%; }
.console-quota-fill.bg-green-500 { background: var(--console-accent); }
.console-quota-fill.bg-amber-500 { background: var(--console-amber); }
.console-quota-fill.bg-red-500 { background: var(--console-danger); }
.console-disabled { color: var(--console-danger); }
.console-reset { margin-top: 4px; font-size: 11px; color: var(--console-muted); }
@media (max-width: 1100px) {
  .console-platform-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .console-metric, .console-reading { padding: 16px 12px; }
}
@media (max-width: 640px) {
  .console-stat-strip, .console-stat-strip--simple, .console-telemetry { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .console-metric:nth-child(odd), .console-reading:nth-child(odd) { border-left: 0; }
  .console-metric:nth-child(n+3), .console-reading:nth-child(n+3) { border-top: 1px solid var(--console-line); }
  .console-value { font-size: 24px; }
  .console-platform-grid { gap: 0 16px; }
}
@media (max-width: 420px) {
  .console-platform-grid { grid-template-columns: minmax(0, 1fr); }
  .console-platform-ledger { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; }
  .console-platform-ledger > div { display: block; }
  .console-platform-ledger dd { text-align: left; }
}
</style>
