import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const Artifacts = {
  human: {
    title: "docs/architecture.md",
    mode: "Narrative-First",
    status: "Audit Passed",
    icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1-2.5-2.5z"/><path d="M8 7h6"/><path d="M8 11h8"/><path d="M8 15h6"/></svg>,
    content: `# Architecture Overview\n\n## Narrative Context\nThis repository prioritizes clarity for human onboarding and strategic alignment.\n\n## Systemic Core\n- Unified Analysis: Single pass for dual outputs.\n- Drift Prevention: Automated refresh via CLI.\n\n## Maintenance\nNarratives remain synchronized with real code signals.`
  },
  agent: {
    title: "AGENTS/rules.md",
    mode: "Execution-First",
    status: "Grounded 100%",
    icon: <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v10m0 0 4-4m-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>,
    content: `# Agent Execution Rules\n\n## Top Invariants\n- Verify AST stability before merge.\n- Ground all commands in local /src.\n- Prevent context overflow via splits.\n\n## Grounding Context\n- Root Path: ./\n- Engine: docagent-core v1.2`
  }
};

const heroCases = [
  {
    index: 0,
    label: 'docagent init',
    title: 'Establish Baseline',
    command: 'tim@macBook ~ % docagent init --target . --ai all',
    output: [
      { text: '[1/3] Scanning repository for legacy knowledge...', color: 'var(--text-secondary)' },
      { text: '✓ Detected low-doc state with scattered READMEs.', color: 'var(--accent)' },
      { text: '[2/3] Establishing Dual-Doc baseline...', color: 'var(--text-secondary)' },
      { text: '  + /AGENTS/ (Machine Execution Context)', color: '#fff' },
      { text: '  + /docs/   (Human Narrative Guide)', color: '#fff' },
      { text: '[3/3] LifeCycle enabled. Initialized for Claude/Codex/Copilot.', color: 'var(--accent)' },
    ]
  },
  {
    index: 1,
    label: 'docagent refresh',
    title: 'Knowledge Maintenance',
    command: 'tim@macBook ~ % docagent refresh',
    output: [
      { text: '[1/2] Checking for systemic drift...', color: 'var(--text-secondary)' },
      { text: '✓ Detected 5 code changes affecting execution logic.', color: 'var(--accent)' },
      { text: '[2/2] Refreshing paired artifacts...', color: 'var(--text-secondary)' },
      { text: '  ↺ /AGENTS/ context synchronized.', color: '#fff' },
      { text: '  ↺ /docs/ architecture guides updated.', color: '#fff' },
      { text: 'Refresh complete. "Manual Drift" neutralized.', color: 'var(--primary)' },
    ]
  },
  {
    index: 2,
    label: 'docagent doctor',
    title: 'System Health Audit',
    command: 'tim@macBook ~ % docagent doctor',
    output: [
      { text: '[1/1] Auditing documentation integrity...', color: 'var(--text-secondary)' },
      { text: '✓ /AGENTS/ rules are 100% grounded in /src.', color: 'var(--accent)' },
      { text: '✓ /docs/ narratives match current AST structure.', color: 'var(--accent)' },
      { text: '✓ Dual-doc synchronization confirmed.', color: 'var(--accent)' },
      { text: 'Integrity Audit Passed (0.8s).', color: 'var(--primary)' },
    ]
  }
];

