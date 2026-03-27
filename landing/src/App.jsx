import React from 'react';
import { LogoMark } from './components/LogoMark';

const steps = [
  {
    id: '01',
    label: 'Install',
    title: 'Shortest path to start',
    body: 'One CLI for Node and Python environments. Universal docagent command surface.',
    command: 'npm install -g doc-for-agent',
  },
  {
    id: '02',
    label: 'Init',
    title: 'Initialize your agent context',
    body: 'Deep-scan your repository and generate your first source-of-truth documentation system.',
    command: 'docagent init --ai codex --target .',
  },
  {
    id: '03',
    label: 'Refresh',
    title: 'Maintain the lifecycle',
    body: 'As your code evolves, your docs stay in sync. Reliable, repeatable updates.',
    command: 'docagent refresh --root . --output-mode dual',
  },
];

const platforms = [
  { name: 'Claude Code', flag: 'claude' },
  { name: 'Codex / Cursor', flag: 'codex' },
  { name: 'CodeBuddy', flag: 'codex' },
  { name: 'Continue', flag: 'continue' },
  { name: 'GitHub Copilot', flag: 'copilot' },
];

function App() {
  return (
    <div className="page-shell">
      <div className="page-backdrop" aria-hidden="true" />
      
      <header className="topbar">
        <a className="brand" href="#hero">
          <LogoMark />
          <span>
            <strong>doc-for-agent</strong>
            <small>v1.0.0 "Stability"</small>
          </span>
        </a>
        <nav className="nav-links" aria-label="Primary">
          <a href="#how-it-works">How it works</a>
          <a href="#comparison">Stability</a>
          <a href="#dual-system">Dual-Docs</a>
          <a href="#platforms">Platforms</a>
          <a className="nav-cta" href="#cta">Get Started</a>
        </nav>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="hero section" id="hero">
          <div className="hero-copy">
            <span className="eyebrow">The Documentation Foundation for Coding Agents</span>
            <h1>
              Turn repository knowledge into a <span style={{ color: 'var(--primary)' }}>stable documentation system.</span>
            </h1>
            <p className="hero-text">
              Built for Claude Code, Codex, and GitHub Copilot users. 
              Move beyond one-off LLM prompts to a maintained, lifecycle-managed doc system that grows with your code.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#how-it-works">See the flow</a>
              <a className="button button-secondary" href="#comparison">Why not just prompt?</a>
            </div>
          </div>

          <div className="hero-preview">
            <div className="glass-card floating">
              <div className="code-window">
                <div className="code-header">
                  <div className="dot red" />
                  <div className="dot yellow" />
                  <div className="dot green" />
                </div>
                <div className="code-body">
                  <code style={{ fontSize: '0.9rem' }}>
                    <span style={{ color: 'var(--primary)' }}>$</span> docagent init --ai codex<br /><br />
                    <span style={{ color: '#94a3b8' }}>Scanning repository...</span><br />
                    <span style={{ color: '#10b981' }}>✓ Found supporting docs</span><br />
                    <span style={{ color: '#10b981' }}>✓ Identified 24 core modules</span><br />
                    <span style={{ color: '#10b981' }}>✓ Initializing docs/ and AGENTS/...</span><br /><br />
                    <span style={{ color: '#3b82f6' }}>System ready. Run docagent refresh to sync.</span>
                  </code>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* CONVERSION PATH SECTION */}
        <section className="section" id="how-it-works">
          <div className="section-head">
            <span className="eyebrow">Installation to Refresh</span>
            <h2>One path, three visible steps</h2>
            <p className="feature-desc">The shortest path for terminal-first teams that want repo docs to stay usable across sessions.</p>
          </div>
          
          <div className="steps-visual">
            {steps.map((step, index) => (
              <React.Fragment key={step.id}>
                <div className="step-node">
                  <div className="step-circle">{step.id}</div>
                  <h3 className="feature-title">{step.label}</h3>
                  <p className="feature-desc" style={{ fontSize: '0.9rem' }}>{step.body}</p>
                </div>
                {index < steps.length - 1 && <div className="step-arrow" />}
              </React.Fragment>
            ))}
          </div>

          <div className="bento-grid" style={{ marginTop: '64px' }}>
            {steps.map((step) => (
              <div className="bento-item glass-card" key={step.id}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '16px' }}>{step.title}</h3>
                <div className="code-window" style={{ background: '#08090a' }}>
                  <div className="code-body" style={{ padding: '12px' }}>
                    <code><span style={{ color: 'var(--primary)' }}>$</span> {step.command}</code>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* COMPARISON SECTION */}
        <section className="section" id="comparison">
          <div className="glass-card" style={{ padding: '64px' }}>
            <div className="section-head">
              <span className="eyebrow">Stability vs. Prompting</span>
              <h2>Why use a system tool instead of just prompting?</h2>
              <p className="feature-desc">Temporary prompts are easy. Long-term maintenance is hard.</p>
            </div>

            <div className="table-container" style={{ overflowX: 'auto' }}>
              <table className="comparison-table">
                <thead>
                  <tr>
                    <th>Feature</th>
                    <th>Direct LLM Prompting</th>
                    <th>doc-for-agent system</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>Consistency</td>
                    <td className="status-bad">Random structure per session</td>
                    <td className="status-good">Unified, repeatable format</td>
                  </tr>
                  <tr>
                    <td>Update Model</td>
                    <td className="status-bad">One-shot / Copy-paste</td>
                    <td className="status-good">Command-based lifecycle (refresh)</td>
                  </tr>
                  <tr>
                    <td>Knowledge Capture</td>
                    <td className="status-bad">Misses non-code context</td>
                    <td className="status-good">Absorbs human docs + code structure</td>
                  </tr>
                  <tr>
                    <td>Handoff</td>
                    <td className="status-bad">Implicit / Hidden in chat</td>
                    <td className="status-good">Explicit AGENTS/ source of truth</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        {/* DUAL SYSTEM SECTION */}
        <section className="section" id="dual-system">
          <div className="section-head">
            <span className="eyebrow">The Dual-Doc Model</span>
            <h2>Serves Humans and Agents together</h2>
          </div>

          <div className="bento-grid">
            <div className="bento-item wide glass-card">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
                <div>
                  <h3 className="feature-title" style={{ color: 'var(--primary)' }}>docs/</h3>
                  <p className="feature-desc">For Maintainers & Humans</p>
                  <ul className="feature-desc" style={{ listStyle: 'disc', paddingLeft: '20px', marginTop: '16px' }}>
                    <li>Project narratives & on-boarding</li>
                    <li>System orientation & high-level architecture</li>
                    <li>Human-readable decision logs</li>
                  </ul>
                </div>
                <div>
                  <h3 className="feature-title" style={{ color: 'var(--accent)' }}>AGENTS/</h3>
                  <p className="feature-desc">For Coding Agents</p>
                  <ul className="feature-desc" style={{ listStyle: 'disc', paddingLeft: '20px', marginTop: '16px' }}>
                    <li>Execution guardrails & strict constraints</li>
                    <li>Repo source-of-truth & navigation</li>
                    <li>Inter-session state / Handoff artifacts</li>
                  </ul>
                </div>
              </div>
            </div>
            <div className="bento-item glass-card">
              <h3 className="feature-title">Reliability</h3>
              <p className="feature-desc">Both sets share a single analysis engine, ensuring zero drift between human intent and agent execution.</p>
            </div>
            
            <div className="bento-item glass-card">
              <h3 className="feature-title">Messy-Doc Ready</h3>
              <p className="feature-desc">Designed to absorb scattered notes, flat AGENTS files, and legacy docs into a clean system.</p>
            </div>
            <div className="bento-item wide glass-card">
              <h3 className="feature-title">The Lifecycle Command Suite</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', marginTop: '16px' }}>
                {['init', 'doctor', 'refresh', 'migrate'].map(cmd => (
                  <code key={cmd} style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--primary)', padding: '4px 12px', borderRadius: '4px' }}>
                    docagent {cmd}
                  </code>
                ))}
              </div>
              <p className="feature-desc" style={{ marginTop: '16px' }}>
                From initial setup to ongoing health checks and legacy migrations—we manage the entire documentation lifecycle.
              </p>
            </div>
          </div>
        </section>

        {/* PLATFORMS SECTION */}
        <section className="section" id="platforms">
          <div className="section-head">
            <span className="eyebrow">Platform Support</span>
            <h2>One interface for every coding agent</h2>
          </div>
          <div className="platform-grid">
            {platforms.map((p) => (
              <div className="platform-card" key={p.name}>
                <span style={{ fontWeight: 600 }}>{p.name}</span>
                <code>docagent init --ai {p.flag}</code>
              </div>
            ))}
          </div>
        </section>

        {/* CTA SECTION */}
        <section className="section cta-section" id="cta">
          <div className="glass-card" style={{ textAlign: 'center', padding: '80px 40px', background: 'linear-gradient(135deg, var(--bg) 0%, var(--primary-glow) 100%)' }}>
            <h2>Ready to build a doc-first repository?</h2>
            <p className="hero-text" style={{ margin: '24px auto' }}>
              Join the teams building with agentic documentation systems. 
              Install doc-for-agent today.
            </p>
            <div className="hero-actions" style={{ justifyContent: 'center' }}>
              <a className="button button-primary" href="#">Install Now</a>
              <a className="button button-secondary" href="https://github.com/Doc-For-Agent">GitHub Repo</a>
            </div>
          </div>
        </section>
      </main>

      <footer style={{ padding: '48px 0', textAlign: 'center', borderTop: '1px solid var(--line)', color: 'var(--muted)', fontSize: '0.9rem' }}>
        <p>&copy; 2026 doc-for-agent. Dedicated to the Agentic Era.</p>
      </footer>
    </div>
  );
}

export default App;
