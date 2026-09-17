import { computed, ref } from 'vue'
import { useMutationObserver } from '@vueuse/core'

export function useChartTheme() {
  const root = document.documentElement
  const revision = ref(0)

  // Canvas colors must be resolved again when the CSS theme changes.
  useMutationObserver(root, () => { revision.value++ }, {
    attributes: true,
    attributeFilter: ['class', 'style']
  })

  return computed(() => {
    void revision.value
    const styles = getComputedStyle(root)
    const dark = root.classList.contains('dark')
    const color = (name: string, fallback: string) => {
      const value = styles.getPropertyValue(name).trim()
      return value ? `rgb(${value})` : fallback
    }

    return {
      text: color('--ui-ink-muted', dark ? '#c9b8af' : '#6f625a'),
      grid: color('--ui-line', dark ? '#4a3a33' : '#e7ded6')
    }
  })
}
