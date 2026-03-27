import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const Artifacts = {
  human: {
    title: "docs/overview.md",
    content: `# Project Overview\n\n## Purpose\nThis repository provides a CLI-first documentation system for coding-agent workflows.\n\n## Core Outputs\n- \`docs/\` for human maintainers and onboarding\n- \`AGENTS/\` for agent execution and handoff\n\n## Lifecycle\n- \`docagent init\`\n- \`docagent doctor\`\n- \`docagent refresh\``
  },
  agent: {
    title: "AGENTS/03-execution/008-implementation-plan.md",
    content: `# Workflows\n\n## Top Rules (Read First)\n- Verify before merging.\n- Use the documented command path, not ad-hoc prompts.\n- Escalate source-of-truth conflicts before editing.\n\n## Run\n- \`docagent init --ai codex --target .\`\n- \`docagent refresh --root . --output-mode dual\``
  }
};

const heroCases = [
  {
    index: 0,
    label: 'Agent Skill',
    title: 'Codex / Agentic Workflow',
    command: 'tim@macBook ~ % @codex Use doc-for-agent to check the current branch health.',
    output: [
      { text: 'Codex: Calling doc-for-agent skill...', color: 'var(--primary)' },
      { text: '$ docagent doctor --target . --platform codex', color: 'var(--text-secondary)' },
      { text: '[1/2] Auditing knowledge drift...', color: 'var(--text-secondary)' },
      { text: '✓ No drift detected in 24 core modules.', color: 'var(--accent)' },
      { text: '[2/2] Status: Systemic Integrity Confirmed.', color: 'var(--accent)' },
      { text: 'Codex: Context grounded. You are ready to proceed.', color: 'var(--primary)' },
    ]
  },
  {
    index: 1,
    label: 'docagent init',
    title: 'Initialize System',
    command: 'tim@macBook ~ % docagent init --ai codex --target .',
    output: [
      { text: '[1/3] Scanning repository depth...', color: 'var(--text-secondary)' },
      { text: '✓ Detected CLI-first repo with existing product docs', color: 'var(--accent)' },
      { text: '[2/3] Building dual documentation baseline...', color: 'var(--text-secondary)' },
      { text: '+ Generated /AGENTS/ (Machine Source-of-Truth)', color: '#fff' },
      { text: '+ Generated /docs/ (Human-Centric Guides)', color: '#fff' },
      { text: '[3/3] Done. Baseline established for all agents.', color: 'var(--accent)' },
    ]
  },
  {
    index: 2,
    label: 'docagent refresh',
    title: 'Lifecycle Sync',
    command: 'tim@macBook ~ % docagent refresh --root . --output-mode dual',
    output: [
      { text: '[1/2] Detecting code evolution...', color: 'var(--text-secondary)' },
      { text: '✓ Supporting docs and code signals changed', color: 'var(--accent)' },
      { text: '[2/2] Synchronizing dual documentation...', color: 'var(--text-secondary)' },
      { text: '↺ AGENTS/ updated for agent execution', color: '#fff' },
      { text: '↺ docs/ updated for maintainers and onboarding', color: '#fff' },
      { text: 'Lifecycle Sync complete (8s).', color: 'var(--primary)' },
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
              The Documentation System <br />
              <span style={{ color: 'var(--primary)' }}>for CLI Coding Agents.</span>
            </h1>
            <p className="hero-text">
              Transform raw code into a durable, systemic knowledge base. Stop relying on one-off chat sessions; build a persistent bridge between your code and your agents.
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
            <span className="eyebrow">The Dual-Doc Advantage</span>
            <h2>One engine. Two core audiences. ZERO drift.</h2>
            <p className="feature-desc">By using a unified analysis engine, we maintain perfect synchronization between internal machine truth and external human guides.</p>
          </div>

          <div className="sync-diagram scroll-reveal">
             <div className="sync-part">
               <div className="circle-pulse accent" />
               <strong>Unified Analysis Engine</strong>
               <p>Deep scan of directory structure, AST, and legacy artifacts.</p>
             </div>
             <div className="sync-arrow">
               <svg width="40" height="24" viewBox="0 0 40 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h30"/><path d="m28 5 7 7-7 7"/></svg>
             </div>
             <div className="sync-results">
               <div className="res-card agent"><strong>/AGENTS/</strong> Machine Truth</div>
               <div className="res-card human"><strong>/docs/</strong> Human Narrative</div>
             </div>
          </div>

          <div className="dual-grid scroll-reveal" style={{ marginTop: '64px' }}>
            <div className="dual-card agent">
              <div className="card-label">FOR AGENTS (The Context)</div>
              <h3>/AGENTS/ Baseline</h3>
              <p>Actionable, high-density knowledge maps. Designed for Claude Code, Codex, Continue, and Copilot to navigate massive codebases with zero-hallucination precision.</p>
              <ul className="mini-features">
                <li>✓ Execution Invariants</li>
                <li>✓ Cross-session Memory</li>
                <li>✓ Rapid AST Navigation</li>
              </ul>
            </div>
            <div className="dual-card human (The Onboarding)">
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
              { type: 'Low-Doc Repo', desc: 'From zero baseline to professional documentation structure in seconds.' },
              { type: 'Messy-Doc Repo', desc: 'Inhale scattered READMEs and systemize them into a durable Dual-Doc system.' },
              { type: 'Agent-Ready Repo', desc: 'Maintain peak efficiency for every agent session with automated lifecycle sync.' }
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
            <span className="eyebrow">The Prompting Trap</span>
            <h2>Stop chat-history knowledge rot.</h2>
            <p className="feature-desc">Sessions drift. Knowledge vanishes. HALLUCINATIONS increase as repositories grow. doc-for-agent provides the systemic ground truth that ephemeral chats lack.</p>
          </div>

          <div className="drift-visual scroll-reveal">
            <div className="drift-card bad">
              <div className="drift-title">Ad-hoc Prompting</div>
              <ul>
                <li>❌ Knowledge expires mid-session</li>
                <li>❌ Inconsistent for different agents</li>
                <li>❌ Manual sync, manual copy-paste</li>
              </ul>
            </div>
            <div className="drift-card good">
              <div className="drift-title">Doc-for-Agent System</div>
              <ul>
                <li>✅ Persistent /AGENTS baseline</li>
                <li>✅ Unified truth for every agent</li>
                <li>✅ Automated CLI refresh cycle</li>
              </ul>
            </div>
          </div>
        </section>

        {/* SETUP WORKFLOW */}
        <section className="section" id="workflow">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Path</span>
            <h2>Install. Init. Refresh.</h2>
          </div>
          <div className="workflow-grid scroll-reveal">
            <div className="workflow-card">
              <div className="step-num">01</div>
              <h3>Global Install</h3>
              <p>Equip your environment with the systemic CLI engine.</p>
              <code>npm install -g doc-for-agent</code>
            </div>
            <div className="workflow-card">
              <div className="step-num">02</div>
              <h3>System Init</h3>
              <p>Scan baseline and establish your Dual-Doc foundation.</p>
              <code>docagent init --ai codex</code>
            </div>
            <div className="workflow-card">
              <div className="step-num">03</div>
              <h3>Active Refresh</h3>
              <p>Sync knowledge as code evolves. Zero-manual overhead.</p>
              <code>docagent refresh</code>
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
