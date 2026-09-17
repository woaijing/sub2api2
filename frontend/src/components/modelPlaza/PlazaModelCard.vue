<template>
  <article class="plaza-model-card min-w-0 rounded-lg border border-ui-line bg-ui-surface p-5 shadow-sm transition-shadow hover:shadow-md">
    <header class="flex min-h-12 items-start gap-3">
      <span class="model-mark mt-0.5 text-ui-ink" aria-hidden="true">
        <ModelIcon :model="entry.category.iconModel" size="24px" />
      </span>
      <div class="min-w-0 flex-1">
        <h2 class="break-words text-sm font-semibold leading-5 text-ui-ink [overflow-wrap:anywhere]">{{ entry.name }}</h2>
        <p class="mt-1 text-xs text-ui-ink-muted">{{ entry.category.label }}</p>
      </div>
      <span class="max-w-24 shrink-0 rounded bg-ui-brand-soft px-2 py-1 text-center text-xs font-medium text-ui-brand-strong">
        {{ billingLabel }}
      </span>
    </header>

    <div class="mb-3 mt-4 flex flex-wrap justify-between gap-1 text-xs text-ui-ink-muted">
      <span>{{ t('modelPlaza.catalog.basePrice') }}</span>
      <span>{{ unit }}</span>
    </div>
    <dl class="min-h-28 space-y-2.5 text-sm">
      <div v-for="row in priceRows" :key="row.field" class="grid grid-cols-[minmax(0,1fr)_minmax(0,1.5fr)] gap-2">
        <dt class="text-ui-ink-muted">{{ row.label }}</dt>
        <dd class="break-words text-right font-semibold tabular-nums text-ui-ink">{{ basePriceRange(entry, row.field) }}</dd>
      </div>
    </dl>
    <p v-if="entry.offers.some(offer => !offer.model.pricing)" class="mt-2 text-xs text-ui-ink-muted">
      {{ t('modelPlaza.catalog.partialPricing') }}
    </p>

    <div class="mt-4 border-t border-ui-line pt-3">
      <button
        type="button"
        class="flex min-h-8 w-full items-center justify-between gap-3 rounded text-left text-sm font-medium text-ui-brand-strong focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-brand"
        :aria-expanded="expanded"
        :aria-controls="groupsId"
        @click="expanded = !expanded"
      >
        <span>{{ t('modelPlaza.catalog.viewGroups', { count: groupCount }) }}</span>
        <Icon name="chevronDown" size="sm" class="shrink-0 transition-transform" :class="{ 'rotate-180': expanded }" />
      </button>
      <ul v-if="expanded" :id="groupsId" class="mt-2 divide-y divide-ui-line">
        <li v-for="offer in entry.offers" :key="offer.key" class="py-3 last:pb-0">
          <div class="flex items-start gap-2 text-sm">
            <span class="min-w-0 flex-1 break-words font-medium text-ui-ink [overflow-wrap:anywhere]">{{ offer.group.name }}</span>
            <span class="shrink-0 font-mono text-ui-brand-strong">
              <del v-if="hasPersonalRate(offer)" class="mr-1 text-xs text-ui-ink-muted">{{ offer.group.rate_multiplier }}x</del>
              {{ offerRate(offer) }}x
            </span>
          </div>
          <div class="mt-1.5 flex flex-wrap items-center gap-x-2 gap-y-1 text-xs text-ui-ink-muted">
            <span v-if="offer.group.is_exclusive">{{ t('modelPlaza.badges.exclusive') }}</span>
            <span v-if="offer.group.subscription_type === 'subscription'">{{ t('modelPlaza.badges.subscription') }}</span>
            <span v-if="isIndependentImage(offer)">{{ t('modelPlaza.catalog.imageRate') }}</span>
            <button type="button" class="ml-auto inline-flex items-center gap-1 rounded py-1 text-ui-brand-strong hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-brand" @click="$emit('details', offer)">
              {{ t('modelPlaza.catalog.priceDetails') }}
              <Icon name="chevronRight" size="xs" />
            </button>
          </div>
        </li>
      </ul>
    </div>
  </article>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
import ModelIcon from '@/components/common/ModelIcon.vue'
import { basePriceRange, offerRate, type PlazaCatalogEntry, type PlazaOffer, type PlazaPriceField } from './catalog'

const props = defineProps<{ entry: PlazaCatalogEntry }>()
defineEmits<{ details: [offer: PlazaOffer] }>()
const { t } = useI18n()
const expanded = ref(false)
const groupsId = computed(() => 'plaza-groups-' + encodeURIComponent(props.entry.key))
const groupCount = computed(() => new Set(props.entry.offers.map(offer => offer.group.id)).size)
const billingLabel = computed(() => props.entry.billingMode === 'token'
  ? t('modelPlaza.catalog.perToken')
  : t(props.entry.billingMode === 'image' ? 'modelPlaza.table.perImage' : 'modelPlaza.table.perRequest'))
const unit = computed(() => props.entry.billingMode === 'token'
  ? t('modelPlaza.table.unitPerMillion')
  : `$ ${t(props.entry.billingMode === 'image' ? 'modelPlaza.table.perUnitImage' : 'modelPlaza.table.perUnitRequest')}`)
const priceRows = computed<{ field: PlazaPriceField; label: string }[]>(() => {
  if (props.entry.billingMode !== 'token') return [{ field: 'per_request_price', label: t('modelPlaza.catalog.unitPrice') }]
  const rows: { field: PlazaPriceField; label: string }[] = [
    { field: 'input_price', label: t('modelPlaza.table.input') },
    { field: 'output_price', label: t('modelPlaza.table.output') },
    { field: 'cache_write_price', label: t('modelPlaza.catalog.cacheWrite') },
    { field: 'cache_read_price', label: t('modelPlaza.catalog.cacheRead') }
  ]
  if (basePriceRange(props.entry, 'cache_write_1h_price') !== '-') {
    rows.splice(3, 0, { field: 'cache_write_1h_price', label: t('modelPlaza.catalog.cacheWrite1h') })
  }
  return rows
})
const isIndependentImage = (offer: PlazaOffer) => offer.model.pricing?.billing_mode === 'image' && offer.group.image_rate_independent
const hasPersonalRate = (offer: PlazaOffer) => !isIndependentImage(offer) && offer.group.user_rate_multiplier != null && offer.group.user_rate_multiplier !== offer.group.rate_multiplier
</script>

<style scoped>
.model-mark :deep(path) { fill: currentColor; }
.model-mark :deep(.model-icon-fallback) { background: rgb(var(--ui-brand-soft)); color: rgb(var(--ui-brand-strong)); }
</style>
