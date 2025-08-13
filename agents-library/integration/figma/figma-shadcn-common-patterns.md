# Common Patterns and Utilities

## Tailwind/ShadCN Integration Patterns

### Tailwind Class Generation
```typescript
class TailwindClassGenerator {
  // Convert Figma spacing to Tailwind spacing
  static convertSpacing(pixels: number, property: 'p' | 'm' | 'gap' | 'space'): string {
    const spacingMap: Record<number, string> = {
      0: '0',
      1: '0.5',
      2: '0.5',
      4: '1',
      6: '1.5',
      8: '2',
      10: '2.5',
      12: '3',
      14: '3.5',
      16: '4',
      20: '5',
      24: '6',
      28: '7',
      32: '8',
      36: '9',
      40: '10',
      44: '11',
      48: '12',
      56: '14',
      64: '16',
      80: '20',
      96: '24',
      112: '28',
      128: '32'
    };

    const closest = this.findClosestSpacing(pixels, spacingMap);
    return `${property}-${spacingMap[closest]}`;
  }

  // Convert Figma colors to Tailwind color classes
  static convertColor(
    color: string, 
    property: 'bg' | 'text' | 'border' | 'ring',
    opacity?: number
  ): string {
    const tailwindColor = this.mapColorToTailwind(color);
    const opacityClass = opacity && opacity < 1 ? `/${Math.round(opacity * 100)}` : '';
    return `${property}-${tailwindColor}${opacityClass}`;
  }

  // Convert Figma typography to Tailwind typography
  static convertTypography(typography: FigmaTypography): string[] {
    const classes: string[] = [];

    // Font size
    if (typography.fontSize) {
      classes.push(this.convertFontSize(typography.fontSize));
    }

    // Font weight
    if (typography.fontWeight) {
      classes.push(this.convertFontWeight(typography.fontWeight));
    }

    // Line height
    if (typography.lineHeight) {
      classes.push(this.convertLineHeight(typography.lineHeight, typography.fontSize));
    }

    // Letter spacing
    if (typography.letterSpacing) {
      classes.push(this.convertLetterSpacing(typography.letterSpacing));
    }

    return classes;
  }

  // Convert Figma layout to Flexbox classes
  static convertFlexLayout(layout: AutoLayoutProperties): string[] {
    const classes: string[] = ['flex'];

    // Direction
    if (layout.direction === 'vertical') {
      classes.push('flex-col');
    }

    // Justify content (main axis)
    switch (layout.alignment) {
      case 'start':
        classes.push('justify-start');
        break;
      case 'center':
        classes.push('justify-center');
        break;
      case 'end':
        classes.push('justify-end');
        break;
      case 'space-between':
        classes.push('justify-between');
        break;
      case 'space-around':
        classes.push('justify-around');
        break;
    }

    // Align items (cross axis)
    switch (layout.counterAlignment) {
      case 'start':
        classes.push('items-start');
        break;
      case 'center':
        classes.push('items-center');
        break;
      case 'end':
        classes.push('items-end');
        break;
      case 'stretch':
        classes.push('items-stretch');
        break;
    }

    // Gap
    if (layout.spacing > 0) {
      classes.push(this.convertSpacing(layout.spacing, 'gap'));
    }

    return classes;
  }

  private static findClosestSpacing(target: number, spacingMap: Record<number, string>): number {
    const spacingValues = Object.keys(spacingMap).map(Number);
    return spacingValues.reduce((prev, curr) => 
      Math.abs(curr - target) < Math.abs(prev - target) ? curr : prev
    );
  }

  private static mapColorToTailwind(color: string): string {
    // Convert hex/rgb to semantic Tailwind colors
    const colorMap: Record<string, string> = {
      '#000000': 'black',
      '#ffffff': 'white',
      '#f3f4f6': 'gray-100',
      '#e5e7eb': 'gray-200',
      '#d1d5db': 'gray-300',
      '#9ca3af': 'gray-400',
      '#6b7280': 'gray-500',
      '#374151': 'gray-700',
      '#1f2937': 'gray-800',
      '#111827': 'gray-900'
    };

    return colorMap[color.toLowerCase()] || this.generateCustomColor(color);
  }

  private static generateCustomColor(color: string): string {
    // Generate a custom color name based on hue
    const rgb = this.hexToRgb(color);
    if (!rgb) return 'gray-500';

    const hsl = this.rgbToHsl(rgb.r, rgb.g, rgb.b);
    const hue = Math.round(hsl.h * 360);

    if (hue >= 0 && hue < 30) return 'red-500';
    if (hue >= 30 && hue < 60) return 'orange-500';
    if (hue >= 60 && hue < 120) return 'yellow-500';
    if (hue >= 120 && hue < 180) return 'green-500';
    if (hue >= 180 && hue < 240) return 'blue-500';
    if (hue >= 240 && hue < 300) return 'purple-500';
    if (hue >= 300 && hue < 360) return 'pink-500';

    return 'gray-500';
  }
}
```

