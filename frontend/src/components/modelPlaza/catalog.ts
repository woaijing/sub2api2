import type { ModelPlazaGroup, PlazaModel } from '@/api/modelPlaza'
import type { UserSupportedModelPricing } from '@/api/channels'
import type { BillingMode } from '@/constants/channel'
import { formatScaled, resolveIntervalPrices } from '@/utils/pricing'

export interface PlazaOffer {
  key: string
  group: ModelPlazaGroup
  model: PlazaModel
}

export interface PlazaCategory {
  id: string
  label: string
  iconModel: string
}

export interface PlazaCatalogEntry {
  key: string
  name: string
  category: PlazaCategory
  billingMode: BillingMode
  offers: PlazaOffer[]
}

const categories: [RegExp, string, string][] = [
  [/claude/i, 'CLAUDE', 'claude'],
  [/codex/i, 'CODEX', 'gpt'],
  [/deepseek/i, 'DEEPSEEK', 'deepseek'],
  [/embed/i, 'EMBED', 'text-embedding-3'],
  [/rerank/i, 'RERANK', 'command'],
  [/nano|imagen/i, 'NANO', 'gemini'],
  [/gemini|gemma|veo/i, 'GEMINI', 'gemini'],
  [/glm|cogview|cogvideo/i, 'GLM', 'glm'],
  [/gpt|chatgpt|^o[134](?:-|$)|dall-e|whisper|tts/i, 'GPT', 'gpt'],
  [/grok/i, 'GROK', 'grok'],
  [/kimi|moonshot/i, 'KIMI', 'kimi'],
  [/qwen|qwq/i, 'QWEN', 'qwen'],
  [/minimax|abab/i, 'MINIMAX', 'minimax'],
  [/llama/i, 'LLAMA', 'llama'],
  [/mistral|mixtral|codestral/i, 'MISTRAL', 'mistral']
]

function categoryFor(model: PlazaModel): PlazaCategory {
  const match = categories.find(([pattern]) => pattern.test(model.name))
  if (match) return { id: match[1], label: match[1], iconModel: match[2] }
  const label = (model.platform || 'OTHER').toUpperCase()
  return { id: label, label, iconModel: model.name }
}

export function offerRate(offer: PlazaOffer): number {
  const { group, model } = offer
  if (model.pricing?.billing_mode === 'image' && group.image_rate_independent) {
    return group.image_rate_multiplier ?? 1
  }
  return group.user_rate_multiplier ?? group.rate_multiplier
}

// Keep different billing units separate; the same model can use multiple routing platforms.
export function buildModelCatalog(groups: ModelPlazaGroup[]): PlazaCatalogEntry[] {
  const entries = new Map<string, PlazaCatalogEntry>()
  for (const group of groups) {
    for (const model of group.models) {
      const billingMode = model.pricing?.billing_mode ?? 'token'
      const key = JSON.stringify([model.name, billingMode])
      let entry = entries.get(key)
      if (!entry) {
        entry = { key, name: model.name, category: categoryFor(model), billingMode, offers: [] }
        entries.set(key, entry)
      }
      const offerKey = JSON.stringify([group.id, model.platform])
      if (!entry.offers.some(offer => offer.key === offerKey)) {
        entry.offers.push({ key: offerKey, group, model })
      }
    }
  }
  for (const entry of entries.values()) {
    entry.offers.sort((a, b) => offerRate(a) - offerRate(b) || a.group.name.localeCompare(b.group.name))
  }
  return [...entries.values()].sort((a, b) =>
    a.category.label.localeCompare(b.category.label) || a.name.localeCompare(b.name)
  )
}

export type PlazaPriceField = 'input_price' | 'output_price' | 'cache_write_price' | 'cache_write_1h_price' | 'cache_read_price' | 'per_request_price'

export function basePriceRange(entry: PlazaCatalogEntry, field: PlazaPriceField): string {
  const values = entry.offers.flatMap(({ model }) => {
    const pricing = model.pricing
    if (!pricing) return []
    const tiers = pricing.intervals ?? []
    const prices: Pick<UserSupportedModelPricing, PlazaPriceField>[] = tiers.length
      ? tiers.map(tier => ({ ...resolveIntervalPrices(tier, pricing), per_request_price: tier.per_request_price ?? pricing.per_request_price }))
      : [pricing]
    return prices.map(price => price[field]).filter((value): value is number => value != null && Number.isFinite(value))
  })
  if (!values.length) return '-'
  const min = Math.min(...values)
  const max = Math.max(...values)
  const scale = field === 'per_request_price' ? 1 : 1_000_000
  return min === max ? formatScaled(min, scale) : `${formatScaled(min, scale)} - ${formatScaled(max, scale)}`
}
