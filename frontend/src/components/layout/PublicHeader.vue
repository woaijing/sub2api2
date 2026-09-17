<template>
  <header class="public-header">
    <nav class="public-nav" :aria-label="t('brand.navigation')">
      <RouterLink to="/home" class="public-brand" :title="siteName">
        <img :src="siteLogo || '/logo.svg'" :alt="siteName" width="34" height="34" />
        <span>{{ siteName }}</span>
      </RouterLink>
      <div v-if="!auth" class="public-links">
        <RouterLink v-if="showModelPlaza" to="/model-plaza">{{ t('nav.modelPlaza') }}</RouterLink>
        <a href="#possibilities">{{ t('brand.possibilities') }}</a>
        <a href="#start">{{ t('brand.getStarted') }}</a>
        <a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer">{{ t('home.docs') }}</a>
      </div>
      <div class="public-actions">
        <RouterLink v-if="auth" to="/home" class="back-home"><Icon name="chevronLeft" size="xs" />{{ t('brand.backHome') }}</RouterLink>
        <LocaleSwitcher />
        <button type="button" class="theme-button" :aria-label="t(isDark ? 'home.switchToLight' : 'home.switchToDark')" @click="toggleTheme">
          <Icon :name="isDark ? 'sun' : 'moon'" size="md" />
        </button>
        <RouterLink v-if="!auth" :to="isAuthenticated ? dashboardPath : '/login'" class="btn btn-primary header-login">
          {{ t(isAuthenticated ? 'home.dashboard' : 'home.login') }}<Icon name="chevronRight" size="xs" />
        </RouterLink>
        <details v-if="!auth" ref="menu" class="mobile-navigation" @keydown.esc="closeMenu">
          <summary :aria-label="t('brand.menu')"><Icon name="menu" size="md" /></summary>
          <div class="mobile-navigation-links" @click="closeMenu">
            <RouterLink v-if="showModelPlaza" to="/model-plaza">{{ t('nav.modelPlaza') }}</RouterLink>
            <a href="#possibilities">{{ t('brand.possibilities') }}</a>
            <a href="#start">{{ t('brand.getStarted') }}</a>
            <a v-if="docUrl" :href="docUrl" target="_blank" rel="noopener noreferrer">{{ t('home.docs') }}</a>
            <RouterLink :to="isAuthenticated ? dashboardPath : '/login'">{{ t(isAuthenticated ? 'home.dashboard' : 'home.login') }}</RouterLink>
          </div>
        </details>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { usePublicBrand } from '@/composables/usePublicBrand'
import LocaleSwitcher from '@/components/common/LocaleSwitcher.vue'
import Icon from '@/components/icons/Icon.vue'

defineProps<{ auth?: boolean }>()
const { t } = useI18n()
const { siteName, siteLogo, docUrl, isAuthenticated, dashboardPath, showModelPlaza, isDark, toggleTheme } = usePublicBrand()
const menu = ref<HTMLDetailsElement | null>(null)
function closeMenu() { if (menu.value) menu.value.open = false }
</script>

<style scoped>
.public-header { position: relative; z-index: 30; border-bottom: 1px solid rgb(var(--ui-line)); background: rgb(var(--ui-page) / .95); }
.public-nav { max-width: 1280px; min-height: 86px; margin: auto; padding: 16px 32px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }
.public-brand { display: flex; align-items: center; gap: 11px; min-width: 0; font-size: 19px; font-weight: 750; letter-spacing: -.6px; }
.public-brand img { flex-shrink: 0; border-radius: 9px; object-fit: contain; }
.public-brand span { overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 220px; }
.public-links { display: flex; gap: 26px; font-size: 13px; color: rgb(var(--ui-ink-muted)); }
.public-links a:hover, .back-home:hover { color: rgb(var(--ui-brand-strong)); }
.public-actions { display: flex; align-items: center; gap: 9px; flex-shrink: 0; }
.theme-button { display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; color: rgb(var(--ui-ink-muted)); }
.theme-button:hover { background: rgb(var(--ui-surface-muted)); }
.header-login { margin-left: 8px; min-height: 40px; font-size: 13px; }
.back-home { display: flex; align-items: center; gap: 4px; margin-right: 14px; font-size: 13px; color: rgb(var(--ui-ink-muted)); }
.mobile-navigation { position: relative; display: none; }
.mobile-navigation summary { list-style: none; cursor: pointer; padding: 8px; border-radius: 8px; }
.mobile-navigation summary::-webkit-details-marker { display: none; }
.mobile-navigation-links { position: absolute; right: 0; top: 45px; width: 200px; padding: 8px; border: 1px solid rgb(var(--ui-line)); border-radius: 12px; background: rgb(var(--ui-surface)); box-shadow: 0 12px 30px #00000012; }
.mobile-navigation-links a { display: block; padding: 12px; border-radius: 6px; font-size: 14px; }
.mobile-navigation-links a:hover { background: rgb(var(--ui-brand-soft)); }
.public-nav :is(a, button, summary):focus-visible { outline: 2px solid rgb(var(--ui-brand)); outline-offset: 4px; }
@media (max-width: 1023px) { .public-links { display: none; } .mobile-navigation { display: block; } }
@media (max-width: 639px) { .public-nav { padding: 16px; min-height: 72px; gap: 8px; } .public-brand { font-size: 16px; gap: 8px; } .public-brand span { max-width: 130px; } .public-brand img { width: 30px; height: 30px; } .public-actions { gap: 2px; } .header-login, .back-home { display: none; } }
@media (max-width: 359px) { .public-brand span { max-width: 88px; } }
</style>
