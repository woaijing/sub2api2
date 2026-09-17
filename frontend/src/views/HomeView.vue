<template>
  <!-- Custom Home Content: Full Page Mode -->
  <div v-if="hasHomeContent" class="min-h-screen">
    <!-- iframe mode -->
    <iframe
      v-if="isHomeContentUrl"
      :src="homeContent.trim()"
      class="h-screen w-full border-0"
      allowfullscreen
    ></iframe>
    <!-- HTML mode - SECURITY: homeContent is admin-only setting, XSS risk is acceptable -->
    <div v-else v-html="homeContent"></div>
  </div>

  <!-- Compact Home Page -->
  <div
    v-else-if="compactHomeEnabled"
    data-testid="compact-home"
    class="flex min-h-screen flex-col bg-ui-page text-ui-ink"
  >
    <header class="border-b border-gray-200 px-4 py-4 sm:px-6 dark:border-dark-800">
      <nav class="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 sm:gap-4">
        <div class="flex min-w-0 flex-1 items-center gap-3">
          <img
            :src="siteLogo || '/logo.svg'"
            alt="Logo"
            class="h-9 w-9 shrink-0 rounded-lg object-contain"
          />
          <span class="min-w-0 truncate text-base font-semibold">{{ siteName }}</span>
        </div>
        <div class="flex max-w-full shrink-0 flex-wrap items-center justify-end gap-2">
          <LocaleSwitcher />
          <a
            v-if="docUrl"
            :href="docUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-gray-500 hover:bg-gray-100 dark:text-dark-400 dark:hover:bg-dark-800"
            :title="t('home.viewDocs')"
          >
            <Icon name="book" size="md" />
          </a>
          <router-link
            v-if="showModelPlazaEntry"
            to="/model-plaza"
            class="flex h-10 shrink-0 items-center gap-1.5 rounded-lg px-2.5 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-700 dark:text-dark-400 dark:hover:bg-dark-800 dark:hover:text-white"
            :title="t('nav.modelPlaza')"
          >
            <Icon name="grid" size="md" />
            <span class="hidden sm:inline">{{ t('nav.modelPlaza') }}</span>
          </router-link>
          <button
            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-gray-500 hover:bg-gray-100 dark:text-dark-400 dark:hover:bg-dark-800"
            :title="isDark ? t('home.switchToLight') : t('home.switchToDark')"
            @click="toggleTheme"
          >
            <Icon v-if="isDark" name="sun" size="md" />
            <Icon v-else name="moon" size="md" />
          </button>
          <router-link
            :to="isAuthenticated ? dashboardPath : '/login'"
            class="inline-flex min-h-10 shrink-0 items-center justify-center rounded-lg bg-gray-900 px-4 py-2 text-sm font-medium text-white hover:bg-gray-800 dark:bg-white dark:text-gray-900 dark:hover:bg-gray-200"
          >
            {{ isAuthenticated ? t('home.dashboard') : t('home.login') }}
          </router-link>
        </div>
      </nav>
    </header>

    <main class="flex min-w-0 flex-1 items-center justify-center px-4 py-16 sm:px-6">
      <div class="min-w-0 max-w-2xl text-center">
        <img
          :src="siteLogo || '/logo.svg'"
          alt="Logo"
          class="mx-auto mb-6 h-20 w-20 rounded-2xl object-contain"
        />
        <h1 class="[overflow-wrap:anywhere] text-3xl font-bold md:text-4xl">{{ siteName }}</h1>
        <p class="mt-4 whitespace-pre-wrap [overflow-wrap:anywhere] text-base text-gray-600 dark:text-dark-300">{{ siteSubtitle }}</p>
        <router-link
          :to="isAuthenticated ? dashboardPath : '/login'"
          class="btn btn-primary mt-8 min-h-10 px-5"
        >
          {{ isAuthenticated ? t('home.goToDashboard') : t('home.login') }}
        </router-link>
      </div>
    </main>

    <footer class="min-w-0 border-t border-gray-200 px-4 py-5 text-center text-sm text-gray-500 [overflow-wrap:anywhere] sm:px-6 dark:border-dark-800 dark:text-dark-400">
      &copy; {{ currentYear }} {{ siteName }}
    </footer>
  </div>

  <!-- Default branded home; custom HTML and compact mode retain priority. -->
  <div v-else id="top" class="brand-home" data-testid="brand-home">
    <PublicHeader />
    <main>
      <section class="brand-hero brand-width">
        <div class="hero-copy">
          <p class="brand-eyebrow"><span></span>{{ t('brand.eyebrow') }}</p>
          <h1>{{ t('brand.heroFirst') }}<br /><span>{{ t('brand.heroSecond') }}</span></h1>
          <p class="hero-description">{{ t('brand.heroDescription') }}</p>
          <div class="hero-actions">
            <RouterLink :to="startPath" class="btn btn-primary brand-cta">{{ t(isAuthenticated ? 'home.goToDashboard' : 'brand.start') }}<Icon name="arrowRight" size="sm" /></RouterLink>
            <RouterLink v-if="showModelPlazaEntry" to="/model-plaza" class="hero-secondary">{{ t('brand.explore') }}<Icon name="chevronRight" size="sm" /></RouterLink>
            <a v-else href="#start" class="hero-secondary">{{ t('brand.seeHow') }}<Icon name="chevronRight" size="sm" /></a>
          </div>
          <p class="hero-note"><span class="note-line"></span>{{ t('brand.heroNote') }}</p>
        </div>
        <div class="hero-visual">
          <div class="visual-corner" aria-hidden="true">+</div>
          <ConnectionStudio />
          <div class="visual-caption" aria-hidden="true"><span>IDEA &rarr; API &rarr; POSSIBILITY</span><Icon name="arrowRight" size="sm" /></div>
        </div>
      </section>

      <section class="ecosystem brand-width" :aria-label="t('brand.ecosystem')">
        <p>{{ t('brand.ecosystem') }}</p>
        <div class="ecosystem-models">
          <span v-for="provider in providers" :key="provider.name"><ModelIcon :model="provider.model" size="22px" />{{ provider.name }}</span>
        </div>
        <small>{{ t('brand.availability') }}</small>
      </section>

      <section id="possibilities" class="capabilities brand-width">
        <div class="section-heading">
          <div><p class="brand-eyebrow">{{ t('brand.capabilityLabel') }}</p><h2>{{ t('brand.capabilityTitle') }}</h2></div>
          <p class="section-description">{{ t('brand.capabilityDescription') }}</p>
        </div>
        <div class="capability-grid">
          <article v-for="(feature, index) in features" :key="feature.key" class="capability-card">
            <div class="capability-top"><span>0{{ index + 1 }}</span><Icon :name="feature.icon" size="lg" /></div>
            <h3>{{ t(`brand.${feature.key}Title`) }}</h3>
            <p>{{ t(`brand.${feature.key}Description`) }}</p>
            <RouterLink v-if="feature.key === 'choose' && showModelPlazaEntry" to="/model-plaza" class="feature-link">{{ t('nav.modelPlaza') }}<Icon name="arrowRight" size="sm" /></RouterLink>
            <RouterLink v-else :to="feature.key === 'usage' ? '/usage' : '/keys'" class="feature-link">{{ t(feature.key === 'usage' ? 'nav.usage' : 'nav.apiKeys') }}<Icon name="arrowRight" size="sm" /></RouterLink>
          </article>
        </div>
      </section>

      <section id="start" class="workflow brand-width">
        <div class="workflow-intro"><p class="brand-eyebrow">{{ t('brand.workflowLabel') }}</p><h2>{{ t('brand.workflowTitle') }}</h2><a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer" class="feature-link">{{ t('brand.docsLink') }}<Icon name="externalLink" size="sm" /></a></div>
        <ol class="workflow-steps">
          <li v-for="(step, index) in ['One', 'Two', 'Three']" :key="step"><span class="step-number">0{{ index + 1 }}</span><div><h3>{{ t(`brand.step${step}`) }}</h3><p>{{ t(`brand.step${step}Description`) }}</p></div></li>
        </ol>
      </section>

      <section class="closing brand-width">
        <div class="closing-mark" aria-hidden="true"><Icon name="sparkles" size="xl" /></div>
        <div><h2>{{ t('brand.closingTitle') }}</h2><p>{{ t('brand.closingDescription') }}</p></div>
        <RouterLink :to="startPath" class="btn btn-primary brand-cta">{{ t(isAuthenticated ? 'home.goToDashboard' : 'brand.start') }}<Icon name="arrowRight" size="sm" /></RouterLink>
      </section>
    </main>
    <footer class="brand-footer brand-width">
      <div><RouterLink to="/home" class="footer-brand">{{ siteName }}</RouterLink><p>{{ t('brand.footerNote') }}</p></div>
      <div class="footer-meta"><div><a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer">{{ t('home.docs') }}</a><a :href="githubUrl" target="_blank" rel="noopener noreferrer">GitHub</a><RouterLink :to="isAuthenticated ? dashboardPath : '/login'">{{ t('home.dashboard') }}</RouterLink></div><p>&copy; {{ currentYear }} {{ siteName }}</p></div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore, useAppStore } from '@/stores'