### ShadCN Component Composition
```typescript
class ComponentComposer {
  static composeButton(figmaButton: FigmaComponentDetails): ComponentComposition {
    const baseComponent = 'Button';
    const modifications: string[] = [];
    const wrappers: string[] = [];

    // Check if it needs icon support
    if (this.hasIcon(figmaButton)) {
      modifications.push('Add icon support with proper spacing');
    }

    // Check if it needs loading state
    if (this.hasLoadingState(figmaButton)) {
      modifications.push('Add loading spinner integration');
    }

    // Check if it needs custom sizes beyond ShadCN defaults
    const customSizes = this.extractCustomSizes(figmaButton);
    if (customSizes.length > 0) {
      modifications.push(`Add custom sizes: ${customSizes.join(', ')}`);
    }

    return {
      primary: baseComponent,
      supporting: this.hasIcon(figmaButton) ? ['Icon'] : [],
      wrappers,
      modifications,
      customElements: []
    };
  }

  static composeCard(figmaCard: FigmaComponentDetails): ComponentComposition {
    const children = figmaCard.children || [];
    const supporting: string[] = ['Card'];

    // Analyze card structure
    const hasHeader = children.some(child => 
      this.isHeaderElement(child)
    );
    const hasFooter = children.some(child => 
      this.isFooterElement(child)
    );
    const hasImage = children.some(child => 
      child.type === 'IMAGE' || this.hasImageContent(child)
    );

    if (hasHeader) supporting.push('CardHeader', 'CardTitle');
    if (hasFooter) supporting.push('CardFooter');
    supporting.push('CardContent');

    return {
      primary: 'Card',
      supporting,
      wrappers: [],
      modifications: [],
      customElements: hasImage ? [{
        type: 'image',
        requirements: ['Image optimization', 'Aspect ratio handling']
      }] : []
    };
  }

  static composeForm(figmaForm: FigmaComponentDetails): ComponentComposition {
    const formElements = this.extractFormElements(figmaForm);
    const supporting: string[] = ['Form'];

    formElements.forEach(element => {
      switch (element.type) {
        case 'input':
          supporting.push('FormField', 'FormLabel', 'FormControl', 'Input');
          break;
        case 'textarea':
          supporting.push('FormField', 'FormLabel', 'FormControl', 'Textarea');
          break;
        case 'select':
          supporting.push('FormField', 'FormLabel', 'Select');
          break;
        case 'checkbox':
          supporting.push('FormField', 'FormControl', 'Checkbox', 'FormLabel');
          break;
        case 'radio':
          supporting.push('FormField', 'FormControl', 'RadioGroup', 'RadioGroupItem', 'FormLabel');
          break;
      }
    });

    supporting.push('Button'); // Submit button

    return {
      primary: 'Form',
      supporting: [...new Set(supporting)], // Remove duplicates
      wrappers: [],
      modifications: ['Add form validation', 'Add error handling'],
      customElements: []
    };
  }

  private static hasIcon(component: FigmaComponentDetails): boolean {
    return component.children?.some(child => 
      child.type === 'VECTOR' || 
      child.name.toLowerCase().includes('icon') ||
      this.isIconComponent(child)
    ) || false;
  }

  private static extractFormElements(form: FigmaComponentDetails): FormElement[] {
    const elements: FormElement[] = [];
    
    const traverse = (node: FigmaComponentDetails) => {
      if (this.isFormInput(node)) {
        elements.push({
          type: this.inferInputType(node),
          name: node.name,
          required: this.isRequired(node),
          validation: this.extractValidation(node)
        });
      }

      node.children?.forEach(child => traverse(child));
    };

    traverse(form);
    return elements;
  }
}
```

