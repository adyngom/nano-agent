# Figma to ShadCN Theme Conversion Map

## Overview
This document defines the conversion map for translating Figma design tokens into ShadCN-compatible theme CSS files.

## Color Format Conversion

### Input: Figma Color Tokens
Figma provides colors in various formats:
- Hex: `#FF5733`
- RGB: `rgb(255, 87, 51)`
- RGBA: `rgba(255, 87, 51, 0.8)`

### Output: ShadCN CSS Variables
ShadCN expects colors in one of two formats:

1. **HSL Format** (preferred for default themes):
   ```css
   --primary: 240 5.9% 10%;  /* No hsl() wrapper, space-separated */
   ```

2. **OKLCH Format** (for advanced color spaces):
   ```css
   --primary: oklch(0.723 0.219 149.579);
   ```

## Required CSS Variables

### Core Color Variables
Each theme must define these variables:

```css
:root {
  /* Background and foreground pairs */
  --background: [hsl-values];
  --foreground: [hsl-values];
  
  /* Component-specific pairs */
  --card: [hsl-values];
  --card-foreground: [hsl-values];
  --popover: [hsl-values];
  --popover-foreground: [hsl-values];
  
  /* Semantic colors */
  --primary: [hsl-values];
  --primary-foreground: [hsl-values];
  --secondary: [hsl-values];
  --secondary-foreground: [hsl-values];
  --muted: [hsl-values];
  --muted-foreground: [hsl-values];
  --accent: [hsl-values];
  --accent-foreground: [hsl-values];
  --destructive: [hsl-values];
  --destructive-foreground: [hsl-values];
  
  /* UI elements */
  --border: [hsl-values];
  --input: [hsl-values];
  --ring: [hsl-values];
  
  /* Border radius */
  --radius: 0.5rem;
  
  /* Chart colors (optional) */
  --chart-1: [hsl-values];
  --chart-2: [hsl-values];
  --chart-3: [hsl-values];
  --chart-4: [hsl-values];
  --chart-5: [hsl-values];
  
  /* Sidebar colors (optional) */
  --sidebar-background: [hsl-values];
  --sidebar-foreground: [hsl-values];
  --sidebar-primary: [hsl-values];
  --sidebar-primary-foreground: [hsl-values];
  --sidebar-accent: [hsl-values];
  --sidebar-accent-foreground: [hsl-values];
  --sidebar-border: [hsl-values];
  --sidebar-ring: [hsl-values];
}
```

## Conversion Functions

### Hex to HSL Conversion
```typescript
function hexToHSL(hex: string): string {
  // Remove # if present
  hex = hex.replace('#', '');
  
  // Convert to RGB
  const r = parseInt(hex.substr(0, 2), 16) / 255;
  const g = parseInt(hex.substr(2, 2), 16) / 255;
  const b = parseInt(hex.substr(4, 2), 16) / 255;
  
  // Find min and max values
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const diff = max - min;
  
  // Calculate lightness
  const l = (max + min) / 2;
  
  // Calculate saturation
  let s = 0;
  if (diff !== 0) {
    s = diff / (1 - Math.abs(2 * l - 1));
  }
  
  // Calculate hue
  let h = 0;
  if (diff !== 0) {
    if (max === r) {
      h = ((g - b) / diff + (g < b ? 6 : 0)) / 6;
    } else if (max === g) {
      h = ((b - r) / diff + 2) / 6;
    } else {
      h = ((r - g) / diff + 4) / 6;
    }
  }
  
  // Convert to degrees and percentages
  h = Math.round(h * 360);
  s = Math.round(s * 100);
  const lPercent = Math.round(l * 100);
  
  // Return space-separated HSL values (ShadCN format)
  return `${h} ${s}% ${lPercent}%`;
}
```

## Mapping Strategy

### 1. Primary Color Mapping
```typescript
interface ColorMapping {
  figmaToken: string;      // e.g., "Brand/Primary/500"
  shadcnVariable: string;  // e.g., "--primary"
  contrastPair?: string;   // e.g., "--primary-foreground"
}

const primaryColorMap: ColorMapping[] = [
  {
    figmaToken: "Brand/Primary/500",
    shadcnVariable: "--primary",
    contrastPair: "--primary-foreground"
  },
  {
    figmaToken: "Brand/Secondary/500", 
    shadcnVariable: "--secondary",
    contrastPair: "--secondary-foreground"
  }
];
```

