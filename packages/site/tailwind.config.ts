import type { Config } from 'tailwindcss';
export default { content: ['./index.html','./src/**/*.{ts,tsx}'], theme: { extend: { colors: { arena: { bg:'#070b16', card:'#0f172a', line:'#23314f', cyan:'#67e8f9', violet:'#a78bfa', amber:'#fbbf24' } } } }, plugins: [] } satisfies Config;