const commands = [
  { 
    name: 'init', 
    desc: 'Bootstrap the Dual-Doc system from low-doc or scattered repo state', 
    status: 'Production',
    logic: 'Global Repository Scan',
    complexity: 'High',
    efficiency: 'High fit',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v10m0 0 4-4m-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>
  },
  { 
    name: 'doctor', 
    desc: 'Audit repository stability and documentation health', 
    status: 'Stable',
    logic: 'Integrity Verification',
    complexity: 'Medium',
    efficiency: 'Fast check',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2v20"/><path d="m5 9 7 7 7-7"/></svg>
  },
  { 
    name: 'refresh', 
    desc: 'Sync documentation with real-time code evolution', 
    status: 'Production',
    logic: 'Drift Detection Engine',
    complexity: 'High',
    efficiency: 'Repeatable',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M16 16h5v5"/></svg>
  },
  { 
    name: 'migrate', 
    desc: 'Systemize scattered READMEs into structured baselines', 
    status: 'Beta',
    logic: 'Heuristic Document Extraction',
    complexity: 'Higher risk',
    efficiency: 'Use with review',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 14.899A7 7 0 1 1 15.71 8h1.79a4.5 4.5 0 0 1 2.5 8.242"/><path d="M12 12v9"/><path d="m8 17 4 4 4-4"/></svg>
  },
  { 
    name: 'generate', 
    desc: 'Produce machine-first artifacts for specific AI agents', 
    status: 'Stable',
    logic: 'Context Compression',
    complexity: 'Low',
    efficiency: 'Targeted',
    icon: <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"/><polyline points="14 2 14 8 20 8"/></svg>
  },
];

