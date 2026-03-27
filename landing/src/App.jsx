import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const Artifacts = {
  human: {
    title: "docs/onboarding.md",
    content: `# Onboarding Guide\n## Core Concepts\nThe system uses a **Plugin-based** architecture.\nTo extend, see \`/src/plugins\`.\n\n## Getting Started\n1. \`npm install\`\n2. \`docagent init\`\n3. \`docagent refresh\``
  },
  agent: {
    title: "AGENTS/source-of-truth.json",
    content: `{\n  "project_type": "nodejs/vite",\n  "entry_points": ["src/main.jsx"],\n  "knowledge_graph": {\n    "nodes": 42,\n    "edges": 128\n  },\n  "constraints": [\n    "No global state",\n    "Tailwind not allowed"\n  ]\n}`
  }
};

const heroCases = [
  {
    index: 0,
    label: 'Agent Skill',
    title: 'Codex / Agentic Workflow',
    command: 'tim@macBook ~ % @codex Analyze current branch health.',
    output: [
      { text: 'Codex: Calling doc-for-agent skill...', color: 'var(--primary)' },
      { text: '$ docagent doctor --root .', color: 'var(--text-secondary)' },
      { text: '[1/2] Auditing knowledge drift...', color: 'var(--text-secondary)' },
      { text: '✓ No drift detected in 24 core modules.', color: 'var(--accent)' },
      { text: '[2/2] Status: Systemic Integrity Confirmed.', color: 'var(--accent)' },
      { text: 'Codex: Doc-for-agent grounded your context.', color: 'var(--primary)' },
    ]
  },
  {
    index: 1,
    label: 'docagent init',
    title: 'Initialize System',
    command: 'tim@macBook ~ % docagent init --ai codex',
    output: [
      { text: '[1/3] Analyzing repo architecture...', color: 'var(--text-secondary)' },
      { text: '✓ Detected 4 microservices', color: 'var(--accent)' },
      { text: '✓ Found legacy docs in /wiki', color: 'var(--accent)' },
      { text: '[2/3] Synthesizing Dual-Docs...', color: 'var(--text-secondary)' },
      { text: '+ Created /AGENTS/ (Source of Truth)', color: '#fff' },
      { text: '+ Structured /docs/ (Human Onboarding)', color: '#fff' },
    ]
  },
  {
    index: 2,
    label: 'docagent refresh',
    title: 'Sync Lifecycle',
    command: 'tim@macBook ~ % docagent refresh --ai all',
    output: [
      { text: '[1/2] Scanning branch feature/v2...', color: 'var(--text-secondary)' },
      { text: '✓ 14 files changed', color: 'var(--accent)' },
      { text: '[2/2] Syncing documentation...', color: 'var(--text-secondary)' },
      { text: '✓ AGENTS/context.json updated', color: '#fff' },
      { text: '✓ docs/CHANGELOG.md updated', color: '#fff' },
      { text: 'Sync complete (12s).', color: 'var(--primary)' },
    ]
  }
];

