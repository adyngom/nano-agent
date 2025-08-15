# MCP Server Integration Patterns

## Figma MCP Server Integration

### Core Connection Pattern
```typescript
class FigmaMCPProxy {
  private client: FigmaMCPClient;
  private cache: Map<string, any> = new Map();
  private cacheTimeout = 5 * 60 * 1000; // 5 minutes

  async getCode(nodeId?: string, options?: CodeOptions): Promise<CodeResult> {
    const cacheKey = `code-${nodeId}-${JSON.stringify(options)}`;
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    const result = await this.client.getCode({
      nodeId,
      clientName: 'claude-code',
      clientLanguages: 'typescript,javascript,html,css',
      clientFrameworks: 'react,nextjs,tailwindcss,shadcn'
    });

    this.cache.set(cacheKey, result);
    setTimeout(() => this.cache.delete(cacheKey), this.cacheTimeout);
    
    return result;
  }

  async getVariableDefinitions(nodeId?: string): Promise<VariableDefinitions> {
    const cacheKey = `variables-${nodeId}`;
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    const result = await this.client.getVariableDefinitions({
      nodeId,
      clientName: 'claude-code',
      clientLanguages: 'typescript,css',
      clientFrameworks: 'tailwindcss,shadcn'
    });

    this.cache.set(cacheKey, result);
    setTimeout(() => this.cache.delete(cacheKey), this.cacheTimeout);
    
    return result;
  }

  async getImage(nodeId?: string): Promise<ImageResult> {
    const cacheKey = `image-${nodeId}`;
    
    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey);
    }

    const result = await this.client.getImage({
      nodeId,
      clientName: 'claude-code',
      clientLanguages: 'typescript',
      clientFrameworks: 'react,nextjs'
    });

    this.cache.set(cacheKey, result);
    setTimeout(() => this.cache.delete(cacheKey), this.cacheTimeout);
    
    return result;
  }

  async getCodeConnectMap(nodeId?: string): Promise<CodeConnectMap> {
    const result = await this.client.getCodeConnectMap({
      nodeId,
      clientName: 'claude-code',
      clientLanguages: 'typescript',
      clientFrameworks: 'react,nextjs,shadcn'
    });

    return result;
  }
}
```

### Data Extraction Utilities
```typescript
class FigmaDataExtractor {
  constructor(private mcpProxy: FigmaMCPProxy) {}

  async extractComponentStructure(nodeId: string): Promise<ComponentStructure> {
    const [code, variables, image] = await Promise.all([
      this.mcpProxy.getCode(nodeId),
      this.mcpProxy.getVariableDefinitions(nodeId),
      this.mcpProxy.getImage(nodeId)
    ]);

    return {
      code: this.parseCodeStructure(code),
      variables: this.parseVariables(variables),
      visual: this.analyzeVisualStructure(image),
      metadata: this.extractMetadata(code)
    };
  }

  private parseCodeStructure(code: CodeResult): ParsedStructure {
    // Extract HTML structure and identify component patterns
    const htmlMatch = code.code.match(/<[\s\S]*>/);
    if (!htmlMatch) return { elements: [], interactions: [] };

    return {
      elements: this.identifyElements(htmlMatch[0]),
      interactions: this.identifyInteractions(code.code),
      layout: this.identifyLayoutPattern(htmlMatch[0])
    };
  }

  private parseVariables(variables: VariableDefinitions): ParsedVariables {
    const parsed: ParsedVariables = {
      colors: {},
      typography: {},
      spacing: {},
      effects: {}
    };

    Object.entries(variables).forEach(([key, value]) => {
      if (this.isColorVariable(key, value)) {
        parsed.colors[key] = this.parseColorValue(value);
      } else if (this.isTypographyVariable(key, value)) {
        parsed.typography[key] = this.parseTypographyValue(value);
      } else if (this.isSpacingVariable(key, value)) {
        parsed.spacing[key] = this.parseSpacingValue(value);
      } else if (this.isEffectVariable(key, value)) {
        parsed.effects[key] = this.parseEffectValue(value);
      }
    });

    return parsed;
  }
}
```

## ShadCN MCP Server Integration

