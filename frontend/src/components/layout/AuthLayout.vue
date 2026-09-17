<template>
  <div v-if="experience" class="brand-auth" :class="`brand-auth-${experience}`">
    <PublicHeader auth />
    <main class="auth-workspace">
      <aside class="auth-story">
        <p class="auth-eyebrow"><span></span>{{ t(experience === 'login' ? 'brand.auth.loginEyebrow' : 'brand.auth.registerEyebrow') }}</p>
        <h2>{{ t(experience === 'login' ? 'brand.auth.loginTitle' : 'brand.auth.registerTitle') }}</h2>
        <p class="auth-description">{{ t(experience === 'login' ? 'brand.auth.loginDescription' : 'brand.auth.registerDescription') }}</p>
        <div class="auth-art" aria-hidden="true">
          <svg viewBox="0 0 440 250" fill="none">
            <path v-for="i in 8" :key="i" :d="`M${24 + i * 15} 244V${135 - i * 9}Q${24 + i * 15} ${38 - i * 2} 245 ${38 - i * 2}H410`" stroke="currentColor" :opacity=".17 + i * .07" />
            <circle cx="307" cy="107" r="53" stroke="currentColor" opacity=".25" />
            <circle cx="307" cy="107" r="72" stroke="currentColor" stroke-dasharray="2 7" opacity=".4" />
            <path d="M36 50H54M45 41V59M364 200H382M373 191V209" stroke="currentColor" opacity=".6" />
          </svg>
          <div class="art-emblem"><Icon name="sparkles" size="xl" /></div>
          <span class="art-label">MAKE SOMETHING<br />THAT MATTERS.</span>
        </div>
        <p class="auth-story-note">{{ t('brand.auth.note') }}</p>
      </aside>
      <div class="auth-form-column">
        <div class="auth-form"><slot /></div>
        <div class="auth-switch"><slot name="footer" /></div>
      </div>
    </main>
    <footer class="auth-page-footer"><span>&copy; {{ currentYear }} {{ siteName }}</span><span>{{ t('brand.footerNote') }}</span></footer>
  </div>
  <div v-else class="relative flex min-h-screen items-center justify-center overflow-hidden bg-ui-page p-4 text-ui-ink">
    <!-- Content Container -->
    <div class="relative z-10 w-full max-w-md">
      <!-- Logo/Brand -->
      <div class="mb-8 text-center">
        <!-- Custom Logo or Default Logo -->
        <template v-if="settingsLoaded">
          <div
            class="mb-4 inline-flex h-16 w-16 items-center justify-center overflow-hidden rounded-xl"
          >
            <img :src="siteLogo || '/logo.svg'" alt="Logo" class="h-full w-full object-contain" />
          </div>
          <h1 class="mb-2 break-words text-3xl font-bold text-ui-ink">
            {{ siteName }}
          </h1>
          <p class="break-words text-sm text-ui-ink-muted">
            {{ siteSubtitle }}
          </p>
        </template>
      </div>

      <!-- Card Container -->
      <div class="card p-6 sm:p-8">
        <slot />
      </div>

      <!-- Footer Links -->
      <div class="mt-6 text-center text-sm">
        <slot name="footer" />
      </div>

      <!-- Copyright -->
      <div class="mt-8 break-words text-center text-xs text-ui-ink-muted">
        &copy; {{ currentYear }} {{ siteName }}. All rights reserved.
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '@/stores'
import { sanitizeUrl } from '@/utils/url'
import PublicHeader from './PublicHeader.vue'
import Icon from '@/components/icons/Icon.vue'

defineProps<{ experience?: 'login' | 'register' }>()
const { t } = useI18n()

const appStore = useAppStore()

const siteName = computed(() => appStore.siteName || 'Sub2API')
const siteLogo = computed(() => sanitizeUrl(appStore.siteLogo || '', { allowRelative: true, allowDataUrl: true }))
const siteSubtitle = computed(() => appStore.cachedPublicSettings?.site_subtitle || 'Subscription to API Conversion Platform')
const settingsLoaded = computed(() => appStore.publicSettingsLoaded)

const currentYear = computed(() => new Date().getFullYear())

onMounted(() => {
  appStore.fetchPublicSettings()
})
</script>