import LocaleSwitcher from '@/components/common/LocaleSwitcher.vue'
import Icon from '@/components/icons/Icon.vue'
import PublicHeader from '@/components/layout/PublicHeader.vue'
import ConnectionStudio from '@/components/common/ConnectionStudio.vue'
import ModelIcon from '@/components/common/ModelIcon.vue'
import { sanitizeUrl } from '@/utils/url'
import { FeatureFlags, isFeatureFlagEnabled } from '@/utils/featureFlags'

const { t } = useI18n()

const authStore = useAuthStore()
const appStore = useAppStore()

// Site settings - directly from appStore (already initialized from injected config)
const siteName = computed(() => appStore.cachedPublicSettings?.site_name || appStore.siteName || 'Sub2API')
const siteLogo = computed(() => sanitizeUrl(appStore.cachedPublicSettings?.site_logo || appStore.siteLogo || '', { allowRelative: true, allowDataUrl: true }))
const siteSubtitle = computed(() => appStore.cachedPublicSettings?.site_subtitle || 'AI API Gateway Platform')
const docUrl = computed(() => sanitizeUrl(appStore.cachedPublicSettings?.doc_url || appStore.docUrl || ''))
const homeContent = computed(() => appStore.cachedPublicSettings?.home_content || '')
const hasHomeContent = computed(() => homeContent.value.trim().length > 0)
const compactHomeEnabled = computed(() => appStore.cachedPublicSettings?.compact_home_enabled === true)
const modelPlazaEnabled = computed(() => isFeatureFlagEnabled(FeatureFlags.modelPlaza))

