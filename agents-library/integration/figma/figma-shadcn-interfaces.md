# Shared TypeScript Interfaces

## Core Data Structures

### Figma Data Types
```typescript
interface FigmaComponentDetails {
  id: string;
  name: string;
  type: 'COMPONENT' | 'COMPONENT_SET' | 'INSTANCE';
  description?: string;
  variants: ComponentVariant[];
  properties: ComponentProperty[];
  layout: LayoutProperties;
  styles: ComputedStyles;
  children: FigmaComponentDetails[];
  interactions: InteractionProperties[];
}

interface ComponentVariant {
  id: string;
  name: string;
  properties: Record<string, string>;
  styles: ComputedStyles;
}

interface LayoutProperties {
  width: number | 'auto' | 'fill';
  height: number | 'auto' | 'fill';
  constraints: {
    horizontal: 'left' | 'center' | 'right' | 'stretch' | 'scale';
    vertical: 'top' | 'center' | 'bottom' | 'stretch' | 'scale';
  };
  autoLayout?: AutoLayoutProperties;
  positioning?: PositioningProperties;
}

interface AutoLayoutProperties {
  direction: 'horizontal' | 'vertical';
  spacing: number;
  padding: PaddingValue;
  alignment: 'start' | 'center' | 'end' | 'stretch' | 'space-between' | 'space-around';
  counterAlignment: 'start' | 'center' | 'end' | 'stretch';
  wrap: boolean;
}

interface PaddingValue {
  top: number;
  right: number;
  bottom: number;
  left: number;
}
```

### Design Token System
```typescript
interface DesignTokenSystem {
  colors: ColorTokens;
  typography: TypographyTokens;
  spacing: SpacingTokens;
  effects: EffectTokens;
  components: ComponentTokens;
}

interface ColorTokens {
  primitives: ColorPrimitive[];
  semantic: SemanticColor[];
  themes: ThemeVariation[];
  aliases: ColorAlias[];
}

interface ColorPrimitive {
  name: string;
  value: string; // hex, rgb, hsl
  description?: string;
}

interface SemanticColor {
  name: string; // primary, secondary, success, warning, error
  light: string;
  dark: string;
  variants?: Record<string, string>; // 50, 100, 200, etc.
}

interface TypographyTokens {
  families: FontFamily[];
  scales: TypographyScale[];
  weights: FontWeight[];
  lineHeights: LineHeight[];
  letterSpacing: LetterSpacing[];
}

interface TypographyScale {
  name: string; // xs, sm, base, lg, xl, 2xl, etc.
  fontSize: string;
  lineHeight: string;
  letterSpacing?: string;
  fontWeight?: string;
}
```

### ShadCN Component Mapping
```typescript
interface ShadCNComponent {
  name: string;
  category: 'form' | 'navigation' | 'feedback' | 'data-display' | 'layout' | 'overlay';
  dependencies: string[];
  variants: ComponentVariantDefinition[];
  examples: ComponentExample[];
  accessibility: AccessibilityFeatures;
  customizable: CustomizationOptions;
}

interface ComponentVariantDefinition {
  name: string;
  description: string;
  props: PropDefinition[];
  styles: TailwindClasses;
}

interface PropDefinition {
  name: string;
  type: string;
  required: boolean;
  default?: any;
  description: string;
}

interface ShadCNMatch {
  component: ShadCNComponent;
  confidence: number; // 0-1
  modifications: ModificationRequirement[];
  composition: ComponentComposition;
}

interface ComponentComposition {
  primary: string; // Main ShadCN component
  supporting: string[]; // Additional components needed
  wrappers: string[]; // Container components
  customElements: CustomElementSpec[];
}
```

### Generated Component Structure
```typescript
interface GeneratedComponent {
  name: string;
  filePath: string;
  sourceCode: string;
  dependencies: ComponentDependency[];
  variants: GeneratedVariant[];
  examples: ComponentExample[];
  documentation: ComponentDocumentation;
  tests: ComponentTest[];
  accessibility: AccessibilityValidation;
  performance: PerformanceMetrics;
}

interface ComponentDependency {
  name: string;
  version?: string;
  type: 'peer' | 'dev' | 'runtime';
  source: 'npm' | 'internal' | 'shadcn';
}

interface GeneratedVariant {
  name: string;
  props: Record<string, any>;
  classes: string;
  description: string;
}

interface ComponentDocumentation {
  description: string;
  usage: string[];
  props: PropDocumentation[];
  examples: string[];
  accessibility: string[];
  notes?: string[];
}
```

