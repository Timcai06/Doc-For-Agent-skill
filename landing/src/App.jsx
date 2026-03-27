import React, { useEffect, useState } from 'react';

// --- Icon Components (Inline SVG) ---
const IconInit = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>;
const IconDoctor = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 14 4-4"/><path d="m3.34 19 1.4-1.4"/><path d="m19.07 4.93-1.4 1.4"/><path d="M7.5 7.5c1.4-1.4 4.5-.4 4.5.5C12 9 10 11 10 12s2 2 3 3c.9 0 1.9 3.1.5 4.5-1.4 1.4-4.5.4-4.5-.5 0-1 2-3 2-4s-2-2-3-3c-.9 0-1.9-3.1-.5-4.5Z"/></svg>;
const IconRefresh = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><polyline points="21 3 21 8 16 8"/></svg>;
const IconMigrate = () => <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v8"/><path d="m16 6-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>;

const Scenarios = [
  {
    title: "Scenario: The 'Ghost' Repository",
    status: "Newly inherited or 0-doc debt repo.",
    action: "docagent init",
    proof: "Deep-scans AST and folder patterns to generate a baseline. Found 14 modules, 8 core entry points, and mapped 100% of the architecture in 15 seconds.",
    label: "Baseline Created"
  },
  {
    title: "Scenario: Documentation Debt",
    status: "Scattered, outdated READMEs and wiki notes.",
    action: "docagent migrate + doctor",
    proof: "Absorbs legacy files, deduplicates overlapping info, and flags 12 inconsistencies between code logic and current human-written docs.",
    label: "Knowledge Unified"
  },
  {
    title: "Scenario: High-Speed Refactor",
    status: "Syncing docs with branch main-v2 velocity.",
    action: "docagent refresh",
    proof: "Automatically updates both AGENTS/ and docs/ based on the latest diffs. 0 manual copy-pasting needed for cross-session agent handoffs.",
    label: "Active Sync"
  }
];

const Artifacts = {
  human: {
    title: "docs/onboarding.md",
    lang: "markdown",
    content: `# Onboarding Guide
## Core Concepts
The system uses a **Plugin-based** architecture.
To extend, see \`/src/plugins\`.

## Getting Started
1. \`npm install\`
2. \`docagent init\`
3. \`docagent refresh\``
  },
  agent: {
    title: "AGENTS/source-of-truth.json",
    lang: "json",
    content: `{
  "project_type": "nodejs/vite",
  "entry_points": ["src/main.jsx"],
  "knowledge_graph": {
    "nodes": 42,
    "edges": 128
  },
  "constraints": [
    "No global state",
    "Tailwind not allowed"
  ]
}`
  }
};

const commands = [
  { name: 'init', desc: 'Initialize documentation system from scratch', status: 'Production' },
  { name: 'doctor', desc: 'Audit current documentation for drift and health', status: 'Stable' },
  { name: 'refresh', desc: 'Sync documentation with the latest code state', status: 'Production' },
  { name: 'migrate', desc: 'Inhale and systemize legacy documentation files', status: 'Beta' },
  { name: 'generate', desc: 'Force-generate specific artifact subsets', status: 'Stable' },
];