### Component Management
```typescript
class ShadCNMCPProxy {
  private client: ShadCNMCPClient;
  private componentCache: Map<string, ShadCNComponent> = new Map();

  async getComponent(componentName: string): Promise<ShadCNComponent> {
    if (this.componentCache.has(componentName)) {
      return this.componentCache.get(componentName)!;
    }

    const [source, demo, metadata] = await Promise.all([
      this.client.getComponent({ componentName }),
      this.client.getComponentDemo({ componentName }),
      this.client.getComponentMetadata({ componentName })
    ]);

    const component: ShadCNComponent = {
      name: componentName,
      source: source.code,
      demo: demo.code,
      metadata,
      variants: this.extractVariants(source.code),
      props: this.extractProps(source.code),
      dependencies: this.extractDependencies(source.code)
    };

    this.componentCache.set(componentName, component);
    return component;
  }

  async listAllComponents(): Promise<ShadCNComponent[]> {
    const componentList = await this.client.listComponents();
    
    return Promise.all(
      componentList.map(name => this.getComponent(name))
    );
  }

  async getBlock(blockName: string): Promise<ShadCNBlock> {
    const block = await this.client.getBlock({ 
      blockName,
      includeComponents: true 
    });

    return {
      name: blockName,
      code: block.code,
      components: block.components || [],
      category: this.inferBlockCategory(blockName),
      complexity: this.assessBlockComplexity(block.code)
    };
  }

  private extractVariants(sourceCode: string): ComponentVariant[] {
    // Parse cva() calls to extract variants
    const cvaMatch = sourceCode.match(/cva\s*\(\s*["'`]([^"'`]*)["'`]\s*,\s*\{([\s\S]*?)\}\s*\)/);
    if (!cvaMatch) return [];

    const variantsMatch = cvaMatch[2].match(/variants:\s*\{([\s\S]*?)\}/);
    if (!variantsMatch) return [];

    return this.parseVariantObject(variantsMatch[1]);
  }

  private extractProps(sourceCode: string): PropDefinition[] {
    // Extract TypeScript interface definitions
    const interfaceMatches = sourceCode.match(/interface\s+(\w+Props)\s*\{([\s\S]*?)\}/g);
    if (!interfaceMatches) return [];

    return interfaceMatches.flatMap(match => 
      this.parseInterfaceProps(match)
    );
  }
}
```

### Component Matching Engine
```typescript
class ComponentMatcher {
  constructor(
    private figmaProxy: FigmaMCPProxy,
    private shadcnProxy: ShadCNMCPProxy
  ) {}

  async findBestMatches(
    figmaStructure: ComponentStructure,
    confidence: number = 0.3
  ): Promise<ShadCNMatch[]> {
    const availableComponents = await this.shadcnProxy.listAllComponents();
    const matches: ShadCNMatch[] = [];

    for (const component of availableComponents) {
      const matchScore = await this.calculateMatch(figmaStructure, component);
      
      if (matchScore.confidence >= confidence) {
        matches.push({
          component,
          confidence: matchScore.confidence,
          modifications: matchScore.modifications,
          composition: matchScore.composition
        });
      }
    }

    return matches.sort((a, b) => b.confidence - a.confidence);
  }

  private async calculateMatch(
    figmaStructure: ComponentStructure,
    shadcnComponent: ShadCNComponent
  ): Promise<MatchScore> {
    const scores = {
      semantic: this.calculateSemanticMatch(figmaStructure, shadcnComponent),
      structural: this.calculateStructuralMatch(figmaStructure, shadcnComponent),
      functional: this.calculateFunctionalMatch(figmaStructure, shadcnComponent),
      visual: this.calculateVisualMatch(figmaStructure, shadcnComponent)
    };

    const weightedScore = 
      scores.semantic * 0.3 +
      scores.structural * 0.3 +
      scores.functional * 0.2 +
      scores.visual * 0.2;

    return {
      confidence: weightedScore,
      modifications: this.identifyModifications(figmaStructure, shadcnComponent),
      composition: this.suggestComposition(figmaStructure, shadcnComponent),
      breakdown: scores
    };
  }

