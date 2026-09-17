<template>
  <header class="sticky top-0 z-30 border-b border-ui-line bg-ui-surface">
    <nav class="mx-auto flex min-h-16 max-w-[1448px] items-center justify-between gap-3 px-4 py-3 sm:px-6">
      <RouterLink to="/home" class="flex min-w-0 items-center gap-2.5 text-ui-ink">
        <img :src="siteLogo || '/logo.svg'" :alt="siteName" class="h-9 w-9 shrink-0 rounded-lg object-contain" />
        <span class="min-w-0 break-words text-base font-semibold leading-5 [overflow-wrap:anywhere]">{{ siteName }}</span>
      </RouterLink>
      <div class="flex shrink-0 items-center gap-2">
        <LocaleSwitcher />
        <button type="button" class="flex h-9 w-9 items-center justify-center rounded-lg border border-ui-line text-ui-ink-muted transition-colors hover:bg-ui-muted focus-visible:outline focus-visible:outline-2 focus-visible:outline-ui-brand" :title="themeLabel" :aria-label="themeLabel" @click="toggleTheme">
          <Icon :name="isDark ? 'sun' : 'moon'" size="md" />
        </button>
        <RouterLink :to="isAuthenticated ? backTarget : { path: '/login', query: { redirect: '/model-plaza' } }" class="btn btn-primary max-w-36 px-3 py-2 text-center text-sm">
          {{ isAuthenticated ? t('modelPlaza.nav.backToDashboard') : t('modelPlaza.nav.login') }}
        </RouterLink>
      </div>
    </nav>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import Icon from '@/components/icons/Icon.vue'
import LocaleSwitcher from '@/components/common/LocaleSwitcher.vue'
import { sanitizeUrl } from '@/utils/url'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'

const { t } = useI18n()
const appStore = useAppStore()
const authStore = useAuthStore()
const settings = computed(() => appStore.cachedPublicSettings)
const siteName = computed(() => settings.value?.site_name || 'Sub2API')
const siteLogo = computed(() => sanitizeUrl(settings.value?.site_logo || '', { allowRelative: true, allowDataUrl: true }))
const isAuthenticated = computed(() => authStore.isAuthenticated)
const backTarget = computed(() => authStore.isAdmin ? '/admin/dashboard' : '/dashboard')
const isDark = ref(document.documentElement.classList.contains('dark'))
const themeLabel = computed(() => t(isDark.value ? 'nav.lightMode' : 'nav.darkMode'))

function toggleTheme() {
  isDark.value = !isDark.value
  document.documentElement.classList.toggle('dark', isDark.value)
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
}
</script>
