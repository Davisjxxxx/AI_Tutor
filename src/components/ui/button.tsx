import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap text-sm font-medium transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-opacity-50 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-gradient-primary text-primary-foreground rounded-xl px-6 py-3 shadow-glow hover:scale-105 hover:shadow-[0_6px_30px_hsl(var(--primary)/0.4)] active:scale-95",
        secondary: "glass-button text-foreground hover:bg-glass-strong hover:text-primary-foreground",
        ghost: "rounded-xl px-4 py-2 text-foreground hover:glass hover:text-primary-foreground transition-all duration-200",
        outline: "rounded-xl px-6 py-3 border border-glass-border glass hover:bg-primary hover:text-primary-foreground hover:border-primary transition-all duration-300",
        glass: "glass-button text-foreground hover:shadow-glow hover:border-primary",
        hero: "bg-gradient-primary text-primary-foreground rounded-xl px-8 py-4 text-lg font-semibold shadow-glow hover:scale-105 hover:shadow-[0_8px_40px_hsl(var(--primary)/0.5)] transition-all duration-300 animate-pulse-glow",
        destructive: "bg-destructive text-primary-foreground rounded-xl px-6 py-3 hover:bg-destructive/90 hover:scale-105 transition-all duration-200",
        link: "text-primary underline-offset-4 hover:underline p-0",
      },
      size: {
        default: "h-11 px-6",
        sm: "h-9 px-4 text-sm",
        lg: "h-12 px-8 text-base",
        xl: "h-14 px-10 text-lg",
        icon: "h-11 w-11",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
