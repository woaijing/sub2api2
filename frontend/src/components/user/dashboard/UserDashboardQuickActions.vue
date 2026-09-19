<template>
  <nav class="console-actions" :aria-label="t('dashboard.quickActions')">
    <h2 class="console-actions-label">{{ t('dashboard.quickActions') }}</h2>
    <div class="console-actions-list">
      <button @click="router.push('/keys')"><Icon name="key" size="md" /><span>{{ t('dashboard.createApiKey') }}</span><Icon name="arrowRight" size="sm" /></button>
      <button @click="router.push('/infinite-canvas')"><Icon name="grid" size="md" /><span>{{ t('dashboard.infiniteCanvas') }}</span><Icon name="arrowRight" size="sm" /></button>
      <button @click="router.push('/usage')"><Icon name="chart" size="md" /><span>{{ t('dashboard.viewUsage') }}</span><Icon name="arrowRight" size="sm" /></button>
      <button v-if="canUseBatchImage" @click="router.push('/batch-image')"><Icon name="sparkles" size="md" /><span>{{ t('dashboard.batchImageAgent') }}</span><Icon name="arrowRight" size="sm" /></button>
      <button @click="router.push('/redeem')"><Icon name="gift" size="md" /><span>{{ t('dashboard.redeemCode') }}</span><Icon name="arrowRight" size="sm" /></button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
import { useBatchImageAccess } from '@/composables/useBatchImageAccess'
const router = useRouter()
const { t } = useI18n()
const { canUseBatchImage, refreshBatchImageAccess } = useBatchImageAccess()

onMounted(() => {
  void refreshBatchImageAccess()
})
</script>

<style scoped>
.console-actions { display: flex; align-items: center; gap: 18px; padding: 12px 0; min-width: 0; }
.console-actions-label { flex-shrink: 0; font-size: 11px; color: var(--console-muted); }
.console-actions-list { display: flex; flex-wrap: wrap; gap: 4px 8px; min-width: 0; }
.console-actions button { display: inline-flex; align-items: center; justify-content: flex-start; gap: 7px; min-height: 36px; padding: 6px 9px; border-radius: 4px; font-size: 12px; font-weight: 500; color: var(--console-text); text-align: left; }
.console-actions button :deep(svg) { color: var(--console-accent); flex-shrink: 0; }
.console-actions button:hover { background: var(--console-surface); color: var(--console-accent); }
.console-actions button:focus-visible { outline: 2px solid var(--console-accent); outline-offset: 2px; }
@media (max-width: 640px) {
  .console-actions { align-items: flex-start; gap: 8px; padding: 10px 0; }
  .console-actions-label { padding-top: 14px; }
  .console-actions-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); flex: 1; gap: 0 6px; }
  .console-actions button { min-height: 44px; padding: 7px 4px; overflow-wrap: anywhere; }
}
</style>
