import { computed, ref } from 'vue'
import { useMutationObserver } from '@vueuse/core'
import { useAppStore, useAuthStore } from '@/stores'
import { sanitizeUrl } from '@/utils/url'
import { FeatureFlags, isFeatureFlagEnabled } from '@/utils/featureFlags'

/** Presentation settings for public pages; access control remains in the router. */
export function usePublicBrand() {
  const app = useAppStore()
  const auth = useAuthStore()
  const settings = computed(() => app.cachedPublicSettings)
  const siteName = computed(() => settings.value?.site_name || app.siteName || 'Sub2API')
  const siteLogo = computed(() => sanitizeUrl(settings.value?.site_logo || app.siteLogo || '', { allowRelative: true, allowDataUrl: true }))
  const docUrl = computed(() => sanitizeUrl(settings.value?.doc_url || app.docUrl || ''))
  const isAuthenticated = computed(() => auth.isAuthenticated)
  const dashboardPath = computed(() => auth.isAdmin ? '/admin/dashboard' : '/dashboard')
  const canRegister = computed(() => settings.value?.registration_enabled === true && settings.value?.backend_mode_enabled !== true)
  const showModelPlaza = computed(() => isFeatureFlagEnabled(FeatureFlags.modelPlaza) && (auth.isAuthenticated || settings.value?.model_plaza_require_auth !== true))
  const startPath = computed(() => isAuthenticated.value ? dashboardPath.value : canRegister.value ? '/register' : '/login')
  const root = document.documentElement
  const isDark = ref(root.classList.contains('dark'))
  useMutationObserver(root, () => { isDark.value = root.classList.contains('dark') }, { attributes: true, attributeFilter: ['class'] })

  function toggleTheme() {
    const dark = !root.classList.contains('dark')
    root.classList.toggle('dark', dark)
    localStorage.setItem('theme', dark ? 'dark' : 'light')
    isDark.value = dark
  }

  return { siteName, siteLogo, docUrl, isAuthenticated, dashboardPath, canRegister, showModelPlaza, startPath, isDark, toggleTheme }
}
