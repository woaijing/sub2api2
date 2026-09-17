/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // FoxCode 品牌色：陶土橙
        primary: {
          50: '#fff7f2',
          100: '#fbe9e2',
          200: '#f6d2c5',
          300: '#e9b7a5',
          400: '#e99a7c',
          500: '#d97757',
          600: '#c66646',
          700: '#b85c3e',
          800: '#9e4932',
          900: '#7d3928',
          950: '#4a2d25'
        },
        // FoxCode 辅助色：暖棕灰
        accent: {
          50: '#faf9f5',
          100: '#f5f1ec',
          200: '#e7ded6',
          300: '#c9bdb4',
          400: '#a99489',
          500: '#6f625a',
          600: '#594d46',
          700: '#463c36',
          800: '#322823',
          900: '#26201d',
          950: '#1b1715'
        },
        // 深色模式背景（暖棕黑灰）
        dark: {
          50: '#fff7f2',
          100: '#f5e8e1',
          200: '#e2cec4',
          300: '#c9b8af',
          400: '#a99287',
          500: '#80685c',
          600: '#604e43',
          700: '#4a3a33',
          800: '#322823',
          900: '#26201d',
          950: '#1b1715'
        },
        ui: {
          page: 'rgb(var(--ui-page) / <alpha-value>)',
          surface: 'rgb(var(--ui-surface) / <alpha-value>)',
          muted: 'rgb(var(--ui-surface-muted) / <alpha-value>)',
          line: 'rgb(var(--ui-line) / <alpha-value>)',
          control: 'rgb(var(--ui-control-line) / <alpha-value>)',
          ink: 'rgb(var(--ui-ink) / <alpha-value>)',
          'ink-muted': 'rgb(var(--ui-ink-muted) / <alpha-value>)',
          brand: 'rgb(var(--ui-brand) / <alpha-value>)',
          'brand-hover': 'rgb(var(--ui-brand-hover) / <alpha-value>)',
          'brand-soft': 'rgb(var(--ui-brand-soft) / <alpha-value>)',
          'brand-strong': 'rgb(var(--ui-brand-strong) / <alpha-value>)',
          'on-brand': 'rgb(var(--ui-on-brand) / <alpha-value>)',
          action: 'rgb(var(--ui-action) / <alpha-value>)',
          'action-hover': 'rgb(var(--ui-action-hover) / <alpha-value>)',
          accent: 'rgb(var(--ui-accent) / <alpha-value>)'
        }
      },
      fontFamily: {
        sans: [
          'system-ui',
          '-apple-system',
          'BlinkMacSystemFont',
          'Segoe UI',
          'Roboto',
          'Helvetica Neue',
          'Arial',
          'PingFang SC',
          'Hiragino Sans GB',
          'Microsoft YaHei',
          'sans-serif'
        ],
        mono: ['ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', 'monospace']
      },
      boxShadow: {
        glass: '0 8px 32px rgba(0, 0, 0, 0.08)',
        'glass-sm': '0 4px 16px rgba(0, 0, 0, 0.06)',
        glow: '0 0 20px rgba(217, 119, 87, 0.15)',
        'glow-lg': '0 0 40px rgba(217, 119, 87, 0.20)',
        card: '0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.06)',
        'card-hover': '0 10px 40px rgba(0, 0, 0, 0.08)',
        'inner-glow': 'inset 0 1px 0 rgba(255, 255, 255, 0.1)'
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-primary': 'linear-gradient(135deg, #d97757 0%, #b85c3e 100%)',
        'gradient-dark': 'linear-gradient(135deg, #322823 0%, #1b1715 100%)',
        'gradient-glass':
          'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
        'mesh-gradient':
          'radial-gradient(at 40% 20%, rgba(217, 119, 87, 0.10) 0px, transparent 50%), radial-gradient(at 80% 0%, rgba(233, 183, 165, 0.08) 0px, transparent 50%), radial-gradient(at 0% 50%, rgba(217, 119, 87, 0.06) 0px, transparent 50%)'
      },
      animation: {
        'fade-in': 'fadeIn 0.3s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'slide-in-right': 'slideInRight 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        shimmer: 'shimmer 2s linear infinite',
        glow: 'glow 2s ease-in-out infinite alternate'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideDown: {
          '0%': { opacity: '0', transform: 'translateY(-10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' }
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.95)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        },
        shimmer: {
          '0%': { backgroundPosition: '-200% 0' },
          '100%': { backgroundPosition: '200% 0' }
        },
        glow: {
          '0%': { boxShadow: '0 0 20px rgba(217, 119, 87, 0.20)' },
          '100%': { boxShadow: '0 0 30px rgba(217, 119, 87, 0.34)' }
        }
      },
      backdropBlur: {
        xs: '2px'
      },
      borderRadius: {
        '4xl': '2rem'
      }
    }
  },
  plugins: []
}
