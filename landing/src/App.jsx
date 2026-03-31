import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const Artifacts = {
  agent: {
    title: "AGENTS/rules.md",
    mode: "Execution-First",
    status: "Structural Baseline",
    icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v10m0 0 4-4m-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>,
    content: `# Agent Execution Rules (Baseline)\n\nUse this structural baseline to maintain agent grounding. Content is synchronized with logic evolution via \`docagent refresh\`.\n\n## Top Invariants\n- Verify documented command paths before merge.\n- Keep AGENTS and docs refreshed after structural changes.\n- Escalate source-of-truth conflicts instead of guessing.`
  },
  agentZh: {
    title: "AGENTS.zh/rules.md",
    mode: "执行优先",
    status: "结构化基线 (已就绪)",
    icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v10m0 0 4-4m-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>,
    content: `# 智能体执行规则 (结构契约)\n\n在执行 Agent 任务时提供结构化说明。注：此产物为结构化契约，内容质量取决于初始生成后的刷新循环。\n\n## 核心不变式\n- 交付前验证文档化的命令路径。\n- 在结构变更后通过 refresh 保持同步。\n- 遇到真相来源冲突时，选择上报而非猜测。`
  },
  human: {
    title: "docs/architecture.md",
    mode: "Strategic-First",
    status: "Narrative Baseline",
    icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M8 7h6"/><path d="M8 11h8"/><path d="M8 15h6"/></svg>,
    content: `# Architecture Overview (Baseline)\n\n## Structural Intent\nThis repository is designed as a modular documentation engine. It prioritizes cross-platform compatibility and dual-doc clarity.\n\n## Systemic Core\n- **Dual-Doc Sync**: Unified single-pass analysis for paired outputs.\n- **Sustainability Loop**: CLI-driven refresh mechanisms to reduce manual drift.`
  },
  humanZh: {
    title: "docs.zh/architecture.md",
    mode: "策略优先",
    status: "结构化基线 (已就绪)",
    icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M8 7h6"/><path d="M8 11h8"/><path d="M8 15h6"/></svg>,
    content: `# 架构概览 (结构契约)\n\n## 结构意图\n本仓库设计为模块化文档引擎。注：此产物为初始结构投影，建议人工校验核心叙词。\n\n## 系统核心\n- **双效同步**: 统一单次分析产生配对产物。\n- **可持续循环**: CLI 驱动的刷新机制，减少偏移。`
  }
};

const heroCases = [
  {
    index: 0,
    label: 'Global Install',
    title: 'Registering CLI Engine',
    command: 'tim@macBook ~ % npm install -g doc-for-agent@next',
    output: [
      { text: '[step 1/1] Fetching docagent engine...', color: 'var(--text-secondary)' },
      { text: '✓ doc-for-agent installed globally.', color: 'var(--accent)' },
      { text: '✓ Ready for repository-level activation.', color: 'var(--accent)' },
    ]
  },
  {
    index: 1,
    label: 'docagent init',
    title: 'Activating Structural Baseline',
    command: 'tim@macBook ~ % docagent init --ai codex',
    output: [
      { text: '[step 1/3] Scanning repository signals...', color: 'var(--text-secondary)' },
      { text: '✓ Detected low-doc codebase state.', color: 'var(--accent)' },
      { text: '[step 2/3] Projecting Four-View Baseline...', color: 'var(--text-secondary)' },
      { text: '  + /AGENTS/ (EN)', color: '#fff' },
      { text: '  + /AGENTS.zh/ (ZH)', color: '#fff' },
      { text: '  + /docs/   (EN)', color: '#fff' },
      { text: '  + /docs.zh/   (ZH)', color: '#fff' },
      { text: '[step 3/3] Baseline established as structural contract.', color: 'var(--accent)' },
    ]
  },
  {
    index: 2,
    label: 'docagent refresh',
    title: 'Continuous Synchronization',
    command: 'tim@macBook ~ % docagent refresh',
    output: [
      { text: '[step 1/2] Detecting logic evolution...', color: 'var(--text-secondary)' },
      { text: '✓ Identifying code drifts from baseline.', color: 'var(--accent)' },
      { text: '[step 2/2] Synchronizing dual-doc pair...', color: 'var(--text-secondary)' },
      { text: '  ↺ /AGENTS/ rules updated.', color: '#fff' },
      { text: '  ↺ /docs/ narrative refreshed.', color: '#fff' },
      { text: 'Documentation lifecycle sync complete.', color: 'var(--primary)' },
    ]
  }
];

