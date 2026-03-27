import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const Artifacts = {
  human: {
    title: "docs/architecture.md",
    content: `# Architecture Overview\n\n## Narrative Context\nThis repository implements a rule-based documentation engine. It prioritizes clarity for human onboarding.\n\n## Core Logic\n- Unified Scan: One pass for both target outputs.\n- Drift Detection: Automated sync checks.\n\n## How to Maintain\nUse \`docagent refresh\` after significant AST changes.`
  },
  agent: {
    title: "AGENTS/03-execution/008-implementation-plan.md",
    content: `# Workflows\n\n## Top Rules\n- Verify before merge.\n- Use the documented command path.\n- Escalate source-of-truth conflicts.\n\n## Run\n- \`docagent doctor --target .\`\n- \`docagent refresh --root . --output-mode dual\``
  }
};

const heroCases = [
  {
    index: 0,
    label: 'docagent init',
    title: 'Initialize System',
    command: 'tim@macBook ~ % docagent init --ai codex --target .',
    output: [
      { text: '[1/3] Deep scanning repository...', color: 'var(--text-secondary)' },
      { text: '✓ Detected low-doc state with scattered configurations.', color: 'var(--accent)' },
      { text: '[2/3] Generating Dual-Doc baseline...', color: 'var(--text-secondary)' },
      { text: '  + /AGENTS/ (Machine Source-of-Truth)', color: '#fff' },
      { text: '  + /docs/   (Human Narrative)', color: '#fff' },
      { text: '[3/3] Dual-doc baseline established.', color: 'var(--accent)' },
    ]
  },
  {
    index: 1,
    label: 'docagent refresh',
    title: 'Lifecycle Sync',
    command: 'tim@macBook ~ % docagent refresh',
    output: [
      { text: '[1/2] Checking for drift...', color: 'var(--text-secondary)' },
      { text: '✓ Detected 3 core logic changes in /src/models.', color: 'var(--accent)' },
      { text: '[2/2] Synchronizing dual outputs...', color: 'var(--text-secondary)' },
      { text: '  ↺ /AGENTS/ context updated.', color: '#fff' },
      { text: '  ↺ /docs/ technical guides updated.', color: '#fff' },
      { text: 'Refresh complete. Agent and human docs updated.', color: 'var(--primary)' },
    ]
  },
  {
    index: 2,
    label: 'docagent doctor',
    title: 'Health Audit',
    command: 'tim@macBook ~ % docagent doctor',
    output: [
      { text: '[1/1] Auditing knowledge integrity...', color: 'var(--text-secondary)' },
      { text: '✓ All AGENTS/ skills grounded to current code.', color: 'var(--accent)' },
      { text: '✓ Human docs synchronized with recent PRs.', color: 'var(--accent)' },
      { text: 'Status: Core install and docs paths look healthy.', color: 'var(--primary)' },
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
              The Dual Documentation <br />
              <span style={{ color: 'var(--primary)' }}>System for the Agentic Era.</span>
            </h1>
            <p className="hero-text">
              Stop splitting your focus. <strong>doc-for-agent</strong> builds a unified knowledge system: /AGENTS/ for machine precision, /docs/ for human clarity. One systemic source of truth.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#workflow">Start Lifecycle</a>
              <a className="button button-secondary" href="#dual-logic">The Dual-Doc Architecture</a>
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
            <span className="eyebrow">The Dual-Mode Architecture</span>
            <h2>Two Targets. One Engine.</h2>
            <p className="feature-desc">Humans need <strong>Architectural Narrative</strong> to maintain context. Agents need <strong>Execution Rules</strong> to maintain stability. We generate both from the same code signals.</p>
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
              <div className="card-label">FOR AGENTS (Context-First)</div>
              <h3>/AGENTS/ Context</h3>
              <p>Actionable, high-density knowledge maps. Designed for AI like Claude Code and Codex to navigate repositories with clearer execution context and lower ambiguity.</p>
              <ul className="mini-features">
                <li>✓ Execution Invariants</li>
                <li>✓ Repository-Grounded Rules</li>
                <li>✓ Machine-readable Rules</li>
              </ul>
            </div>
            <div className="dual-card human">
              <div className="card-label">FOR HUMANS (Narrative-First)</div>
              <h3>/docs/ Reference</h3>
              <p>Natural narrative for maintainers and team onboarding. High-level architecture guides, technical principles, and onboarding maps grounded in real code signals.</p>
              <ul className="mini-features">
                <li>✓ Narrative Cohesion</li>
                <li>✓ Architecture Visibility</li>
                <li>✓ Fast Human Onboarding</li>
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
          <div className="artifact-viewer scroll-reveal">
            <div className="viewer-tabs">
              <button className={`tab ${activeArtifact === 'agent' ? 'active' : ''}`} onClick={() => setActiveArtifact('agent')}>AGENTS Context (Machine)</button>
              <button className={`tab ${activeArtifact === 'human' ? 'active' : ''}`} onClick={() => setActiveArtifact('human')}>Human Guide (docs/)</button>
            </div>
            <div className="viewer-window">
              <div className="viewer-header">Viewing: {Artifacts[activeArtifact].title}</div>
              <div className="code-body">
                <pre><code>{Artifacts[activeArtifact].content}</code></pre>
              </div>
            </div>
          </div>
        </section>

        {/* WHY DOCAGENT SECTION */}
        <section className="section" id="why-docagent">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Prompting Paradox</span>
            <h2>Why not just prompt the agent?</h2>
            <p className="feature-desc">Prompting works for small fixes, but fails for long-term repo maintenance. Ephemeral chat histories drift, context limits overflow, and different agents hallucinate different rules.</p>
          </div>

          <div className="drift-visual scroll-reveal">
            <div className="drift-card bad">
              <div className="drift-title">Ephemeral Prompting</div>
              <ul className="mini-features" style={{ color: '#f87171' }}>
                <li>❌ Knowledge expires mid-session</li>
                <li>❌ Inconsistent for different agents</li>
                <li>❌ Fails on large, messy context</li>
                <li>❌ Manual drift, higher hallucinations</li>
              </ul>
            </div>
            <div className="drift-card good">
              <div className="drift-title">Systemic Documentation</div>
              <ul className="mini-features">
                <li>✅ Persistent /AGENTS baseline</li>
                <li>✅ Unified truth for every agent</li>
                <li>✅ Scales to complex, low-doc repos</li>
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
            <div className="eyebrow" style={{ color: '#fff' }}>Grounded Development</div>
            <h2>Protect your repo from knowledge drift.</h2>
            <p className="hero-text" style={{ margin: '0 auto 48px' }}>Move from ephemeral chat history to a durable knowledge system.</p>
            <div className="hero-actions" style={{ justifyContent: 'center' }}>
              <div className="install-box">
                <code>npm install -g doc-for-agent</code>
              </div>
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
