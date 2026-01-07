/** @type {import('tailwindcss').Config} */
module.exports = {
    darkMode: 'class',
    content: [
        './templates/**/*.html',
        './app_*/templates/**/*.html',
        './app_*/forms.py',  // Include Python form files for Tailwind classes
    ],
    theme: {
        extend: {
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
            colors: {
                border: "hsl(var(--border))",
                input: "hsl(var(--input))",
                ring: "hsl(var(--ring))",
                background: "hsl(var(--background))",
                foreground: "hsl(var(--foreground))",
                primary: {
                    DEFAULT: "hsl(var(--primary))",
                    foreground: "hsl(var(--primary-foreground))",
                },
                secondary: {
                    DEFAULT: "hsl(var(--secondary))",
                    foreground: "hsl(var(--secondary-foreground))",
                },
                destructive: {
                    DEFAULT: "hsl(var(--destructive))",
                    foreground: "hsl(var(--destructive-foreground))",
                },
                muted: {
                    DEFAULT: "hsl(var(--muted))",
                    foreground: "hsl(var(--muted-foreground))",
                },
                accent: {
                    DEFAULT: "hsl(var(--accent))",
                    foreground: "hsl(var(--accent-foreground))",
                },
                popover: {
                    DEFAULT: "hsl(var(--popover))",
                    foreground: "hsl(var(--popover-foreground))",
                },
                card: {
                    DEFAULT: "hsl(var(--card))",
                    foreground: "hsl(var(--card-foreground))",
                },
                // Status Colors
                status: {
                    yellow: "hsl(45 93% 47%)",
                    blue: "hsl(217 91% 60%)",
                    orange: "hsl(25 95% 53%)",
                    red: "hsl(0 84% 60%)",
                    emerald: "hsl(160 84% 39%)",
                },
                // AWS Custom Colors
                aws: {
                    orange: "hsl(var(--aws-orange))",
                    light: "hsl(var(--aws-orange-light))",
                    dark: "hsl(var(--aws-dark))",
                    darker: "hsl(var(--aws-darker))",
                },
                success: "hsl(var(--success))",
                warning: "hsl(var(--warning))",
                info: "hsl(var(--info))",
            },
            borderRadius: {
                lg: "var(--radius)",
                md: "calc(var(--radius) - 2px)",
                sm: "calc(var(--radius) - 4px)",
            },
            backgroundImage: {
                'gradient-primary': 'linear-gradient(135deg, hsl(var(--aws-orange)) 0%, hsl(var(--aws-orange-light)) 100%)',
                'gradient-dark': 'linear-gradient(180deg, hsl(var(--aws-dark)) 0%, hsl(var(--aws-darker)) 100%)',
                'gradient-card': 'linear-gradient(135deg, hsl(220 14% 98%) 0%, hsl(220 14% 96%) 100%)',
            },
            boxShadow: {
                'glow': '0 0 40px hsl(24 95% 53% / 0.15)',
                'glow-lg': '0 0 60px hsl(24 95% 53% / 0.25)',
                'card': '0 4px 24px -4px hsl(222 47% 11% / 0.1)',
            },
            keyframes: {
                'accordion-down': {
                    from: { height: '0' },
                    to: { height: 'var(--radix-accordion-content-height)' },
                },
                'accordion-up': {
                    from: { height: 'var(--radix-accordion-content-height)' },
                    to: { height: '0' },
                },
                shimmer: {
                    '0%': { backgroundPosition: '-200% 0' },
                    '100%': { backgroundPosition: '200% 0' },
                },
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-10px)' },
                },
                fadeIn: {
                    from: { opacity: '0' },
                    to: { opacity: '1' },
                },
                slideUp: {
                    from: { transform: 'translateY(20px)', opacity: '0' },
                    to: { transform: 'translateY(0)', opacity: '1' },
                },
                scaleIn: {
                    from: { transform: 'scale(0.95)', opacity: '0' },
                    to: { transform: 'scale(1)', opacity: '1' },
                },
            },
            animation: {
                'accordion-down': 'accordion-down 0.2s ease-out',
                'accordion-up': 'accordion-up 0.2s ease-out',
                'shimmer': 'shimmer 2s infinite linear',
                'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
                'float': 'float 3s ease-in-out infinite',
                'fade-in': 'fadeIn 0.5s ease-out',
                'slide-up': 'slideUp 0.5s ease-out',
                'scale-in': 'scaleIn 0.3s ease-out',
            },
        },
    },
    plugins: [],
}