### Responsive Design Patterns
```typescript
class ResponsivePatterns {
  static generateResponsiveClasses(
    breakpoints: Record<string, ComponentProperties>
  ): string[] {
    const classes: string[] = [];

    // Mobile-first approach
    const mobileProps = breakpoints.mobile || breakpoints.base;
    if (mobileProps) {
      classes.push(...this.propsToClasses(mobileProps));
    }

    // Add breakpoint-specific classes
    Object.entries(breakpoints).forEach(([breakpoint, props]) => {
      if (breakpoint === 'mobile' || breakpoint === 'base') return;

      const prefixedClasses = this.propsToClasses(props).map(cls => 
        `${breakpoint}:${cls}`
      );
      classes.push(...prefixedClasses);
    });

    return classes;
  }

  static generateContainerQueries(
    component: FigmaComponentDetails
  ): ContainerQueryConfig {
    const containers = this.findContainerBreakpoints(component);
    
    return {
      containerType: 'inline-size',
      queries: containers.map(container => ({
        minWidth: container.width,
        classes: this.generateClassesForWidth(container.width),
        modifications: container.modifications
      }))
    };
  }

  private static propsToClasses(props: ComponentProperties): string[] {
    const classes: string[] = [];

    if (props.width) classes.push(this.convertWidth(props.width));
    if (props.height) classes.push(this.convertHeight(props.height));
    if (props.padding) classes.push(...this.convertPadding(props.padding));
    if (props.margin) classes.push(...this.convertMargin(props.margin));
    if (props.display) classes.push(this.convertDisplay(props.display));

    return classes;
  }
}
```

### Accessibility Patterns
```typescript
class AccessibilityPatterns {
  static generateAriaAttributes(
    component: FigmaComponentDetails,
    componentType: string
  ): Record<string, string> {
    const attrs: Record<string, string> = {};

    switch (componentType) {
      case 'button':
        attrs['aria-label'] = this.extractButtonLabel(component);
        if (this.hasIcon(component) && !this.hasText(component)) {
          attrs['aria-label'] = attrs['aria-label'] || 'Button';
        }
        break;

      case 'input':
        attrs['aria-label'] = this.extractInputLabel(component);
        if (this.isRequired(component)) {
          attrs['aria-required'] = 'true';
        }
        break;

      case 'dialog':
        attrs['aria-modal'] = 'true';
        attrs['aria-labelledby'] = this.generateId('dialog-title');
        attrs['aria-describedby'] = this.generateId('dialog-description');
        break;

      case 'navigation':
        attrs['aria-label'] = 'Main navigation';
        break;
    }

    return attrs;
  }

  static generateKeyboardHandlers(componentType: string): KeyboardHandler[] {
    const handlers: KeyboardHandler[] = [];

    switch (componentType) {
      case 'button':
        handlers.push({
          key: 'Enter',
          action: 'click',
          preventDefault: true
        });
        handlers.push({
          key: ' ',
          action: 'click',
          preventDefault: true
        });
        break;

      case 'dialog':
        handlers.push({
          key: 'Escape',
          action: 'close',
          preventDefault: true
        });
        break;

      case 'dropdown':
        handlers.push({
          key: 'ArrowDown',
          action: 'navigate-next',
          preventDefault: true
        });
        handlers.push({
          key: 'ArrowUp',
          action: 'navigate-previous',
          preventDefault: true
        });
        break;
    }

    return handlers;
  }

  static validateColorContrast(
    foreground: string,
    background: string,
    fontSize?: number
  ): ContrastValidation {
    const contrast = this.calculateContrast(foreground, background);
    const isLargeText = fontSize ? fontSize >= 18 : false;
    const threshold = isLargeText ? 3.0 : 4.5;

    return {
      ratio: contrast,
      passes: contrast >= threshold,
      level: contrast >= 7.0 ? 'AAA' : contrast >= threshold ? 'AA' : 'fail',
      recommendation: contrast < threshold 
        ? this.suggestColorAdjustment(foreground, background, threshold)
        : null
    };
  }
}
```

