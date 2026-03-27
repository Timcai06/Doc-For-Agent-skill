import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const Artifacts = {
  human: {
    title: "docs/architecture.md",
    content: `# Architecture Overview\n\n## Narrative Context\nThis repository implements a rule-based documentation engine. It prioritizes clarity for human onboarding.\n\n## Core Logic\n- Unified Scan: One pass for both target outputs.\n- Drift Detection: Automated sync checks.\n\n## How to Maintain\nUse \`docagent refresh\` after significant AST changes.`
  },
  agent: {
    title: "AGENTS/00-context/002-rules.md",
    content: `# Execution Rules\n\n## Path Mapping\n- Source: /src/core\n- Documentation: /docs\n\n## Constraints (Machine Truth)\n- STRICT: Do not modify index.js directly.\n- REQUIRED: Run @docagent-doctor before every task.\n- INVARIANT: All skills must reside in /AGENTS/skills.`
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
      { text: '[3/3] Systemic Bridge established.', color: 'var(--accent)' },
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
      { text: 'Refresh complete (1.2s). All agents aligned.', color: 'var(--primary)' },
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
      { text: 'Status: Systemic Integrity Confirmed.', color: 'var(--primary)' },
    ]
  }
];

const commands = [
  { name: 'init', desc: 'Bootstrap the Dual-Doc system from zero-knowledge state', status: 'Production' },
  { name: 'doctor', desc: 'Audit repository stability and documentation health', status: 'Stable' },
  { name: 'refresh', desc: 'Sync documentation with real-time code evolution', status: 'Production' },
  { name: 'migrate', desc: 'Systemize scattered READMEs into structured baselines', status: 'Beta' },
  { name: 'generate', desc: 'Produce machine-first artifacts for specific AI agents', status: 'Stable' },
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
              The Systemic Bridge <br />
              <span style={{ color: 'var(--primary)' }}>Between Code and Agents.</span>
            </h1>
            <p className="hero-text">
              Transform messy, low-doc repositories into a durable <strong>Dual-Doc system</strong>. Persistent Machine Truth for Agents, Clear Narrative for Humans. Zero drift, full alignment.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#workflow">Start Lifecycle</a>
              <a className="button button-secondary" href="#dual-logic">The Dual-Doc Advantage</a>
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
            <span className="eyebrow">The Dual-Doc Architecture</span>
            <h2>One scan. Two worlds. Zero drift.</h2>
            <p className="feature-desc">Why maintain two sets of docs? Because agents need <strong>Execution Rules</strong> while humans need <strong>Architectural Narrative</strong>. We generate both from a single source of truth.</p>
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
                 <div className="res-card agent"><strong>/AGENTS/</strong> Machine Truth</div>
                 <div className="res-card human"><strong>/docs/</strong> Human Narrative</div>
               </div>
               <strong>Dual-Doc Ecosystem</strong>
               <p>Synchronized, systemic knowledge.</p>
             </div>
          </div>

          <div className="dual-grid scroll-reveal" style={{ marginTop: '64px' }}>
            <div className="dual-card agent">
              <div className="card-label">FOR AGENTS (The Context)</div>
              <h3>/AGENTS/ Baseline</h3>
              <p>Actionable, high-density knowledge maps. Designed for Claude Code, Codex, and Continue to navigate repositories with machine-level precision.</p>
              <ul className="mini-features">
                <li>✓ Execution Invariants</li>
                <li>✓ Cross-session Memory</li>
                <li>✓ Faster Repo Navigation</li>
              </ul>
            </div>
            <div className="dual-card human">
              <div className="card-label">FOR HUMANS (The Narrative)</div>
              <h3>/docs/ Guides</h3>
              <p>Natural narrative for human maintainers. Perfect documentation for team onboarding, architecture reviews, and technical handoffs.</p>
              <ul className="mini-features">
                <li>✓ Narrative Cohesion</li>
                <li>✓ Maintenance Logic</li>
                <li>✓ Team Alignment</li>
              </ul>
            </div>
          </div>
        </section>

        {/* REPO SCENARIOS SECTION: Explicit Proof */}
        <section className="section" id="scenarios">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Proven Resilience</span>
            <h2>Built for the messiest repositories.</h2>
          </div>
          <div className="scenario-row scroll-reveal">
            {[
              { type: 'Low-Doc Repo', desc: 'Bootstrap a professional documentation system from raw source code and config files.' },
              { type: 'Messy-Doc Repo', desc: 'Inhale scattered, outdated READMEs and systemize them into a durable structured baseline.' },
              { type: 'Scaling Repo', desc: 'Maintain peak alignment for every agent session with automated, recurring lifecycle sync.' }
            ].map(s => (
              <div key={s.type} className="scenario-pill glass-card">
                <strong>{s.type}</strong>
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
                <p>The core of sustainability. Sync knowledge as code evolves, zero-manual overhead.</p>
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
            <span className="eyebrow">Product Integrity</span>
            <h2>Capability Matrix</h2>
          </div>
          <div className="glass-card scroll-reveal" style={{ overflowX: 'auto' }}>
            <table className="capability-table" style={{ width: '100%', textAlign: 'left', borderCollapse: 'separate', borderSpacing: '0 8px' }}>
              <thead>
                <tr>
                  <th style={{ padding: '16px' }}>Command</th>
                  <th style={{ padding: '16px' }}>Systemic Logic</th>
                  <th style={{ padding: '16px' }}>Product Status</th>
                </tr>
              </thead>
              <tbody>
                {commands.map(cmd => (
                  <tr key={cmd.name} style={{ background: 'rgba(255,255,255,0.02)' }}>
                    <td style={{ padding: '16px' }}><code>docagent {cmd.name}</code></td>
                    <td style={{ padding: '16px', color: 'var(--text-secondary)' }}>{cmd.desc}</td>
                    <td style={{ padding: '16px' }}>
                      <span className={`status-badge ${cmd.status.toLowerCase()}`} style={{ fontSize: '0.8rem', padding: '4px 12px', borderRadius: '4px', background: cmd.status === 'Production' ? 'var(--accent-glow)' : 'rgba(255,255,255,0.05)', color: cmd.status === 'Production' ? 'var(--accent)' : '#fff' }}>
                        {cmd.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
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
