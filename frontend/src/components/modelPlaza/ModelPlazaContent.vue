<template>
  <div class="plaza-content space-y-6 text-ui-ink">
    <header v-if="!embedded">
      <h1 class="text-2xl font-bold">{{ t('modelPlaza.title') }}</h1>
      <p class="mt-2 text-sm text-ui-ink-muted">{{ t('modelPlaza.description') }}</p>
    </header>

    <p v-if="!isAuthenticated" class="text-sm text-ui-ink-muted">{{ t('modelPlaza.anonymousHint') }}</p>

    <section class="border-y border-ui-line py-5" :aria-label="t('modelPlaza.catalog.billingNotes')">
      <h2 class="mb-3 flex items-center gap-2 text-base font-semibold">
        <Icon name="infoCircle" size="md" class="text-ui-brand" />
        {{ t('modelPlaza.catalog.billingNotes') }}
      </h2>
      <p class="text-sm leading-6 text-ui-ink-muted">{{ t('modelPlaza.catalog.pricingNote') }}</p>
      <div v-if="descriptionHtml" class="plaza-description mt-3 text-sm" v-html="descriptionHtml"></div>
    </section>

    <div v-if="loading" role="status" class="flex min-h-60 items-center justify-center gap-3 text-sm text-ui-ink-muted">
      <Icon name="refresh" size="md" class="animate-spin text-ui-brand" />
      {{ t('modelPlaza.loading') }}
    </div>
    <div v-else-if="error" role="alert" class="flex min-h-60 flex-col items-center justify-center gap-4 text-sm text-ui-ink-muted">
      <Icon name="exclamationCircle" size="lg" />
      <p>{{ t('modelPlaza.loadFailed') }}</p>
      <button type="button" class="btn btn-secondary" @click="$emit('retry')">
        <Icon name="refresh" size="sm" />{{ t('modelPlaza.catalog.retry') }}
      </button>
    </div>
    <template v-else>
      <section class="space-y-4" :aria-label="t('modelPlaza.catalog.filters')">
        <div class="flex flex-wrap gap-3">
          <div class="relative w-full sm:mr-auto sm:w-80">
            <Icon name="search" size="sm" class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ui-ink-muted" />
            <input v-model="searchQuery" type="search" class="input pl-10 pr-3" :placeholder="t('modelPlaza.filters.searchPlaceholder')" :aria-label="t('modelPlaza.filters.searchPlaceholder')" />
          </div>
          <select v-model="selectedGroupId" class="input w-full sm:w-48" :aria-label="t('modelPlaza.filters.groupLabel')">
            <option value="all">{{ t('modelPlaza.catalog.allGroups') }}</option>
            <option v-for="group in groups" :key="group.id" :value="group.id">{{ group.name }}</option>
          </select>
          <select v-model="selectedRate" class="input w-full sm:w-36" :aria-label="t('modelPlaza.filters.rateLabel')">
            <option value="all">{{ t('modelPlaza.catalog.allRates') }}</option>
            <option v-for="rate in rates" :key="rate" :value="rate">{{ rate }}x</option>
          </select>
        </div>
        <div class="flex flex-wrap gap-2" role="group" :aria-label="t('modelPlaza.catalog.category')">
          <button type="button" class="category-button" :class="{ active: selectedCategory === 'all' }" :aria-pressed="selectedCategory === 'all'" @click="selectedCategory = 'all'">{{ t('modelPlaza.filters.all') }}</button>
          <button v-for="category in categories" :key="category.id" type="button" class="category-button" :class="{ active: selectedCategory === category.id }" :aria-pressed="selectedCategory === category.id" @click="selectedCategory = category.id">
            <ModelIcon :model="category.iconModel" size="18px" aria-hidden="true" />
            {{ category.label }}
          </button>
        </div>
      </section>

      <div class="flex min-h-6 items-center justify-between gap-4 text-sm text-ui-ink-muted">
        <p aria-live="polite">{{ t('modelPlaza.catalog.modelCount', { count: filteredModels.length }) }}</p>
        <button v-if="filtersActive" type="button" class="inline-flex items-center gap-1 text-ui-brand-strong hover:underline" @click="resetFilters">
          <Icon name="x" size="xs" />{{ t('modelPlaza.catalog.resetFilters') }}
        </button>
      </div>
      <div v-if="filteredModels.length" class="grid items-start gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <PlazaModelCard v-for="entry in filteredModels" :key="entry.key" :entry="entry" @details="offer => selectedDetail = { entryKey: entry.key, offerKey: offer.key }" />
      </div>
      <div v-else class="flex min-h-60 flex-col items-center justify-center gap-3 border-y border-dashed border-ui-line text-sm text-ui-ink-muted">
        <Icon name="search" size="lg" />
        <p>{{ filtersActive ? t('modelPlaza.noSearchResult') : t('modelPlaza.empty') }}</p>
      </div>
    </template>

    <BaseDialog :show="!!detailGroup" :title="t('modelPlaza.catalog.priceDetails')" width="extra-wide" @close="selectedDetail = null">
      <PlazaGroupSection v-if="detailGroup" :group="detailGroup" unframed />
    </BaseDialog>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import Icon from '@/components/icons/Icon.vue'