const commands = [
  { 
    name: 'init', 
    desc: 'Establish systemic baseline from legacy or inconsistent repositories', 
    status: 'Grounded',
    logic: 'Context Extraction',
    complexity: 'Infrastructure',
    efficiency: 'Deep Scan',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v10m0 0 4-4m-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>
  },
  { 
    name: 'refresh', 
    desc: 'Synchronize dual artifacts with active logic evolution', 
    status: 'Ready',
    logic: 'Drift Detection',
    complexity: 'Semantic',
    efficiency: 'Atomic Sync',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
  },
  { 
    name: 'doctor', 
    desc: 'Audit grounding integrity and systemic health across artifacts', 
    status: 'Stable',
    logic: 'Verification',
    complexity: 'Deterministic',
    efficiency: 'Instant',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20"/><path d="m5 9 7 7 7-7"/></svg>
  },
  { 
    name: 'migrate', 
    desc: 'Absorb legacy documentation into the dual-doc baseline', 
    status: 'Grounded',
    logic: 'Knowledge Intake',
    complexity: 'Heuristic',
    efficiency: 'Structural',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m8 17 4 4 4-4"/></svg>
  },
  { 
    name: 'generate', 
    desc: 'Project machine execution context for targeted Agent platforms', 
    status: 'Production',
    logic: 'Artifact Projection',
    complexity: 'Targeted',
    efficiency: 'Native-Fit',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
  },
];

const playgroundVariants = [
  {
    id: 'v1',
    label: 'Initial Grounding',
    code: `// src/auth.ts
export function login(user) {
  // Simple auth logic
  return validate(user.id);
}`,
    human: `# Auth logic\n\nSupports basic user ID validation.\n\nStatus: current baseline view.`,
    agent: `# EXECUTION RULES\n\n- call validate(user.id)\n- return boolean`
  },
  {
    id: 'v2',
    label: 'Logic Evolution',
    code: `// src/auth.ts
export function login(user) {
  // Upgraded to JWT + MFA
  const token = sign(user.id);
  return verifyMFA(token);
}`,
    human: `# Auth logic\n\n[DRIFT DETECTED]\nHuman docs currently show legacy ID validation.`,
    agent: `# EXECUTION RULES\n\n[DRIFT DETECTED]\nAgent context out of sync with new MFA logic.`
  },
  {
    id: 'v3',
    label: 'Systemic Sync',
    code: `// src/auth.ts
export function login(user) {
  // Upgraded to JWT + MFA
  const token = sign(user.id);
  return verifyMFA(token);
}`,
    human: `# Auth logic\n\nNow supports JWT and MFA verification flow.\n\nStatus: refreshed after logic change.`,
    agent: `# EXECUTION RULES\n\n- sign(user.id) for token\n- verifyMFA(token) strictly`
  }
];

function renderMarkdown(content) {
  // Simple regex-based syntax highlighting for Markdown
  const lines = content.split('\n');
  return lines.map((line, i) => {
    let styledLine = line;
    
    // Headers
    if (line.startsWith('# ')) {
      return <div key={i} className="md-line md-h1">{line}</div>;
    }
    if (line.startsWith('## ')) {
      return <div key={i} className="md-line md-h2">{line}</div>;
    }
    
    // Bullets
    if (line.trim().startsWith('- ')) {
      const parts = line.split('- ');
      return (
        <div key={i} className="md-line">
          <span className="md-bullet">- </span>
          {renderInlineStyles(parts[1])}
        </div>
      );
    }

    return <div key={i} className="md-line">{renderInlineStyles(line)}</div>;
  });
}

