import { computed } from 'vue'
import { useRoute } from 'vue-router'

const consolePaths = new Set(['/dashboard', '/keys', '/usage'])

export function useConsoleWorkspace() {
  const route = useRoute()
  const isConsoleWorkspace = computed(() => consolePaths.has(route.matched.at(-1)?.path || route.path))

  return { isConsoleWorkspace }
}