  private calculateSemanticMatch(
    figma: ComponentStructure,
    shadcn: ShadCNComponent
  ): number {
    const figmaName = figma.metadata.name.toLowerCase();
    const shadcnName = shadcn.name.toLowerCase();

    // Direct name matching
    if (figmaName.includes(shadcnName) || shadcnName.includes(figmaName)) {
      return 0.9;
    }

    // Semantic keyword matching
    const figmaKeywords = this.extractKeywords(figmaName);
    const shadcnKeywords = this.extractKeywords(shadcnName);
    
    const commonKeywords = figmaKeywords.filter(k => 
      shadcnKeywords.includes(k)
    );

    return commonKeywords.length / Math.max(figmaKeywords.length, shadcnKeywords.length);
  }
}
```

## Shared Data Management

### Cache Strategy
```typescript
class SharedDataCache {
  private figmaData: Map<string, any> = new Map();
  private shadcnData: Map<string, any> = new Map();
  private analysisResults: Map<string, any> = new Map();

  // Figma data caching
  async getFigmaData<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    if (this.figmaData.has(key)) {
      return this.figmaData.get(key);
    }

    const data = await fetcher();
    this.figmaData.set(key, data);
    
    // Auto-expire after 10 minutes
    setTimeout(() => this.figmaData.delete(key), 10 * 60 * 1000);
    
    return data;
  }

  // ShadCN data caching
  async getShadcnData<T>(key: string, fetcher: () => Promise<T>): Promise<T> {
    if (this.shadcnData.has(key)) {
      return this.shadcnData.get(key);
    }

    const data = await fetcher();
    this.shadcnData.set(key, data);
    
    // ShadCN data changes less frequently, cache for 1 hour
    setTimeout(() => this.shadcnData.delete(key), 60 * 60 * 1000);
    
    return data;
  }

  // Cross-agent analysis sharing
  shareAnalysis(analysisId: string, data: any, ttl: number = 5 * 60 * 1000): void {
    this.analysisResults.set(analysisId, data);
    setTimeout(() => this.analysisResults.delete(analysisId), ttl);
  }

  getSharedAnalysis<T>(analysisId: string): T | null {
    return this.analysisResults.get(analysisId) || null;
  }
}
```

### Error Handling and Retry Logic
```typescript
class MCPErrorHandler {
  private maxRetries = 3;
  private baseDelay = 1000;

  async withRetry<T>(
    operation: () => Promise<T>,
    context: string
  ): Promise<T> {
    let lastError: Error;
    
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = error as Error;
        
        if (attempt === this.maxRetries) {
          throw new MCPError(
            `Failed after ${this.maxRetries} attempts: ${context}`,
            lastError
          );
        }

        const delay = this.baseDelay * Math.pow(2, attempt - 1);
        await this.sleep(delay);
      }
    }

    throw lastError!;
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

class MCPError extends Error {
  constructor(message: string, public cause?: Error) {
    super(message);
    this.name = 'MCPError';
  }
}
```

## Best Practices

### 1. Efficient Data Fetching
```typescript
// Batch related requests
const batchFigmaData = async (nodeIds: string[]) => {
  const requests = nodeIds.map(async (nodeId) => ({
    nodeId,
    code: await figmaProxy.getCode(nodeId),
    variables: await figmaProxy.getVariableDefinitions(nodeId),
    image: await figmaProxy.getImage(nodeId)
  }));

  return Promise.all(requests);
};

// Use parallel requests where possible
const [figmaData, shadcnComponents] = await Promise.all([
  figmaProxy.getCode(nodeId),
  shadcnProxy.listAllComponents()
]);
```

### 2. Smart Caching
```typescript
// Cache based on content hash, not just time
const getCacheKey = (data: any): string => {
  return crypto
    .createHash('md5')
    .update(JSON.stringify(data))
    .digest('hex');
};

// Invalidate cache when source data changes
const invalidateRelatedCache = (figmaFileId: string) => {
  const keysToDelete = Array.from(cache.keys()).filter(key => 
    key.includes(figmaFileId)
  );
  keysToDelete.forEach(key => cache.delete(key));
};
```

### 3. Graceful Degradation
```typescript
// Provide fallbacks when MCP services are unavailable
const getComponentWithFallback = async (name: string): Promise<ShadCNComponent> => {
  try {
    return await shadcnProxy.getComponent(name);
  } catch (error) {
    console.warn(`ShadCN MCP unavailable, using local fallback for ${name}`);
    return getLocalComponentDefinition(name);
  }
};
```