### 2. Background/Surface Mapping
```typescript
const surfaceColorMap: ColorMapping[] = [
  {
    figmaToken: "Surface/Background",
    shadcnVariable: "--background",
    contrastPair: "--foreground"
  },
  {
    figmaToken: "Surface/Card",
    shadcnVariable: "--card",
    contrastPair: "--card-foreground"
  },
  {
    figmaToken: "Surface/Popover",
    shadcnVariable: "--popover", 
    contrastPair: "--popover-foreground"
  }
];
```

### 3. State Color Mapping
```typescript
const stateColorMap: ColorMapping[] = [
  {
    figmaToken: "Feedback/Error/500",
    shadcnVariable: "--destructive",
    contrastPair: "--destructive-foreground"
  },
  {
    figmaToken: "State/Hover",
    shadcnVariable: "--accent",
    contrastPair: "--accent-foreground"
  },
  {
    figmaToken: "State/Disabled",
    shadcnVariable: "--muted",
    contrastPair: "--muted-foreground"
  }
];
```

### 4. UI Element Mapping
```typescript
const uiElementMap: ColorMapping[] = [
  {
    figmaToken: "Border/Default",
    shadcnVariable: "--border"
  },
  {
    figmaToken: "Input/Border",
    shadcnVariable: "--input"
  },
  {
    figmaToken: "Focus/Ring",
    shadcnVariable: "--ring"
  }
];
```

## Automatic Contrast Color Generation

When a foreground color is not explicitly defined in Figma, generate it automatically:

```typescript
function generateContrastColor(backgroundColor: string): string {
  const hsl = parseHSL(backgroundColor);
  
  // Calculate relative luminance
  const luminance = calculateLuminance(hsl);
  
  // Use WCAG guidelines for contrast
  if (luminance > 0.5) {
    // Light background - use dark text
    return "240 10% 3.9%"; // Near black
  } else {
    // Dark background - use light text
    return "0 0% 98%"; // Near white
  }
}
```

## Theme Generation Workflow

1. **Extract Figma Tokens**
   - Use `design-token-extractor` to get all color tokens
   - Organize by semantic purpose

2. **Map to ShadCN Variables**
   - Apply mapping rules defined above
   - Generate contrast pairs automatically if needed

3. **Convert Color Formats**
   - Convert all colors to HSL format
   - Ensure space-separated values without wrappers

4. **Generate Theme Files**
   - Create `:root` and `.dark` selectors
   - Include all required CSS variables
   - Add optional variables based on available tokens

5. **Validate Output**
   - Check contrast ratios (WCAG AA compliance)
   - Ensure all required variables are present
   - Verify color format consistency

## Example Conversion

### Input: Figma Design Tokens
```json
{
  "colors": {
    "brand": {
      "primary": "#3B82F6",
      "secondary": "#8B5CF6"
    },
    "surface": {
      "background": "#FFFFFF",
      "card": "#F9FAFB"
    },
    "feedback": {
      "error": "#EF4444",
      "success": "#10B981"
    }
  }
}
```

### Output: ShadCN Theme CSS
```css
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --card: 210 20% 98%;
  --card-foreground: 240 10% 3.9%;
  --primary: 217 91% 60%;
  --primary-foreground: 0 0% 98%;
  --secondary: 262 83% 58%;
  --secondary-foreground: 0 0% 98%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 98%;
  /* ... other required variables ... */
}

.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  /* ... dark theme overrides ... */
}
```

## Integration Points

### 1. Design Token Extractor Updates
- Add HSL conversion functionality
- Support automatic contrast pair generation
- Implement semantic token recognition

### 2. Tailwind Config Agent Updates
- Generate HSL-based color configurations
- Remove RGB wrapper format
- Support both HSL and OKLCH formats

### 3. Theme System Manager Updates
- Generate proper ShadCN theme file structure
- Implement dark theme generation logic
- Add theme validation for required variables