// Check if homeContent is a URL (for iframe display)
const isHomeContentUrl = computed(() => {
  const content = homeContent.value.trim()
  return content.startsWith('http://') || content.startsWith('https://')
})

// Theme
const isDark = ref(document.documentElement.classList.contains('dark'))

// GitHub URL
const githubUrl = 'https://github.com/Wei-Shaw/sub2api'

// Auth state
const isAuthenticated = computed(() => authStore.isAuthenticated)
const modelPlazaRequiresAuth = computed(
  () => appStore.cachedPublicSettings?.model_plaza_require_auth === true,
)
const showModelPlazaEntry = computed(
  () => modelPlazaEnabled.value && (isAuthenticated.value || !modelPlazaRequiresAuth.value),
)
const isAdmin = computed(() => authStore.isAdmin)
const dashboardPath = computed(() => isAdmin.value ? '/admin/dashboard' : '/dashboard')
const canRegister = computed(() => appStore.cachedPublicSettings?.registration_enabled === true && appStore.cachedPublicSettings?.backend_mode_enabled !== true)
const startPath = computed(() => isAuthenticated.value ? dashboardPath.value : canRegister.value ? '/register' : '/login')
const providers = [{ name: 'Claude', model: 'claude' }, { name: 'OpenAI', model: 'gpt' }, { name: 'Gemini', model: 'gemini' }, { name: 'DeepSeek', model: 'deepseek' }]
const features = [{ key: 'choose', icon: 'grid' }, { key: 'keys', icon: 'key' }, { key: 'usage', icon: 'chart' }] as const

// Current year for footer
const currentYear = computed(() => new Date().getFullYear())

// Toggle theme
function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}

// Initialize theme
function initTheme() {
  const savedTheme = localStorage.getItem('theme')
  if (
    savedTheme === 'dark' ||
    (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)
  ) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  }
}

onMounted(() => {
  initTheme()

  // Check auth state
  authStore.checkAuth()

  // Ensure public settings are loaded (will use cache if already loaded from injected config)
  if (!appStore.publicSettingsLoaded) {
    appStore.fetchPublicSettings()
  }
})
</script>