const heroCases = [
  {
    label: 'Agent Skill',
    title: 'Codex / Agentic Workflow',
    command: 'tim@macBook ~ % @codex Use docagent to audit this branch.',
    output: [
      { text: 'Codex: Calling doc-for-agent skill...', color: 'var(--primary)' },
      { text: '$ docagent doctor --root .', color: 'var(--text-secondary)' },
      { text: '[1/2] Auditing knowledge drift...', color: 'var(--text-secondary)' },
      { text: '✓ No drift detected in 24 files.', color: 'var(--accent)' },
      { text: '[2/2] Status: Systemic Integrity Confirmed.', color: 'var(--accent)' },
      { text: 'Codex: Doc-for-agent confirms your context is grounded.', color: 'var(--primary)' },
    ]
  },
  {
    label: 'docagent init',
    title: 'Initialize System',
    command: 'tim@macBook ~ % docagent init --ai codex',
    output: [
      { text: '[1/3] Analyzing repo architecture...', color: 'var(--text-secondary)' },
      { text: '✓ Detected 4 microservices', color: 'var(--accent)' },
      { text: '✓ Found legacy docs in /wiki', color: 'var(--accent)' },
      { text: '[2/3] Synthesizing Dual-Docs...', color: 'var(--text-secondary)' },
      { text: '+ Created /AGENTS/ (Source of Truth)', color: '#fff' },
      { text: '+ Structured /docs/ (Human Guides)', color: '#fff' },
    ]
  },
  {
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

function App() {
  const [activeArtifact, setActiveArtifact] = useState('agent');
  const [activeHeroCase, setActiveHeroCase] = useState(0);

  // Auto-switching disabled as per user request
  // useEffect(() => {
  //   const timer = setInterval(() => {
  //     setActiveHeroCase((prev) => (prev + 1) % heroCases.length);
  //   }, 5000);
  //   return () => clearInterval(timer);
  // }, []);

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
          <strong>doc-for-agent</strong>
          <small>v1.2.0 "Systemic"</small>
        </a>
        <nav className="nav-links">
          <a href="#scenarios">Capabilities</a>
          <a href="#artifacts">The Output</a>
          <a href="#status">Product Matrix</a>
          <a className="nav-cta" href="#cta">View on GitHub</a>
        </nav>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="hero section" id="hero">
          <div className="hero-copy scroll-reveal">
            <span className="eyebrow">Universal Agentic Skill</span>
            <h1>
              Proof-of-Documentation <br />
              <span style={{ color: 'var(--primary)' }}>for AI Workflows.</span>
            </h1>
            <p className="hero-text">
              The purpose-built documentation skill for CLI coding agents. Maintain systemic ground truth within <strong>Codex, Claude Code, and Copilot sessions.</strong>
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#artifacts">See the Artifacts</a>
              <a className="button button-secondary" href="#scenarios">Handoff Scenarios</a>
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
                <div className="terminal-title">
                  zsh — {heroCases[activeHeroCase].title}
                </div>
              </div>
              <div className="terminal-tabs">
                {heroCases.map((c, i) => (
                  <button 
                    key={i} 
                    className={`terminal-tab-btn ${activeHeroCase === i ? 'active' : ''}`}
                    onClick={() => setActiveHeroCase(i)}
                  >
                    {c.label}
                  </button>
                ))}
              </div>
              <div className="code-body terminal-body">
                <div className="terminal-line command" style={{ borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '12px', marginBottom: '16px' }}>
                  <span className="prompt" style={{ color: 'var(--accent)' }}>%</span> {heroCases[activeHeroCase].command.split('%')[1]?.trim() || heroCases[activeHeroCase].command}
                </div>
                <div className="terminal-output">
                  {heroCases[activeHeroCase].output.map((line, i) => (
                    <div key={i} className="terminal-line" style={{ color: line.color, animationDelay: `${i * 100}ms` }}>
                      {line.text}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* SCENARIO PROOF SECTION */}
        <section className="section" id="scenarios">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Real Challenges</span>
            <h2>Proven solutions for chaotic repositories.</h2>
          </div>
          
          <div className="scenario-grid scroll-reveal" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '24px' }}>
            {Scenarios.map((s, idx) => (
              <div className="bento-item glass-card" key={idx} style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
                <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--primary)', textTransform: 'uppercase' }}>{s.action}</div>
                <h3>{s.title}</h3>
                <div className="scenario-content" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                  <p style={{ marginBottom: '8px' }}><strong>Status:</strong> {s.status}</p>
                  <p><strong>Actual Work:</strong> {s.proof}</p>
                </div>
                <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid var(--line)' }}>
                  <span className="cmd-pill" style={{ fontSize: '0.75rem' }}>{s.label}</span>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* ARTIFACT SHOWCASE SECTION */}
        <section className="section" id="artifacts">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Dual-Doc Output</span>
            <h2>Real context, strictly delivered.</h2>
            <p className="feature-desc">Our engine delivers separate outputs for humans and machines simultaneously.</p>
          </div>

          <div className="artifact-viewer scroll-reveal" style={{ maxWidth: '900px', margin: '0 auto', background: 'var(--surface)', border: '1px solid var(--line)', borderRadius: 'var(--radius-lg)', overflow: 'hidden' }}>
            <div className="viewer-tabs" style={{ display: 'flex', borderBottom: '1px solid var(--line)', background: 'rgba(255,255,255,0.03)' }}>
              <button 
                className={`tab ${activeArtifact === 'agent' ? 'active' : ''}`}
                style={{ flex: 1, padding: '16px', border: 'none', background: activeArtifact === 'agent' ? 'var(--primary)' : 'transparent', color: '#fff', cursor: 'pointer', fontWeight: 600 }}
                onClick={() => setActiveArtifact('agent')}
              >
                /AGENTS (Machine Truth)
              </button>
              <button 
                className={`tab ${activeArtifact === 'human' ? 'active' : ''}`}
                style={{ flex: 1, padding: '16px', border: 'none', background: activeArtifact === 'human' ? 'var(--primary)' : 'transparent', color: '#fff', cursor: 'pointer', fontWeight: 600 }}
                onClick={() => setActiveArtifact('human')}
              >
                /docs (Human Guides)
              </button>
            </div>
            <div className="viewer-content" style={{ padding: '32px' }}>
              <div style={{ marginBottom: '16px', fontSize: '0.8rem', opacity: 0.5 }}>{Artifacts[activeArtifact].title}</div>
              <div className="code-window" style={{ background: '#0a0c10' }}>
                <div className="code-body">
                  <pre style={{ margin: 0, overflowX: 'auto', whiteSpace: 'pre-wrap' }}>
                    <code>{Artifacts[activeArtifact].content}</code>
                  </pre>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* PRODUCT MATRIX SECTION */}
        <section className="section" id="status">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Product Status</span>
            <h2>Command-Line Capability Matrix</h2>
          </div>
          <div className="glass-card scroll-reveal" style={{ maxWidth: '1000px', margin: '0 auto', overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--line)', textAlign: 'left' }}>
                  <th style={{ padding: '20px', color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Command</th>
                  <th style={{ padding: '20px', color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Internal Logic</th>
                  <th style={{ padding: '20px', color: 'var(--text-muted)', fontSize: '0.75rem', textTransform: 'uppercase' }}>Status</th>
                </tr>
              </thead>
              <tbody>
                {commands.map(cmd => (
                  <tr key={cmd.name} style={{ borderBottom: '1px solid var(--line)' }}>
                    <td style={{ padding: '20px' }}><code>docagent {cmd.name}</code></td>
                    <td style={{ padding: '20px', color: 'var(--text-secondary)', fontSize: '0.9rem' }}>{cmd.desc}</td>
                    <td style={{ padding: '20px' }}>
                      <span className={`cmd-pill status-${cmd.status.toLowerCase()}`} style={{ background: cmd.status === 'Production' ? 'var(--accent-glow)' : 'rgba(255,255,255,0.05)', color: cmd.status === 'Production' ? 'var(--accent)' : '#fff', padding: '4px 12px', borderRadius: '4px', fontSize: '0.8rem' }}>
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
          <div className="cta-card scroll-reveal" style={{ textAlign: 'center', padding: '80px 40px' }}>
            <h2>Ready to systemize?</h2>
            <p className="hero-text" style={{ margin: '0 auto 48px' }}>
              Run the CLI on your messiest repo and see the Dual-Doc model in action.
            </p>
            <div className="hero-actions" style={{ justifyContent: 'center' }}>
              <div className="code-window" style={{ background: 'var(--bg)', padding: '16px 40px', border: '1px solid var(--primary)' }}>
                <code style={{ fontSize: '1.2rem', color: '#fff' }}>npm install -g doc-for-agent</code>
              </div>
            </div>
          </div>
        </section>
      </main>

      <footer style={{ padding: '64px 0', textAlign: 'center', color: 'var(--text-muted)', borderTop: '1px solid var(--line)' }}>
        <p>&copy; 2026 doc-for-agent. Stability-first documentation system.</p>
      </footer>
    </div>
  );
}

export default App;