function renderInlineStyles(text) {
  if (!text) return '';
  // Highlight inline code `...`
  const parts = text.split(/(`[^`]+`)/g);
  return parts.map((part, i) => {
    if (part.startsWith('`') && part.endsWith('`')) {
      return <span key={i} className="md-inline-code">{part}</span>;
    }
    return part;
  });
}

function App() {
  const [activeArtifact, setActiveArtifact] = useState('agent');
  const [activeHeroCase, setActiveHeroCase] = useState(0);
  const [activePlayground, setActivePlayground] = useState(0);
  const [isSyncing, setIsSyncing] = useState(false);
  const [sliderValue, setSliderValue] = useState(50);
  const [activePlatform, setActivePlatform] = useState('claudecode');

  const handleSync = () => {
    if (activePlayground === 1) {
      setIsSyncing(true);
      setTimeout(() => {
        setActivePlayground(2);
        setIsSyncing(false);
      }, 1500);
    }
  };

  const platforms = {
    claudecode: {
      name: 'Claude Code',
      icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M8 7h6"/><path d="M8 11h8"/><path d="M8 15h6"/></svg>,
      integration: 'docagent init --ai claudecode',
      description: 'Establishes the structural baseline for Claude Code to maintain repository grounding.'
    },
    codex: {
      name: 'Codex',
      icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><line x1="9" x2="15" y1="9" y2="15"/><line x1="15" x2="9" y1="9" y2="15"/></svg>,
      integration: 'docagent init --ai codex',
      description: 'Installs the Codex-facing skill bundle to keep execution rules aligned with logic evolution.'
    },
    continue: {
      name: 'Continue',
      icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>,
      integration: 'docagent init --ai continue',
      description: 'Installs the Continue-facing integration path while keeping the same docs and AGENTS baseline.'
    },
    copilot: {
      name: 'Copilot',
      icon: <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20"/><path d="m5 9 7 7 7-7"/></svg>,
      integration: 'docagent init --ai copilot',
      description: 'Installs the Copilot-facing integration path without changing the core dual-doc lifecycle.'
    }
  };

  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('active');
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.scroll-reveal').forEach(el => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  return (
    <div className="page-shell">
      <div className="page-backdrop" aria-hidden="true" />
      
      <header className="topbar">
        <a className="brand" href="#hero">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" style={{ color: 'var(--primary)' }}><path d="M12 2v8"/><path d="m16 6-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>
          <strong>doc-for-agent</strong>
          <small>v1.4.0 "@next"</small>
        </a>
        <nav className="nav-links">
          <a href="#dual-logic">Documentation System</a>
          <a href="#workflow">Lifecycle Path</a>
          <a href="#why-docagent">Why Grounding?</a>
          <a className="nav-cta" href="https://github.com/Timcai06/Doc-For-Agent-skill">GitHub</a>
        </nav>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="hero section" id="hero">
          <div className="hero-copy scroll-reveal">
            <div className="badge-technical" style={{ borderRadius: '100px', padding: '6px 16px', marginBottom: '16px', color: 'var(--primary)', border: '1px solid var(--primary-glow)', background: 'rgba(56,189,248,0.05)', fontSize: '0.75rem', fontWeight: '700', letterSpacing: '0.05em' }}>DOCUMENTATION LIFECYCLE CLI</div>
            <h1>
              The Source of Truth for <br />
              <span style={{ color: 'var(--primary)', textShadow: '0 0 30px var(--primary-glow)' }}>Agentic Workflows.</span>
            </h1>
            <p className="hero-text">
              Don't leave your Agent's memory to chance. <strong>doc-for-agent</strong> establishes a sustainable documentation system: <code>/docs/</code> for humans, <code>/AGENTS/</code> for machines. All synchronized via CLI.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#workflow">
                Get Started
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
              </a>
              <a className="button button-secondary" href="#dual-logic">Dual-Doc Philosophy</a>
            </div>
            
            <div className="ecosystem-row">
              <span style={{ opacity: 0.6 }}>Powering Workflows in:</span>
              <div className="ecosystem-badges">
                <span className="eco-badge">Claude Code</span>
                <span className="eco-badge">Codex</span>
                <span className="eco-badge">Continue</span>
                <span className="eco-badge">Copilot</span>
              </div>
            </div>
          </div>

          <div className="hero-preview scroll-reveal">
            <div className="terminal-window floating">
              <div className="terminal-header">
                <div className="window-dots">
                  <div className="dot red" />
                  <div className="dot yellow" />
                  <div className="dot green" />
                </div>
                <div className="terminal-title">zsh — {heroCases[activeHeroCase].title}</div>
              </div>
              <div className="terminal-tabs">
                {heroCases.map((c) => (
                  <button 
                    key={c.index} 
                    className={`terminal-tab-btn ${activeHeroCase === c.index ? 'active' : ''}`}
                    onClick={() => setActiveHeroCase(c.index)}
                  >
                    {c.label}
                  </button>
                ))}
              </div>
              <div className="code-body terminal-body">
                <div className="terminal-line command" style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '12px', marginBottom: '16px' }}>
                  <span className="prompt" style={{ color: 'var(--accent)' }}>%</span> {heroCases[activeHeroCase].command.split('%')[1]?.trim()}
                </div>
                <div className="terminal-output">
                  {heroCases[activeHeroCase].output.map((line, i) => (
                    <div key={i} className="terminal-line" style={{ color: line.color, animationDelay: `${i * 80}ms` }}>
                      {line.text}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* DUAL DOC LOGIC SECTION */}
        <section className="section" id="dual-logic">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">DUAL-MODE ARCHITECTURE</span>
            <h2>Two Targets. One Truth.</h2>
            <p className="feature-desc">Stop fighting manual drift. The engine analyzes your codebase to produce synchronized artifacts for both human maintainers and coding agents.</p>
          </div>

          <div className="sync-diagram scroll-reveal">
             <div className="sync-part source">
               <div className="source-stack">
                 <div className="stack-item code">/src</div>
                 <div className="stack-item messy">README.md</div>
                 <div className="stack-item config">.env.example</div>
               </div>
               <strong>Raw Repository Assets</strong>
               <p>Messy, low-doc, or inconsistent files.</p>
             </div>
             <div className="sync-arrow-center">
               <div className="engine-orb">
                 <div className="orb-inner" />
                 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M12 2v8"/><path d="m16 6-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>
               </div>
             </div>
             <div className="sync-part results">
               <div className="res-card-group">
                 <div className="res-card agent"><strong>/AGENTS/</strong> Context Baseline</div>
                 <div className="res-card human"><strong>/docs/</strong> Narrative Baseline</div>
               </div>
               <strong>Unified Knowledge Hub</strong>
               <p>Derived from repository analysis and legacy-document heuristics.</p>
             </div>
          </div>

          {/* GROUNDING PLAYGROUND SUBSECTION */}
          <div className="playground-container scroll-reveal" style={{ marginTop: '80px' }}>
            <div className="playground-head">
              <h3>Grounding Playground</h3>
              <p>Simulate a logic evolution and see the systemic sync in action.</p>
            </div>
            
            <div className="playground-editor-shell">
              <div className="pg-controls">
                {playgroundVariants.map((v, i) => (
                  <button 
                    key={v.id} 
                    className={`pg-btn ${activePlayground === i ? 'active' : ''}`}
                    disabled={i === 2 && activePlayground !== 2 && !isSyncing}
                    onClick={() => setActivePlayground(i)}
                  >
                    {v.label}
                  </button>
                ))}
              </div>
              
              <div className="pg-main-grid">
                <div className="pg-pane code-pane">
                  <div className="pane-header">Source Code</div>
                  <div className="code-body ide-look">
                    <div className="code-gutter">
                      {[1,2,3,4,5].map(n => <span key={n}>{n}</span>)}
                    </div>
                    <pre><code>{playgroundVariants[activePlayground].code}</code></pre>
                  </div>
                  {activePlayground === 1 && (
                    <button className={`sync-trigger ${isSyncing ? 'syncing' : ''}`} onClick={handleSync}>
                      {isSyncing ? 'Systemic Syncing...' : 'docagent refresh'}
                    </button>
                  )}
                </div>
                
                <div className="pg-pane doc-pane">
                  <div className="pane-header">Dual-Doc Outputs</div>
                  <div className="dual-doc-tabs">
                    <div className="sync-doc-box human">
                      <div className="doc-label">/docs/ human narrative</div>
                      <div className="md-content mini">
                        {renderMarkdown(playgroundVariants[activePlayground].human)}
                      </div>
                    </div>
                    <div className="sync-doc-box agent">
                      <div className="doc-label">/AGENTS/ execution rules</div>
                      <div className="md-content mini">
                        {renderMarkdown(playgroundVariants[activePlayground].agent)}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="dual-grid scroll-reveal" style={{ marginTop: '64px' }}>
            <div className="dual-card agent">
              <div className="card-label">FOR AGENTS (Execution-First)</div>
              <h3>/AGENTS/ Context</h3>
              <p>Actionable, high-density execution rules. Designed for Claude Code, Codex, Continue, and Copilot workflows with lower ambiguity and repeatable refresh paths.</p>
              <ul className="mini-features">
                <li>✓ Deterministic Invariants</li>
                <li>✓ CLI Workflow Handoffs</li>
                <li>✓ Lower Ambiguity Under Refresh</li>
              </ul>
            </div>
            <div className="dual-card human">
              <div className="card-label">FOR HUMANS (Narrative-First)</div>
              <h3>/docs/ Reference</h3>
              <p>Strategic narrative for maintainers and team onboarding. High-level architecture guides and onboarding maps that remain synchronized with machine rules.</p>
              <ul className="mini-features">
                <li>✓ Strategic Architecture Maps</li>
                <li>✓ Narrative Team Onboarding</li>
                <li>✓ Sustainable Maintenance</li>
              </ul>
            </div>
          </div>
        </section>

        {/* SYSTEMS RESILIENCE SECTION */}
        <section className="section" id="scenarios">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Enterprise Resilience</span>
            <h2>Built for messy realities.</h2>
            <p className="feature-desc">doc-for-agent doesn't require a clean repo to start. It creates order from fragmentation.</p>
          </div>
          <div className="scenario-row scroll-reveal">
            {[
              { type: 'Low-Doc Legacy', desc: 'Bootstrap a professional documentation system from source code and scattered configs.' },
              { type: 'Messy-Doc Repos', desc: 'Inhale outdated, conflicting READMEs and systemize them into a durable /AGENTS/ baseline.' },
              { type: 'Team Scalability', desc: 'Maintain peak alignment for every agent session with a repeatable, automated refresh cycle.' }
            ].map(s => (
              <div key={s.type} className="scenario-pill glass-card">
                <div className="pill-header">
                  <strong>{s.type}</strong>
                  <div className="trend-up" />
                </div>
                <span>{s.desc}</span>
              </div>
            ))}
          </div>
        </section>

        {/* CASE STUDY SECTION */}
        <section className="section" id="case-study">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Real World Transformation</span>
            <h2>Order from Fragmentation.</h2>
          </div>
          
          <div className="case-study-visual scroll-reveal">
            <div className="comparison-slider">
              <div className="img-container before">
                <img src="/assets/before_messy.png" alt="Messy Repo" />
                <div className="img-label">CHAOTIC BEFORE</div>
              </div>
              <div className="img-container after" style={{ clipPath: `inset(0 0 0 ${sliderValue}%)` }}>
                <img src="/assets/after_clean.png" alt="Clean Repo" />
                <div className="img-label after">SYSTEMIC AFTER</div>
              </div>
              <input 
                type="range" 
                min="0" 
                max="100" 
                value={sliderValue} 
                onChange={(e) => setSliderValue(e.target.value)} 
                className="slider-handle"
              />
              <div className="slider-line" style={{ left: `${sliderValue}%` }} />
            </div>
            
            <div className="case-meta">
              <div className="case-stat">
                <strong>Low-doc repository example</strong>
                <p>Illustrates the shift from scattered inputs to a more structured dual-doc baseline.</p>
              </div>
              <div className="case-quote">
                "The point is not prettier markdown. The point is a baseline that humans and agents can both reuse."
              </div>
            </div>
          </div>
        </section>

        {/* ARTIFACT VISUALIZER */}
        <section className="section" id="artifacts">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Production Outputs</span>
            <h2>Consistent Knowledge Base</h2>
          </div>
          
          <div className="artifact-viewer scroll-reveal premium-viewer">
            <div className="viewer-tabs sidebar-tabs">
              {['agent', 'agentZh', 'human', 'humanZh'].map(key => (
                <button 
                  key={key}
                  className={`tab ${activeArtifact === key ? 'active' : ''}`} 
                  onClick={() => setActiveArtifact(key)}
                >
                  <div className="tab-pill-icon">{Artifacts[key].icon}</div>
                  <div className="tab-label-group">
                    <strong>{Artifacts[key].title}</strong>
                    <small>{Artifacts[key].mode}</small>
                  </div>
                </button>
              ))}
            </div>
            
            <div className="viewer-window browser">
              <div className="viewer-header-premium">
                <div className="browser-path">
                  <span className="dir">repository / </span>
                  <span className="file">{Artifacts[activeArtifact].title}</span>
                </div>
                <div className="browser-meta">
                  <div className="meta-badge pulse-dot">
                    <span className="dot-mini green" />
                    {Artifacts[activeArtifact].status}
                  </div>
                  <div className="meta-badge outline">
                    {Artifacts[activeArtifact].mode}
                  </div>
                </div>
              </div>
              <div className="code-body ide-look">
                <div className="code-gutter">
                  {[1,2,3,4,5,6,7,8,9,10,11,12].map(n => <span key={n}>{n}</span>)}
                </div>
                <div className="md-content">
                  {renderMarkdown(Artifacts[activeArtifact].content)}
                </div>
              </div>
            </div>
          </div>
        </section>

          {/* THE PROMPTING PARADOX SECTION */}
        <section className="section" id="why-docagent">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">THE PROMPTING PARADOX</span>
            <h2>Why not just prompt the agent?</h2>
            <p className="feature-desc">Prompting works for individual tasks, but fails for long-term project survival. Without a maintained baseline, teams and agents both hit context decay over time.</p>
          </div>

          <div className="drift-visual scroll-reveal">
            <div className="drift-card bad">
              <div className="drift-title">Ephemeral Prompting</div>
              <ul className="mini-features" style={{ color: 'var(--danger)' }}>
                <li>✕ Knowledge expires mid-session</li>
                <li>✕ Manual drift during logic shifts</li>
                <li>✕ Context decay across sessions</li>
                <li>✕ High-friction onboarding for new agents</li>
              </ul>
            </div>
            <div className="drift-arrow-hub">
              <div className="vs-badge">VS</div>
            </div>
            <div className="drift-card good">
              <div className="drift-title">Systemic Dual-Doc</div>
              <ul className="mini-features">
                <li>✓ Persistent /AGENTS/ baseline</li>
                <li>✓ More stable truth across sessions</li>
                <li>✓ Low-doc legacy repo support</li>
                <li>✓ Automated refresh cycle</li>
              </ul>
            </div>
          </div>
        </section>

        {/* LIFECYCLE PATH SECTION */}
        <section className="section" id="workflow">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">THE SYSTEMIC RECOVERY</span>
            <h2>Install. Init. Refresh.</h2>
            <p className="feature-desc">Go from a zero-knowledge repository to a deep-context agent workflow in three repeatable steps.</p>
          </div>
          
          <div className="lifecycle-circle-container scroll-reveal">
            <div className="lifecycle-path-v2">
              <div className="l-step step-1">
                <div className="l-icon highlight">01</div>
                <div className="l-info">
                  <strong>npm install -g</strong>
                  <p>doc-for-agent@next</p>
                </div>
              </div>
              <div className="l-connector" />
              <div className="l-step step-2">
                <div className="l-icon highlight">02</div>
                <div className="l-info">
                  <strong>docagent init</strong>
                  <p>Structural Baseline</p>
                </div>
              </div>
              <div className="l-connector" />
              <div className="l-step step-3 recurring">
                <div className="l-icon highlight">03</div>
                <div className="l-info">
                  <strong>docagent refresh</strong>
                  <p>Continuous Alignment</p>
                  <span className="loop-indicator">SYSTEMIC CYCLE</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* ECOSYSTEM BRIDGE SECTION */}
        <section className="section" id="ecosystem">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Systemic Bridge</span>
            <h2>Targeted Agent Context.</h2>
          </div>
          
          <div className="ecosystem-bridge scroll-reveal">
            <div className="platform-tabs">
              {Object.keys(platforms).map(key => (
                <button 
                  key={key} 
                  className={`plat-tab ${activePlatform === key ? 'active' : ''}`}
                  onClick={() => setActivePlatform(key)}
                >
                  {platforms[key].name}
                </button>
              ))}
            </div>
            
            <div className="platform-content glass-card premium-ide">
              <div className="plat-info">
                <div className="plat-icon-box">{platforms[activePlatform].icon}</div>
                <h3>{platforms[activePlatform].name}</h3>
                <p>{platforms[activePlatform].description}</p>
                <div className="command-box highlight">
                  <code>{platforms[activePlatform].integration}</code>
                </div>
              </div>
              <div className="plat-visual">
                <div className="plat-code-preview ide-look">
                  <div className="code-gutter">
                    {[1,2,3,4,5].map(n => <span key={n}>{n}</span>)}
                  </div>
                  <div className="md-content mini">
                    <div className="md-line md-h2"># Platform Integration</div>
                    <div className="md-line">✓ Target: {platforms[activePlatform].name}</div>
                    <div className="md-line">✓ Mode: Repository-aware docs setup</div>
                    <div className="md-line">✓ Status: Supported install path</div>
                    <div className="md-line">✓ Result: Shared dual-doc baseline</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CAPABILITY MATRIX */}
        <section className="section" id="status">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Engine Integrity</span>
            <h2>Modular Capability Matrix</h2>
            <p className="feature-desc">High-density operational modules designed for consistent repository documentation.</p>
          </div>
          
          <div className="matrix-grid scroll-reveal">
            {commands.map((cmd) => (
              <div key={cmd.name} className="matrix-card glass-card">
                <div className="matrix-card-header">
                  <div className="matrix-icon">{cmd.icon}</div>
                  <span className={`status-badge-mini ${cmd.status.toLowerCase()}`}>
                    {cmd.status === 'Production' && <span className="green-pulse-indicator" />}
                    {cmd.status}
                  </span>
                </div>
                
                <div className="matrix-card-body">
                  <div className="matrix-cmd-name">docagent {cmd.name}</div>
                  <p className="matrix-cmd-desc">{cmd.desc}</p>
                </div>
                
                <div className="matrix-card-footer">
                  <div className="matrix-stat">
                    <span className="stat-label">Logic</span>
                    <span className="stat-value">{cmd.logic}</span>
                  </div>
                  <div className="matrix-stat-row">
                    <div className="matrix-stat">
                      <span className="stat-label">Complexity</span>
                      <span className="stat-value">{cmd.complexity}</span>
                    </div>
                    <div className="matrix-stat">
                      <span className="stat-label">Efficiency</span>
                      <span className="stat-value">{cmd.efficiency}</span>
                    </div>
                  </div>
                </div>
                
                <div className="matrix-card-glow" />
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="section" id="cta">
          <div className="cta-card scroll-reveal main-cta">
            <div className="eyebrow" style={{ color: '#fff', opacity: 0.8 }}>Sustainable Knowledge LifeCycle</div>
            <h2>Protect your repo <br /> from knowledge drift.</h2>
            <p className="hero-text" style={{ margin: '0 auto 48px', opacity: 0.9 }}>Stop settling for ephemeral chat history. Establish your baseline today.</p>
            
            <div className="mega-install-container">
              <div className="install-box mega">
                <span className="install-prompt">$</span>
                <code>npm install -g doc-for-agent@next</code>
                <div className="install-glow" />
              </div>
              <p className="install-hint">Ground your repository with <code>docagent init --ai codex</code></p>
            </div>
          </div>
        </section>
      </main>

      <footer style={{ padding: '64px 0', textAlign: 'center', color: 'var(--text-muted)', borderTop: '1px solid var(--line)' }}>
        <p>&copy; 2026 doc-for-agent. A systematic documentation tool for the Agentic Era.</p>
      </footer>
    </div>
  );
}

export default App;
