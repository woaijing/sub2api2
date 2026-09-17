<template>
  <section class="connection-studio" :aria-label="t('brand.studio.title')">
    <div class="studio-top"><span>{{ t('brand.studio.title') }}</span><span class="studio-edition">01 — 03</span></div>
    <div class="studio-modes" role="group" :aria-label="t('brand.studio.choose')">
      <button v-for="mode in modes" :key="mode.id" type="button" :aria-pressed="selected === mode.id" @click="selected = mode.id">
        <Icon :name="mode.icon" size="sm" />{{ t(`brand.studio.${mode.id}`) }}
      </button>
    </div>
    <div class="connection-scene">
      <svg class="connection-lines" viewBox="0 0 520 300" fill="none" aria-hidden="true">
        <circle cx="260" cy="150" r="108" stroke="currentColor" stroke-dasharray="3 7" />
        <circle cx="260" cy="150" r="78" stroke="currentColor" />
        <path d="M62 62H175Q194 62 194 81V129Q194 150 217 150H304Q327 150 327 174V222Q327 240 346 240H465" stroke="currentColor" stroke-width="1.5" />
        <circle cx="62" cy="62" r="4" fill="currentColor" /><circle cx="465" cy="240" r="4" fill="currentColor" />
      </svg>
      <div class="scene-input"><span class="scene-caption">{{ t('brand.studio.idea') }}</span><p>{{ t(`brand.studio.${selected}Prompt`) }}</p></div>
      <div class="connection-hub" aria-hidden="true"><Icon name="link" size="xl" /></div>
      <div class="scene-output"><span class="scene-caption">{{ t('brand.studio.possibility') }}</span><p :key="selected" aria-live="polite">{{ t(`brand.studio.${selected}Result`) }}</p></div>
      <span class="scene-key">ONE API KEY</span>
    </div>
    <div class="studio-bottom"><code><span>POST</span> {{ activeMode.endpoint }}</code><span>{{ t('brand.studio.example') }}</span></div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
const { t } = useI18n()
const modes = [
  { id: 'code', icon: 'terminal', endpoint: '/v1/responses' },
  { id: 'write', icon: 'chat', endpoint: '/v1/messages' },
  { id: 'image', icon: 'sparkles', endpoint: '/v1/images/generations' }
] as const
const selected = ref<(typeof modes)[number]['id']>('code')
const activeMode = computed(() => modes.find(mode => mode.id === selected.value) ?? modes[0])
</script>

<style scoped>
.connection-studio { border: 1px solid rgb(var(--ui-line)); border-radius: 18px; background: rgb(var(--ui-surface)); overflow: hidden; box-shadow: 0 24px 60px -28px #6f49353b; }
.studio-top { padding: 22px 24px 17px; display: flex; justify-content: space-between; gap: 10px; font-size: 12px; color: rgb(var(--ui-ink-muted)); }
.studio-edition { font-family: ui-monospace, monospace; color: rgb(var(--ui-brand-strong)); }
.studio-modes { display: flex; gap: 5px; padding: 0 20px 18px; }
.studio-modes button { flex: 1; display: flex; justify-content: center; align-items: center; gap: 7px; padding: 10px 6px; font-size: 12px; color: rgb(var(--ui-ink-muted)); border-radius: 7px; transition: background .2s; }
.studio-modes button[aria-pressed='true'] { color: rgb(var(--ui-brand-strong)); background: rgb(var(--ui-brand-soft)); }
.studio-modes button:hover { background: rgb(var(--ui-surface-muted)); }
.studio-modes button:focus-visible { outline: 2px solid rgb(var(--ui-brand)); outline-offset: 2px; }
.connection-scene { position: relative; height: 300px; background-color: rgb(var(--ui-surface-muted) / .6); background-image: radial-gradient(rgb(var(--ui-line)) 1px, transparent 1px); background-size: 16px 16px; }
.connection-lines { position: absolute; inset: 0; width: 100%; height: 100%; color: rgb(var(--ui-brand) / .4); }
.connection-hub { position: absolute; left: 50%; top: 50%; transform: translate(-50%, -50%) rotate(-10deg); width: 82px; height: 82px; border-radius: 21px; display: grid; place-items: center; color: rgb(var(--ui-on-brand)); background: rgb(var(--ui-action)); box-shadow: 7px 9px 0 rgb(var(--ui-brand) / .16); }
.connection-hub svg { transform: rotate(10deg); width: 37px; height: 37px; }
.scene-input, .scene-output { position: absolute; max-width: 66%; border: 1px solid rgb(var(--ui-line)); background: rgb(var(--ui-surface)); padding: 12px 16px; border-radius: 10px; box-shadow: 0 4px 12px #00000004; }
.scene-input { left: 24px; top: 22px; transform: rotate(-3deg); }
.scene-output { right: 24px; bottom: 25px; transform: rotate(2deg); }
.scene-caption { font-size: 10px; color: rgb(var(--ui-ink-muted)); }
.scene-input p, .scene-output p { font-size: 14px; font-weight: 550; margin-top: 4px; }
.scene-key { position: absolute; left: 20px; bottom: 25px; writing-mode: vertical-rl; font: 9px ui-monospace, monospace; letter-spacing: 2px; color: rgb(var(--ui-ink-muted)); }
.studio-bottom { display: flex; align-items: center; justify-content: space-between; gap: 10px; min-height: 62px; padding: 16px 24px; }
.studio-bottom code { font-size: 11px; overflow-wrap: anywhere; }
.studio-bottom code span { color: rgb(var(--ui-brand-strong)); margin-right: 7px; }
.studio-bottom > span { font-size: 10px; color: rgb(var(--ui-ink-muted)); flex-shrink: 0; }
@media (max-width: 639px) { .studio-top { padding: 18px 16px 14px; } .studio-modes { padding: 0 12px 14px; } .studio-modes button { gap: 4px; } .connection-scene { height: 280px; } .scene-input { left: 16px; } .scene-output { right: 16px; } .studio-bottom { padding: 14px 16px; } .studio-bottom code { font-size: 10px; } }
</style>