import ModelIcon from '@/components/common/ModelIcon.vue'
import BaseDialog from '@/components/common/BaseDialog.vue'
import PlazaModelCard from './PlazaModelCard.vue'
import PlazaGroupSection from './PlazaGroupSection.vue'
import { buildModelCatalog, offerRate } from './catalog'
import type { ModelPlazaResponse } from '@/api/modelPlaza'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{ response: ModelPlazaResponse | null; loading: boolean; error?: boolean; embedded?: boolean }>()
defineEmits<{ retry: [] }>()
const { t } = useI18n()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)
const selectedCategory = ref('all')
const selectedGroupId = ref<number | 'all'>('all')
const selectedRate = ref<number | 'all'>('all')
const searchQuery = ref('')
const selectedDetail = ref<{ entryKey: string; offerKey: string } | null>(null)
const groups = computed(() => props.response?.groups ?? [])
const models = computed(() => buildModelCatalog(groups.value))
const categories = computed(() => [...new Map(models.value.map(model => [model.category.id, model.category])).values()])
const rates = computed(() => [...new Set(models.value.flatMap(model => model.offers.map(offerRate)))].sort((a, b) => a - b))
const filtersActive = computed(() => !!searchQuery.value.trim() || selectedCategory.value !== 'all' || selectedGroupId.value !== 'all' || selectedRate.value !== 'all')
const descriptionHtml = computed(() => DOMPurify.sanitize(marked.parse(props.response?.description?.trim() ?? '') as string))

const filteredModels = computed(() => {
  const query = searchQuery.value.trim().toLowerCase()
  return models.value
    .filter(model => (selectedCategory.value === 'all' || model.category.id === selectedCategory.value) && model.name.toLowerCase().includes(query))
    .map(model => ({ ...model, offers: model.offers.filter(offer =>
      (selectedGroupId.value === 'all' || offer.group.id === selectedGroupId.value) &&
      (selectedRate.value === 'all' || offerRate(offer) === selectedRate.value)
    ) }))
    .filter(model => model.offers.length)
})

const detailOffer = computed(() => models.value.find(model => model.key === selectedDetail.value?.entryKey)?.offers.find(offer => offer.key === selectedDetail.value?.offerKey))
const detailGroup = computed(() => detailOffer.value ? { ...detailOffer.value.group, models: [detailOffer.value.model] } : null)

function resetFilters() {
  selectedCategory.value = 'all'
  selectedGroupId.value = 'all'
  selectedRate.value = 'all'
  searchQuery.value = ''
}

watch([groups, categories, rates], () => {
  if (!groups.value.some(group => group.id === selectedGroupId.value)) selectedGroupId.value = 'all'
  if (!categories.value.some(category => category.id === selectedCategory.value)) selectedCategory.value = 'all'
  if (selectedRate.value !== 'all' && !rates.value.includes(selectedRate.value)) selectedRate.value = 'all'
})
</script>

<style scoped>
.category-button {
  @apply inline-flex min-h-10 items-center gap-2 rounded-lg bg-ui-muted px-4 py-2 text-sm font-medium text-ui-ink-muted transition-colors hover:bg-ui-brand-soft hover:text-ui-brand-strong focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-brand;
}
.category-button.active { @apply bg-ui-action text-ui-on-brand; }
.category-button :deep(path) { fill: currentColor; }
.category-button :deep(.model-icon-fallback) { background: transparent; color: inherit; }
.plaza-description { line-height: 1.75; overflow-wrap: anywhere; }
.plaza-description :deep(h1), .plaza-description :deep(h2), .plaza-description :deep(h3) { @apply mb-2 mt-3 text-base font-semibold first:mt-0; }
.plaza-description :deep(p) { @apply mb-2 text-ui-ink-muted last:mb-0; }
.plaza-description :deep(a) { @apply text-ui-brand-strong underline underline-offset-4; }
.plaza-description :deep(ul) { @apply mb-2 list-disc pl-5; }
.plaza-description :deep(ol) { @apply mb-2 list-decimal pl-5; }
.plaza-description :deep(li) { @apply mb-1 text-ui-ink-muted; }
.plaza-description :deep(code) { @apply rounded bg-ui-muted px-1 py-0.5 font-mono text-xs; }
.plaza-description :deep(blockquote) { @apply my-2 border-l-2 border-ui-brand pl-3; }
.plaza-description :deep(img) { max-width: 100%; height: auto; }
.plaza-description :deep(pre), .plaza-description :deep(table) { display: block; max-width: 100%; overflow-x: auto; }
</style>