### Tailwind Configuration
```typescript
interface TailwindConfiguration {
  theme: {
    extend: {
      colors: ColorConfiguration;
      fontFamily: FontFamilyConfiguration;
      fontSize: FontSizeConfiguration;
      spacing: SpacingConfiguration;
      borderRadius: BorderRadiusConfiguration;
      boxShadow: ShadowConfiguration;
      animation: AnimationConfiguration;
    };
  };
  plugins: TailwindPlugin[];
  content: string[];
  darkMode: 'class' | 'media';
  safelist: SafelistConfiguration;
}

interface ColorConfiguration {
  [key: string]: string | {
    50: string;
    100: string;
    200: string;
    300: string;
    400: string;
    500: string;
    600: string;
    700: string;
    800: string;
    900: string;
    950: string;
  };
}
```

### Project Architecture
```typescript
interface ProjectArchitecture {
  framework: 'nextjs-app-router' | 'nextjs-pages' | 'vite-react' | 'generic';
  structure: ProjectStructure;
  buildConfig: BuildConfiguration;
  libraryConfig: LibraryConfiguration;
}

interface ProjectStructure {
  appDirectory: string;
  componentsDirectory: string;
  uiLibraryPath: string;
  libDirectory: string;
  assetsPath: string;
  stylesPath: string;
  typesPath: string;
  hooksPath: string;
}

interface LibraryConfiguration {
  structure: LibraryStructure;
  exports: ExportStrategy;
  dependencies: DependencyManagement;
  documentation: DocumentationConfig;
}

interface LibraryStructure {
  'ui/': {
    primitives: string[];
    composed: string[];
    patterns: string[];
  };
  'icons/': IconOrganization;
  'hooks/': HookOrganization;
  'utils/': UtilityOrganization;
  'types/': TypeOrganization;
}
```

### Validation and Quality Assurance
```typescript
interface ValidationResult {
  passed: boolean;
  score: number; // 0-100
  issues: ValidationIssue[];
  suggestions: ValidationSuggestion[];
  metrics: QualityMetrics;
}

interface ValidationIssue {
  severity: 'error' | 'warning' | 'info';
  category: 'accessibility' | 'performance' | 'styling' | 'structure';
  message: string;
  location?: string;
  fix?: string;
}

interface QualityMetrics {
  pixelAccuracy: number; // Deviation in px
  accessibilityScore: number; // WCAG compliance score
  performanceScore: number; // Bundle size, render time
  maintainabilityScore: number; // Code quality metrics
}
```

### Agent Communication
```typescript
interface AgentCommunication {
  sendData<T>(targetAgent: string, data: T): Promise<void>;
  requestData<T>(sourceAgent: string, query: DataQuery): Promise<T>;
  shareAnalysis(analysis: AnalysisResult, targetAgents: string[]): Promise<void>;
  requestValidation(data: any, validatorAgent: string): Promise<ValidationResult>;
}

interface DataQuery {
  type: 'component-analysis' | 'design-tokens' | 'architecture-config';
  filters?: Record<string, any>;
  includeDetails?: boolean;
}

interface AnalysisResult {
  type: string;
  data: any;
  confidence: number;
  timestamp: Date;
  agent: string;
}
```

## Shared Constants

```typescript
export const SHADCN_COMPONENTS = [
  'accordion', 'alert', 'alert-dialog', 'avatar', 'badge', 'button',
  'calendar', 'card', 'carousel', 'checkbox', 'collapsible', 'combobox',
  'command', 'context-menu', 'data-table', 'date-picker', 'dialog',
  'drawer', 'dropdown-menu', 'form', 'hover-card', 'input', 'label',
  'menubar', 'navigation-menu', 'pagination', 'popover', 'progress',
  'radio-group', 'scroll-area', 'select', 'separator', 'sheet',
  'skeleton', 'slider', 'switch', 'table', 'tabs', 'textarea',
  'toast', 'toggle', 'toggle-group', 'tooltip'
] as const;

export const TAILWIND_BREAKPOINTS = {
  'sm': '640px',
  'md': '768px',
  'lg': '1024px',
  'xl': '1280px',
  '2xl': '1536px'
} as const;

export const ACCESSIBILITY_REQUIREMENTS = {
  'WCAG_AA': {
    colorContrast: 4.5,
    largeTextContrast: 3.0,
    focusIndicator: true,
    keyboardNavigation: true,
    screenReaderSupport: true
  }
} as const;
```