<style scoped>
.brand-auth { display: flex; flex-direction: column; min-height: 100vh; background: rgb(var(--ui-page)); color: rgb(var(--ui-ink)); }
.auth-workspace { flex: 1; width: 100%; max-width: 1136px; margin: 0 auto; padding: 62px 32px 52px; display: grid; grid-template-columns: 1fr 440px; gap: 100px; align-items: center; }
.auth-story { min-width: 0; }
.auth-eyebrow { display: flex; align-items: center; gap: 9px; color: rgb(var(--ui-brand-strong)); font-size: 11px; font-weight: 550; letter-spacing: .06em; }
.auth-eyebrow > span { width: 5px; height: 5px; border-radius: 50%; background: currentColor; }
.auth-story h2 { margin-top: 23px; white-space: pre-line; font-size: 48px; font-weight: 650; letter-spacing: -.055em; line-height: 1.4; }
.auth-description { margin-top: 20px; max-width: 360px; color: rgb(var(--ui-ink-muted)); font-size: 14px; line-height: 1.95; }
.auth-art { position: relative; color: rgb(var(--ui-brand)); height: 250px; max-width: 440px; margin-top: 20px; }
.auth-art > svg { width: 100%; height: 100%; }
.art-emblem { position: absolute; left: 70%; top: 43%; transform: translate(-50%, -50%) rotate(-12deg); display: grid; place-items: center; width: 72px; height: 72px; border-radius: 19px; color: rgb(var(--ui-on-brand)); background: rgb(var(--ui-action)); box-shadow: 6px 7px 0 rgb(var(--ui-brand) / .13); }
.art-emblem svg { width: 35px; height: 35px; }
.art-label { position: absolute; left: 54%; bottom: 16px; font: 9px/1.7 ui-monospace, monospace; letter-spacing: 2px; color: rgb(var(--ui-ink-muted)); }
.auth-story-note { margin-top: 18px; padding-top: 22px; border-top: 1px solid rgb(var(--ui-line)); color: rgb(var(--ui-ink-muted)); font-size: 11px; }
.auth-form-column { min-width: 0; }
.auth-form { padding: 38px; border: 1px solid rgb(var(--ui-line)); border-radius: 17px; background: rgb(var(--ui-surface)); box-shadow: 0 18px 48px -30px #4a2d2530; }
.auth-form :deep(.auth-form-heading) { text-align: left; padding-bottom: 8px; }
.auth-form :deep(h1) { font-size: 26px; font-weight: 650; line-height: 1.35; letter-spacing: -.035em; color: rgb(var(--ui-ink)); }
.auth-form :deep(.auth-form-description) { margin-top: 10px; font-size: 13px; line-height: 1.7; color: rgb(var(--ui-ink-muted)); }
.auth-form :deep(.input) { min-height: 46px; border-radius: 8px; }
.auth-form :deep(.input-label) { font-size: 12px; margin-bottom: 9px; }
.auth-form :deep(button[type='submit']) { min-height: 46px; margin-top: 24px; }
.auth-form :deep(button:focus-visible) { outline: 2px solid rgb(var(--ui-brand)); outline-offset: 3px; }
.auth-switch { margin-top: 22px; text-align: center; font-size: 12px; }
.auth-page-footer { display: flex; justify-content: space-between; gap: 20px; width: 100%; max-width: 1216px; margin: 0 auto; padding: 22px 32px; font-size: 10px; color: rgb(var(--ui-ink-muted)); overflow-wrap: anywhere; }
@media (max-width: 1023px) { .auth-workspace { gap: 44px; grid-template-columns: 1fr 410px; padding-top: 44px; } .auth-story h2 { font-size: 37px; } .auth-form { padding: 30px; } .auth-art { height: 220px; } }
@media (max-width: 849px) { .auth-workspace { grid-template-columns: 1fr; max-width: 500px; padding: 38px 24px 45px; } .auth-story { display: none; } .auth-page-footer { justify-content: center; text-align: center; } .auth-page-footer > span:last-child { display: none; } }
@media (max-width: 479px) { .auth-workspace { padding: 28px 16px 38px; } .auth-form { padding: 28px 22px; border-radius: 13px; } .auth-form :deep(h1) { font-size: 24px; } }
@media (max-width: 359px) { .auth-form { padding: 24px 17px; } }
</style>