<style scoped>
.brand-home { background: rgb(var(--ui-page)); color: rgb(var(--ui-ink)); }
.brand-width { max-width: 1216px; margin-left: auto; margin-right: auto; }
.brand-hero { display: grid; grid-template-columns: 1.03fr 1fr; gap: 64px; align-items: center; padding: 94px 0 76px; }
.brand-eyebrow { display: flex; align-items: center; gap: 10px; font-size: 12px; font-weight: 600; color: rgb(var(--ui-brand-strong)); letter-spacing: .06em; }
.brand-eyebrow > span { width: 6px; height: 6px; background: currentColor; border-radius: 50%; }
.hero-copy h1 { margin-top: 25px; font-size: clamp(44px, 4.8vw, 67px); line-height: 1.25; font-weight: 750; letter-spacing: -.055em; }
.hero-copy h1 > span { color: rgb(var(--ui-brand-strong)); }
.hero-description { max-width: 455px; margin-top: 24px; font-size: 16px; line-height: 1.95; color: rgb(var(--ui-ink-muted)); }
.hero-actions { display: flex; flex-wrap: wrap; align-items: center; gap: 22px; margin-top: 34px; }
.brand-cta { gap: 20px; padding: 14px 22px; min-height: 50px; border-radius: 9px; }
.hero-secondary { display: inline-flex; align-items: center; gap: 6px; font-size: 13px; font-weight: 550; }
.hero-secondary:hover { color: rgb(var(--ui-brand-strong)); }
.hero-note { display: flex; align-items: center; gap: 10px; margin-top: 32px; color: rgb(var(--ui-ink-muted)); font-size: 11px; }
.note-line { width: 26px; height: 1px; background: rgb(var(--ui-control-line)); }
.hero-visual { position: relative; min-width: 0; }
.visual-corner { position: absolute; right: -20px; top: -32px; font-size: 26px; font-weight: 200; color: rgb(var(--ui-control-line)); }
.visual-caption { display: flex; justify-content: space-between; align-items: center; margin: 14px 5px 0; font: 9px ui-monospace, monospace; letter-spacing: 2px; color: rgb(var(--ui-ink-muted)); }
.visual-caption > span:last-child { font-size: 18px; }
.ecosystem { padding: 31px 0; border-top: 1px solid rgb(var(--ui-line)); border-bottom: 1px solid rgb(var(--ui-line)); display: grid; grid-template-columns: 1fr auto; align-items: center; gap: 15px 32px; }
.ecosystem > p { font-size: 12px; color: rgb(var(--ui-ink-muted)); }
.ecosystem-models { display: flex; flex-wrap: wrap; align-items: center; gap: 38px; }
.ecosystem-models > span { display: flex; align-items: center; gap: 9px; font-size: 17px; font-weight: 600; letter-spacing: -.5px; }
.ecosystem small { grid-column: 1 / -1; font-size: 10px; color: rgb(var(--ui-ink-muted)); }
.ecosystem :deep(path) { fill: currentColor; }
.capabilities { padding-top: 84px; scroll-margin-top: 30px; }
.section-heading { display: flex; justify-content: space-between; align-items: flex-end; gap: 40px; margin-bottom: 32px; }
.section-heading h2, .workflow h2 { font-size: 32px; line-height: 1.5; font-weight: 650; letter-spacing: -.035em; margin-top: 15px; }
.section-description { max-width: 320px; font-size: 13px; line-height: 1.85; color: rgb(var(--ui-ink-muted)); }
.capability-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.capability-card { padding: 27px; border: 1px solid rgb(var(--ui-line)); background: rgb(var(--ui-surface)); border-radius: 12px; }
.capability-top { display: flex; justify-content: space-between; align-items: center; color: rgb(var(--ui-brand-strong)); margin-bottom: 38px; }
.capability-top > span { font: 11px ui-monospace, monospace; color: rgb(var(--ui-ink-muted)); }
.capability-card h3 { font-size: 18px; font-weight: 650; margin-bottom: 12px; }
.capability-card > p { color: rgb(var(--ui-ink-muted)); font-size: 13px; line-height: 1.9; min-height: 74px; }
.feature-link { display: inline-flex; align-items: center; gap: 10px; margin-top: 22px; font-size: 12px; font-weight: 550; color: rgb(var(--ui-brand-strong)); }
.feature-link:hover { text-decoration: underline; text-underline-offset: 4px; }
.workflow { display: grid; grid-template-columns: 1fr 1.15fr; gap: 110px; padding-top: 94px; padding-bottom: 94px; scroll-margin-top: 30px; }
.workflow h2 { max-width: 355px; }
.workflow-steps > li { display: flex; gap: 22px; padding-bottom: 29px; position: relative; }
.workflow-steps > li:not(:last-child)::before { position: absolute; content: ''; top: 39px; bottom: 5px; left: 18px; width: 1px; background: rgb(var(--ui-line)); }
.workflow-steps > li:last-child { padding-bottom: 0; }
.step-number { display: grid; place-items: center; width: 37px; height: 37px; flex-shrink: 0; border: 1px solid rgb(var(--ui-line)); border-radius: 50%; font: 11px ui-monospace, monospace; color: rgb(var(--ui-brand-strong)); }
.workflow-steps h3 { font-size: 15px; font-weight: 600; margin: 7px 0 10px; }
.workflow-steps p { font-size: 13px; line-height: 1.8; color: rgb(var(--ui-ink-muted)); }
.closing { display: flex; align-items: center; gap: 26px; border: 1px solid rgb(var(--ui-line)); background: rgb(var(--ui-brand-soft) / .45); border-radius: 14px; padding: 36px; }
.closing-mark { display: grid; place-items: center; width: 54px; height: 54px; border-radius: 14px; background: rgb(var(--ui-brand-soft)); color: rgb(var(--ui-brand-strong)); flex-shrink: 0; }
.closing h2 { font-size: 23px; font-weight: 650; letter-spacing: -.04em; }
.closing p { margin-top: 9px; color: rgb(var(--ui-ink-muted)); font-size: 13px; }
.closing .brand-cta { flex-shrink: 0; margin-left: auto; }
.brand-footer { display: flex; justify-content: space-between; gap: 30px; padding-top: 55px; padding-bottom: 35px; }
.footer-brand { font-size: 17px; font-weight: 650; overflow-wrap: anywhere; }
.brand-footer p { font-size: 11px; margin-top: 12px; color: rgb(var(--ui-ink-muted)); }
.footer-meta { text-align: right; }
.footer-meta > div { display: flex; gap: 22px; font-size: 12px; }
.brand-home :is(a, button):focus-visible { outline: 2px solid rgb(var(--ui-brand)); outline-offset: 4px; }
@media (max-width: 1320px) { .brand-width { margin-left: 32px; margin-right: 32px; } .brand-hero { gap: 42px; } }
@media (max-width: 1023px) { .brand-hero { gap: 30px; padding-top: 65px; padding-bottom: 55px; } .hero-copy h1 { font-size: 46px; } .hero-actions { gap: 16px; } .hero-description { font-size: 14px; } .ecosystem { grid-template-columns: 1fr; } .section-heading { align-items: flex-start; flex-direction: column; gap: 16px; } .section-description { max-width: 550px; } .workflow { gap: 50px; } .capability-card { padding: 22px; } .closing { flex-wrap: wrap; } }
@media (max-width: 767px) { .brand-hero { grid-template-columns: 1fr; gap: 48px; padding-top: 48px; } .hero-copy h1 { font-size: 53px; } .hero-description { max-width: 490px; } .hero-visual { max-width: 540px; width: 100%; margin: auto; } .visual-corner { right: 2px; } .ecosystem-models { gap: 20px; } .capability-grid { grid-template-columns: 1fr; } .capabilities { padding-top: 52px; } .capability-top { margin-bottom: 20px; } .capability-card > p { min-height: auto; } .workflow { grid-template-columns: 1fr; padding-top: 55px; padding-bottom: 55px; gap: 30px; } .workflow h2 { max-width: 500px; } .closing { padding: 25px; gap: 18px; } .closing-mark { display: none; } .closing .brand-cta { margin-left: 0; } .brand-footer { flex-direction: column; } .footer-meta { text-align: left; } }
@media (max-width: 479px) { .brand-width { margin-left: 20px; margin-right: 20px; } .hero-copy h1 { font-size: 45px; } .hero-note { font-size: 10px; } .brand-cta { gap: 12px; padding: 13px 18px; } .hero-secondary { font-size: 12px; } .ecosystem-models { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; margin: 8px 0; } .section-heading h2, .workflow h2 { font-size: 28px; } .closing h2 { font-size: 22px; } }
@media (prefers-reduced-motion: reduce) { .brand-home :deep(*) { animation: none !important; transition: none !important; scroll-behavior: auto !important; } }
</style>