const commands = [
  { name: 'init', desc: 'Initialize documentation system from scratch', status: 'Production' },
  { name: 'doctor', desc: 'Audit current documentation for drift and health', status: 'Stable' },
  { name: 'refresh', desc: 'Sync documentation with the latest code state', status: 'Production' },
  { name: 'migrate', desc: 'Inhale and systemize legacy documentation files', status: 'Beta' },
  { name: 'generate', desc: 'Force-generate specific artifact subsets', status: 'Stable' },
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
          <a href="#why-stability">Why?</a>
          <a href="#workflow">Path</a>
          <a href="#artifacts">Outputs</a>
          <a href="#status">Matrix</a>
          <a className="nav-cta" href="https://github.com/Doc-For-Agent">GitHub</a>
        </nav>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="hero section" id="hero">
          <div className="hero-copy scroll-reveal">
            <div className="badge-technical" style={{ borderRadius: '100px', padding: '6px 16px', marginBottom: '16px' }}>Stable Source-of-Truth</div>
            <h1>
              Ground your Agents. <br />
              <span style={{ color: 'var(--primary)' }}>Sustain your Knowledge.</span>
            </h1>
            <p className="hero-text">
              The purpose-built documentation skill for CLI coding agents. Stop relying on one-off chat sessions; build a durable knowledge bridge between your code, your team, and your agents.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#workflow">Get Started</a>
              <a className="button button-secondary" href="#artifacts">Explore Artifacts</a>
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

        {/* WHY STABILITY */}
        <section className="section" id="why-stability">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Prompting Trap</span>
            <h2>One-off chats are not documentation.</h2>
            <p className="feature-desc">Sessions drift. Knowledge vanishes. Agents hallucinate in messy repositories. We provide the systemic "Ground Truth" that ephemeral sessions lack.</p>
          </div>

          <div className="drift-visual scroll-reveal">
            <div className="drift-card bad">
              <div className="drift-title">Ad-hoc Prompting</div>
              <ul>
                <li>❌ Knowledge expires with session</li>
                <li>❌ Inconsistent for different agents</li>
                <li>❌ Manual sync, manual copy-paste</li>
              </ul>
            </div>
            <div className="drift-card good">
              <div className="drift-title">Doc-for-Agent Skill</div>
              <ul>
                <li>✅ Persistent /AGENTS baseline</li>
                <li>✅ Unified truth for every agent</li>
                <li>✅ Automated CLI refresh cycle</li>
              </ul>
            </div>
          </div>
        </section>

        {/* WORKFLOW */}
        <section className="section" id="workflow">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Lifecycle</span>
            <h2>Install. Init. Refresh.</h2>
          </div>
          <div className="workflow-grid scroll-reveal">
            <div className="workflow-card">
              <div className="step-num">01</div>
              <h3>Global Install</h3>
              <p>Equip your machine with the systemic CLI engine via NPM.</p>
              <code>npm install -g doc-for-agent</code>
            </div>
            <div className="workflow-card">
              <div className="step-num">02</div>
              <h3>Scan & Init</h3>
              <p>Analyze repo architecture and legacy docs into a systemic baseline.</p>
              <code>docagent init --ai codex</code>
            </div>
            <div className="workflow-card">
              <div className="step-num">03</div>
              <h3>Continuous Refresh</h3>
              <p>Sync knowledge as your code evolves. No more outdated docs.</p>
              <code>docagent refresh</code>
            </div>
          </div>
        </section>

        {/* ARTIFACTS */}
        <section className="section" id="artifacts">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">System Architecture</span>
            <h2>The Dual-Doc Balance.</h2>
          </div>

          <div className="artifact-viewer scroll-reveal">
            <div className="viewer-tabs">
              <button 
                className={`tab ${activeArtifact === 'agent' ? 'active' : ''}`}
                onClick={() => setActiveArtifact('agent')}
              >
                /AGENTS (Machine Truth)
              </button>
              <button 
                className={`tab ${activeArtifact === 'human' ? 'active' : ''}`}
                onClick={() => setActiveArtifact('human')}
              >
                /docs (Human Guides)
              </button>
            </div>
            <div className="viewer-window">
              <div className="viewer-header">
                <strong>{Artifacts[activeArtifact].title}</strong>
              </div>
              <div className="code-body">
                <pre><code>{Artifacts[activeArtifact].content}</code></pre>
              </div>
            </div>
          </div>
        </section>

        {/* STATUS MATRIX */}
        <section className="section" id="status">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Capabilities</span>
            <h2>Command-Line Matrix</h2>
          </div>
          <div className="glass-card scroll-reveal" style={{ overflowX: 'auto' }}>
            <table className="capability-table" style={{ width: '100%', textAlign: 'left', borderCollapse: 'separate', borderSpacing: '0 8px' }}>
              <thead>
                <tr>
                  <th style={{ padding: '16px' }}>Command</th>
                  <th style={{ padding: '16px' }}>Internal Mechanism</th>
                  <th style={{ padding: '16px' }}>Status</th>
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
          <div className="cta-card scroll-reveal main-cta" style={{ textAlign: 'center', padding: '80px 40px', background: 'linear-gradient(135deg, var(--surface) 0%, var(--primary-glow) 100%)', borderRadius: 'var(--radius-xl)', border: '1px solid var(--primary)' }}>
            <div className="eyebrow" style={{ color: '#fff' }}>Production Ready</div>
            <h2>Protect your repo from knowledge rot.</h2>
            <p className="hero-text" style={{ margin: '0 auto 48px' }}>Join teams moving from ephemeral prompts to durable repository systemics.</p>
            <div className="hero-actions" style={{ justifyContent: 'center' }}>
              <div className="install-box" style={{ background: 'var(--bg)', padding: '16px 32px', border: '1px solid var(--primary)', borderRadius: '8px' }}>
                <code>npm install -g doc-for-agent</code>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer style={{ padding: '64px 0', textAlign: 'center', color: 'var(--text-muted)', borderTop: '1px solid var(--line)' }}>
        <p>&copy; 2026 doc-for-agent. Stability-first system for the Agentic Era.</p>
      </footer>
    </div>
  );
}

export default App;