### Code Generation Patterns
```typescript
class CodeGenerator {
  static generateComponent(spec: ComponentSpec): GeneratedComponent {
    const imports = this.generateImports(spec);
    const interfaces = this.generateInterfaces(spec);
    const variants = this.generateVariants(spec);
    const component = this.generateComponentCode(spec);
    const exports = this.generateExports(spec);

    return {
      name: spec.name,
      sourceCode: [imports, interfaces, variants, component, exports]
        .filter(Boolean)
        .join('

'),
      dependencies: spec.dependencies,
      variants: spec.variants,
      examples: this.generateExamples(spec),
      documentation: this.generateDocumentation(spec)
    };
  }

  private static generateImports(spec: ComponentSpec): string {
    const imports: string[] = [
      `import * as React from "react"`,
      `import { cn } from "@/lib/utils"`
    ];

    // Add conditional imports
    if (spec.hasVariants) {
      imports.push(`import { cva, type VariantProps } from "class-variance-authority"`);
    }

    if (spec.needsForwardRef) {
      // Already included in React import
    }

    if (spec.needsSlot) {
      imports.push(`import { Slot } from "@radix-ui/react-slot"`);
    }

    // Add component-specific imports
    spec.dependencies.forEach(dep => {
      if (dep.type === 'shadcn') {
        imports.push(`import { ${dep.name} } from "@/components/ui/${dep.name.toLowerCase()}"`);
      }
    });

    return imports.join('
');
  }

  private static generateVariants(spec: ComponentSpec): string | null {
    if (!spec.hasVariants || !spec.variants.length) return null;

    const baseClasses = spec.baseClasses.join(' ');
    const variants = spec.variants.map(variant => {
      const options = Object.entries(variant.options)
        .map(([key, value]) => `        ${key}: "${value}"`)
        .join(',
');
      
      return `      ${variant.name}: {
${options}
      }`;
    }).join(',
');

    const defaultVariants = spec.variants
      .map(variant => `      ${variant.name}: "${variant.default}"`)
      .join(',
');

    return `const ${spec.name.toLowerCase()}Variants = cva(
  "${baseClasses}",
  {
    variants: {
${variants}
    },
    defaultVariants: {
${defaultVariants}
    },
  }
)`;
  }

  private static generateComponentCode(spec: ComponentSpec): string {
    const propsInterface = `${spec.name}Props`;
    const elementType = spec.elementType || 'HTMLDivElement';
    const elementTag = spec.elementTag || 'div';

    let componentCode = `const ${spec.name} = React.forwardRef<
  ${elementType},
  ${propsInterface}
>(({ className`;

    // Add variant props
    if (spec.hasVariants) {
      spec.variants.forEach(variant => {
        componentCode += `, ${variant.name} = "${variant.default}"`;
      });
    }

    // Add other props
    if (spec.needsAsChild) {
      componentCode += `, asChild = false`;
    }

    componentCode += `, ...props }, ref) => {
`;

    // Component body
    if (spec.needsAsChild) {
      componentCode += `  const Comp = asChild ? Slot : "${elementTag}"
`;
    }

    componentCode += `  return (
    <${spec.needsAsChild ? 'Comp' : elementTag}
      ref={ref}
      className={cn(${this.generateClassNames(spec)})}`;

    // Add accessibility attributes
    if (spec.accessibility?.length) {
      spec.accessibility.forEach(attr => {
        componentCode += `
      ${attr.name}={${attr.value}}`;
      });
    }

    componentCode += `
      {...props}
    `;

    // Add children
    if (spec.children) {
      componentCode += `>
      ${spec.children}
    `;
    } else {
      componentCode += `/>
  `;
    }

    componentCode += `
  )
})`;

    // Add display name
    componentCode += `
${spec.name}.displayName = "${spec.name}"`;

    return componentCode;
  }

  private static generateClassNames(spec: ComponentSpec): string {
    if (spec.hasVariants) {
      const variantProps = spec.variants.map(v => v.name).join(', ');
      return `${spec.name.toLowerCase()}Variants({ ${variantProps}, className })`;
    } else {
      const baseClasses = spec.baseClasses.map(cls => `"${cls}"`).join(', ');
      return `${baseClasses}, className`;
    }
  }
}
```

### Project Structure Patterns
```typescript
class ProjectStructure {
  static generateNextJSSaaSStructure(config: ProjectConfig): FileStructure {
    return {
      'src/': {
        'app/': this.generateAppStructure(config),
        'components/': {
          'ui/': this.generateUIComponents(config.components),
          'features/': this.generateFeatureComponents(config.features),
          'layouts/': this.generateLayoutComponents()
        },
        'lib/': {
          'utils.ts': this.generateUtilsFile(),
          'auth/': this.generateAuthFiles(config.auth),
          'db/': this.generateDBFiles(config.database)
        },
        'hooks/': this.generateCustomHooks(config.hooks),
        'types/': this.generateTypeDefinitions(config),
        'styles/': {
          'globals.css': this.generateGlobalStyles(config.design),
          'components.css': this.generateComponentStyles()
        }
      },
      'components.json': this.generateComponentsConfig(),
      'tailwind.config.js': this.generateTailwindConfig(config.design),
      'package.json': this.updatePackageJson(config.dependencies)
    };
  }

  private static generateUIComponents(components: ComponentSpec[]): Record<string, string> {
    const files: Record<string, string> = {};

    components.forEach(component => {
      const fileName = `${component.name.toLowerCase().replace(/([A-Z])/g, '-$1').slice(1)}.tsx`;
      files[fileName] = CodeGenerator.generateComponent(component).sourceCode;
    });

    return files;
  }
}
```