import { computed } from 'vue'
import { useRoute } from 'vue-router'

const consolePaths = new Set([
  '/dashboard', '/keys', '/usage', '/monitor', '/available-channels',
  '/purchase', '/orders', '/subscriptions', '/redeem',
  '/profile', '/affiliate', '/ip-allowlist',
  '/payment/qrcode', '/payment/result', '/payment/stripe', '/payment/airwallex',
])

export function useConsoleWorkspace() {
  const route = useRoute()
  const isAdminConsole = computed(() => (route.matched.at(-1)?.path || route.path).startsWith('/admin/'))
  const isConsoleWorkspace = computed(() => isAdminConsole.value || consolePaths.has(route.matched.at(-1)?.path || route.path))

  return { isConsoleWorkspace, isAdminConsole }
}