function App() {
  const [activeArtifact, setActiveArtifact] = useState('agent');
  const [activeHeroCase, setActiveHeroCase] = useState(0);

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
          <small>v1.2.0 "Systemic"</small>
        </a>
        <nav className="nav-links">
          <a href="#dual-logic">Dual-Doc System</a>
          <a href="#why-docagent">Why Stability?</a>
          <a href="#workflow">The Path</a>
          <a className="nav-cta" href="https://github.com/Timcai06/Doc-For-Agent-skill">GitHub</a>
        </nav>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="hero section" id="hero">
          <div className="hero-copy scroll-reveal">
            <div className="badge-technical" style={{ borderRadius: '100px', padding: '6px 16px', marginBottom: '16px' }}>CLI Agent Skill</div>
            <h1>
              Durable Knowledge for <br />
              <span style={{ color: 'var(--primary)' }}>the Agentic LifeCycle.</span>
            </h1>
            <p className="hero-text">
              Don't settle for ephemeral chat history. <strong>doc-for-agent</strong> builds a persistent, refreshable bridge: <code>/docs/</code> for human narrative, <code>/AGENTS/</code> for machine precision.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#workflow">Start Lifecycle</a>
              <a className="button button-secondary" href="#dual-logic">Dual-Doc Architecture</a>
            </div>
            
            <div className="ecosystem-row">
              <span>Bridging:</span>
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
            <span className="eyebrow">The Paired-Documentation Model</span>
            <h2>Two Targets. One LifeCycle.</h2>
            <p className="feature-desc">Humans need <strong>Architectural Narrative</strong> to maintain long-term alignment. Agents need <strong>Execution Rules</strong> to maintain stability. We synchronize both as code evolves.</p>
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
               <p>Grounded in repository analysis and legacy-document heuristics.</p>
             </div>
          </div>

          <div className="dual-grid scroll-reveal" style={{ marginTop: '64px' }}>
            <div className="dual-card agent">
              <div className="card-label">FOR AGENTS (Execution-First)</div>
              <h3>/AGENTS/ Context</h3>
              <p>Actionable, high-density execution rules. Designed for Claude Code and Codex to navigate repositories with machine precision, zero context overflow, and deterministic grounding.</p>
              <ul className="mini-features">
                <li>✓ Deterministic Invariants</li>
                <li>✓ CLI Workflow Handoffs</li>
                <li>✓ Zero Context Overflow</li>
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
            <h2>Grounded in messy realities.</h2>
            <p className="feature-desc">doc-for-agent doesn't require a clean repo to start. It creates order from fragmentation.</p>
          </div>
          <div className="scenario-row scroll-reveal">
            {[
              { type: 'Low-Doc Legacy', desc: 'Bootstrap a professional documentation system from zero-knowledge source and scattered configs.' },
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

        {/* ARTIFACT VISUALIZER */}
        <section className="section" id="artifacts">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Production Outputs</span>
            <h2>Grounded Knowledge Base</h2>
          </div>
          
          <div className="artifact-viewer scroll-reveal premium-viewer">
            <div className="viewer-tabs sidebar-tabs">
              <button 
                className={`tab ${activeArtifact === 'agent' ? 'active' : ''}`} 
                onClick={() => setActiveArtifact('agent')}
              >
                <div className="tab-pill-icon">{Artifacts.agent.icon}</div>
                <div className="tab-label-group">
                  <strong>AGENTS/context</strong>
                  <small>Execution Rules</small>
                </div>
              </button>
              <button 
                className={`tab ${activeArtifact === 'human' ? 'active' : ''}`} 
                onClick={() => setActiveArtifact('human')}
              >
                <div className="tab-pill-icon" style={{ color: 'var(--accent)' }}>{Artifacts.human.icon}</div>
                <div className="tab-label-group">
                  <strong>docs/narrative</strong>
                  <small>Human Guide</small>
                </div>
              </button>
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
                <pre><code>{Artifacts[activeArtifact].content}</code></pre>
              </div>
            </div>
          </div>
        </section>

          {/* WHY DOCAGENT SECTION */}
        <section className="section" id="why-docagent">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Sustainable Choice</span>
            <h2>Why not just prompt the agent?</h2>
            <p className="feature-desc">Prompting works for small fixes, but fails for long-term repository health. Ephemeral chat histories drift, context limits overflow, and agents inevitably hallucinate outdated execution rules.</p>
          </div>

          <div className="drift-visual scroll-reveal">
            <div className="drift-card bad">
              <div className="drift-title">Ephemeral Prompting</div>
              <ul className="mini-features" style={{ color: '#f87171' }}>
                <li>❌ Knowledge expires mid-session</li>
                <li>❌ Inconsistent "Manual Drift"</li>
                <li>❌ Context Decay as session grows</li>
                <li>❌ High manual alignment overhead</li>
              </ul>
            </div>
            <div className="drift-card good">
              <div className="drift-title">Systemic Dual-Doc</div>
              <ul className="mini-features">
                <li>✅ Persistent /AGENTS baseline</li>
                <li>✅ Unified truth for every session</li>
                <li>✅ Scalable for messy legacy repos</li>
                <li>✅ Automated CLI refresh cycle</li>
              </ul>
            </div>
          </div>
        </section>

        {/* LIFECYCLE PATH SECTION */}
        <section className="section" id="workflow">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Systemic Lifecycle</span>
            <h2>Install. Init. Refresh.</h2>
            <p className="feature-desc">Go from a zero-knowledge repository to a deep-context agent workflow in three systemic steps.</p>
          </div>
          
          <div className="lifecycle-path scroll-reveal">
            <div className="lifecycle-step">
              <div className="step-marker">
                <div className="marker-dot" />
                <div className="marker-line" />
              </div>
              <div className="step-content">
                <div className="step-badge">01</div>
                <h3>Global Install</h3>
                <p>Equip your CLI environment with the systemic analysis engine.</p>
                <div className="command-box">
                  <code>npm install -g doc-for-agent</code>
                </div>
              </div>
            </div>

            <div className="lifecycle-step active">
              <div className="step-marker">
                <div className="marker-dot" />
                <div className="marker-line" />
              </div>
              <div className="step-content">
                <div className="step-badge">02</div>
                <h3>System Bridge (Init)</h3>
                <p>Scan your legacy code & mess documents. Establish the baseline for every AI agent.</p>
                <div className="command-box">
                  <code>docagent init --ai all</code>
                </div>
              </div>
            </div>

            <div className="lifecycle-step recurring">
              <div className="step-marker">
                <div className="marker-dot" />
                <div className="marker-line dash" />
              </div>
              <div className="step-content">
                <div className="step-badge">03</div>
                <h3>Active Refresh</h3>
                <p>The core of sustainability. Sync knowledge as code evolves with lower manual overhead.</p>
                <div className="command-box highlight">
                  <code>docagent refresh</code>
                  <span className="recurring-tag">RECURRING</span>
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
            <p className="feature-desc">High-density operational modules designed for deterministic repository alignment.</p>
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
                <code>npm install -g doc-for-agent</code>
                <div className="install-glow" />
              </div>
              <p className="install-hint">Works with Claude Code, Codex, Continue, and Copilot.</p>
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
