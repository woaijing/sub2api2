import { afterEach, describe, expect, it, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { defineComponent } from 'vue'
import type { ModelPlazaGroup, PlazaModel } from '@/api/modelPlaza'
import ModelPlazaContent from '../ModelPlazaContent.vue'
import PlazaGroupSection from '../PlazaGroupSection.vue'
import { basePriceRange, buildModelCatalog, offerRate } from '../catalog'

vi.mock('@/stores/auth', () => ({ useAuthStore: () => ({ isAuthenticated: false }) }))
vi.mock('vue-i18n', async () => ({
  ...await vi.importActual<typeof import('vue-i18n')>('vue-i18n'),
  useI18n: () => ({ t: (key: string, values?: Record<string, unknown>) => values ? `${key} ${JSON.stringify(values)}` : key })
}))

function model(name = 'claude-sonnet-4-6', overrides: Partial<PlazaModel> = {}): PlazaModel {
  return {
    name, platform: 'anthropic', official_pricing: null,
    pricing: {
      billing_mode: 'token', input_price: 3e-6, output_price: 15e-6,
      cache_write_price: 3.75e-6, cache_read_price: 0,
      image_input_price: null, image_output_price: null, per_request_price: null, intervals: []
    },
    ...overrides
  }
}

function group(id: number, models: PlazaModel[], overrides: Partial<ModelPlazaGroup> = {}): ModelPlazaGroup {
  return {
    id, name: `Group ${id}`, description: '', platform: 'anthropic', subscription_type: 'standard',
    rate_multiplier: 1, peak_rate_enabled: false, peak_start: '', peak_end: '', peak_rate_multiplier: 1,
    is_exclusive: false, image_rate_independent: false, image_rate_multiplier: 1,
    long_context_pricing_enabled: true, models, ...overrides
  }
}

const dialogStub = defineComponent({
  props: ['show', 'title'],
  template: '<div v-if="show" role="dialog"><slot /></div>'
})

function mountContent(groups: ModelPlazaGroup[], description = '') {
  return mount(ModelPlazaContent, {
    props: { response: { groups, description }, loading: false },
    global: { stubs: { BaseDialog: dialogStub, PlazaGroupSection: true } }
  })
}

afterEach(() => { document.body.innerHTML = '' })

describe('model catalog pricing', () => {
  it('aggregates routing platforms but keeps different billing units separate', () => {
    const token = model()
    const image = model(token.name, { pricing: { ...token.pricing!, billing_mode: 'image', per_request_price: 0.2 } })
    const source = [group(1, [token]), group(2, [{ ...token, platform: 'antigravity' }, image], { user_rate_multiplier: 0.5 })]
    const entries = buildModelCatalog(source)
    expect(entries).toHaveLength(2)
    const tokens = entries.find(entry => entry.billingMode === 'token')!
    expect(tokens.offers.map(offer => offer.group.id)).toEqual([2, 1])
    expect(tokens.category.label).toBe('CLAUDE')
    expect(source[0].models).toEqual([token])
    expect(basePriceRange(tokens, 'input_price')).toBe('$3')
    expect(basePriceRange(entries.find(entry => entry.billingMode === 'image')!, 'per_request_price')).toBe('$0.2')
  })

  it('preserves zero prices and personal rates, with independent image rates taking precedence', () => {
    const token = model()
    const image = model('gpt-image-1', { pricing: { ...token.pricing!, billing_mode: 'image' } })
    const entries = buildModelCatalog([group(1, [token, image], {
      user_rate_multiplier: 0, image_rate_independent: true, image_rate_multiplier: 0.3
    })])
    expect(offerRate(entries.find(entry => entry.billingMode === 'token')!.offers[0])).toBe(0)
    expect(offerRate(entries.find(entry => entry.billingMode === 'image')!.offers[0])).toBe(0.3)
    expect(basePriceRange(entries[0], 'cache_read_price')).toBe('$0')
  })

  it('includes absolute and multiplier tiers in base price ranges, without applying group discounts', () => {
    const token = model()
    token.pricing!.intervals = [
      { min_tokens: 0, max_tokens: 200000, input_price: null, output_price: null, cache_write_price: null, cache_read_price: null, per_request_price: null },
      { min_tokens: 200000, max_tokens: null, input_price: null, input_multiplier: 2, output_price: 20e-6, cache_write_price: null, cache_read_price: null, per_request_price: null }
    ]
    const entry = buildModelCatalog([group(1, [token], { rate_multiplier: 0.1 })])[0]
    expect(basePriceRange(entry, 'input_price')).toBe('$3 - $6')
    expect(basePriceRange(entry, 'output_price')).toBe('$15 - $20')
    const unknown = buildModelCatalog([group(1, [model('custom-model', { pricing: null, official_pricing: { input_price: 5e-6, output_price: null, cache_write_price: null, cache_read_price: null } })])])[0]
    expect(basePriceRange(unknown, 'input_price')).toBe('-')
  })
})

describe('model plaza interactions', () => {
  it('combines category, search, group and effective-rate filters and resets them', async () => {
    const wrapper = mountContent([
      group(1, [model(), model('gpt-5.4', { platform: 'openai' })]),
      group(2, [model()], { user_rate_multiplier: 0.5 })
    ])
    expect(wrapper.findAll('article')).toHaveLength(2)
    await wrapper.findAll('.category-button').find(button => button.text() === 'CLAUDE')!.trigger('click')
    await wrapper.find('input').setValue('  SONNET  ')
    await wrapper.findAll('select')[0].setValue(2)
    await wrapper.findAll('select')[1].setValue(0.5)
    expect(wrapper.findAll('article')).toHaveLength(1)
    expect(wrapper.find('article').text()).toContain('"count":1')
    await wrapper.findAll('select')[1].setValue(1)
    expect(wrapper.findAll('article')).toHaveLength(0)
    expect(wrapper.text()).toContain('modelPlaza.noSearchResult')
    await wrapper.findAll('button').find(button => button.text().includes('resetFilters'))!.trigger('click')
    expect(wrapper.findAll('article')).toHaveLength(2)
    wrapper.unmount()
  })

  it('opens the selected model and group with all billing metadata intact', async () => {
    const target = group(2, [model()], { user_rate_multiplier: 0.3, peak_rate_enabled: true, peak_start: '12:00', peak_end: '18:00', peak_rate_multiplier: 2 })
    const wrapper = mountContent([group(1, [model()]), target])
    const toggle = wrapper.find('article button[aria-expanded]')
    await toggle.trigger('click')
    expect(toggle.attributes('aria-expanded')).toBe('true')
    expect(wrapper.find('article del').text()).toBe('1x')
    await wrapper.find('article li button').trigger('click')
    expect(wrapper.findComponent(PlazaGroupSection).props('group')).toEqual(target)
    await wrapper.setProps({ response: { groups: [], description: '' } })
    expect(wrapper.find('[role="dialog"]').exists()).toBe(false)
    wrapper.unmount()
  })

  it('clears unavailable filters when the server refreshes its catalog', async () => {
    const wrapper = mountContent([group(1, [model()], { user_rate_multiplier: 0.3 })])
    await wrapper.findAll('.category-button')[1].trigger('click')
    await wrapper.findAll('select')[0].setValue(1)
    await wrapper.findAll('select')[1].setValue(0.3)
    await wrapper.setProps({ response: { groups: [group(2, [model('gpt-5.4')])], description: '' } })
    expect(wrapper.findAll('article')).toHaveLength(1)
    expect(wrapper.find('article').text()).toContain('gpt-5.4')
    wrapper.unmount()
  })

  it('sanitizes billing markdown and distinguishes loading, failure and empty states', async () => {
    const wrapper = mountContent([], '<img src="x" onerror="alert(1)"><script>alert(1)</script>')
    expect(wrapper.find('.plaza-description script').exists()).toBe(false)
    expect(wrapper.find('.plaza-description img').attributes('onerror')).toBeUndefined()
    expect(wrapper.text()).toContain('modelPlaza.empty')
    await wrapper.setProps({ loading: true })
    expect(wrapper.find('[role="status"]').exists()).toBe(true)
    await wrapper.setProps({ loading: false, error: true })
    await wrapper.find('[role="alert"] button').trigger('click')
    expect(wrapper.emitted('retry')).toHaveLength(1)
    wrapper.unmount()
  })
})
