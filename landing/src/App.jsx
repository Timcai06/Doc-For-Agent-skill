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
            <span className="eyebrow">Durable Context for the Agentic Era</span>
            <h1>
              Stop wasting context in <span style={{ color: 'var(--primary)' }}>single-use chats.</span>
            </h1>
            <p className="hero-text">
              Build a permanent documentation system for your coding agents. 
              doc-for-agent turns raw codebases into systemized knowledge that stays fresh across every Claude Code, Codex, and Copilot session.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#how-it-works">Get the lifecycle</a>
              <a className="button button-secondary" href="#comparison">System vs. Prompting</a>
            </div>
          </div>

          <div className="hero-preview">
            <div className="glass-card floating">
              <div className="code-window">
                <div className="code-header">
                  <span style={{ fontSize: '0.7rem', color: 'var(--muted)', marginLeft: 'auto', marginRight: '8px' }}>docagent init</span>
                  <div className="dot red" />
                  <div className="dot yellow" />
                  <div className="dot green" />
                </div>
                <div className="code-body">
                  <code style={{ fontSize: '0.9rem' }}>
                    <span style={{ color: 'var(--primary)' }}>$</span> docagent init --ai codex<br /><br />
                    <span style={{ color: '#94a3b8' }}>[1/3] Analyzing repo structure...</span><br />
                    <span style={{ color: '#10b981' }}>✓ Found supporting docs in /legacy</span><br />
                    <span style={{ color: '#10b981' }}>✓ Identified 12 core entry points</span><br />
                    <span style={{ color: '#94a3b8' }}>[2/3] Synthesizing knowledge...</span><br />
                    <span style={{ color: '#10b981' }}>✓ Created systemized docs/</span><br />
                    <span style={{ color: '#10b981' }}>✓ Created AGENTS/ source-of-truth</span><br /><br />
                    <span style={{ color: '#3b82f6' }}>Done. Your agent is now context-complete.</span>
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
            <span className="eyebrow">The Dual-Doc Advantage</span>
            <h2>One engine, two audiences</h2>
            <p className="feature-desc">Stop splitting your effort. Generate deep context for humans and strict guardrails for agents simultaneously.</p>
          </div>

          <div className="bento-grid">
            <div className="bento-item wide glass-card">
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
                <div className="output-column">
                  <h3 className="feature-title" style={{ color: 'var(--primary)' }}>/docs</h3>
                  <p className="feature-desc" style={{ marginBottom: '16px' }}><strong>Target:</strong> Maintainers & Onboarding</p>
                  <ul className="feature-list feature-desc">
                    <li>Narrative onboarding docs</li>
                    <li>Module dependency graphs</li>
                    <li>Decision records & rationale</li>
                  </ul>
                </div>
                <div className="output-column">
                  <h3 className="feature-title" style={{ color: 'var(--accent)' }}>/AGENTS</h3>
                  <p className="feature-desc" style={{ marginBottom: '16px' }}><strong>Target:</strong> AI Coding Assistants</p>
                  <ul className="feature-list feature-desc">
                    <li>Strict execution guardrails</li>
                    <li>High-density repo maps</li>
                    <li>Multi-session state tracking</li>
                  </ul>
                </div>
              </div>
            </div>
            
            <div className="bento-item glass-card accent-hover">
              <h3 className="feature-title">The "Ghost Repo" Fix</h3>
              <p className="feature-desc">Zero documentation? No problem. docagent reverse-engineers your code artifacts into a systemized baseline in seconds.</p>
            </div>
            
            <div className="bento-item glass-card accent-hover">
              <h3 className="feature-title">The "Messy Docs" Fix</h3>
              <p className="feature-desc">Scattered READMEs and outdated notes get absorbed, deduplicated, and unified into the new lifecycle model.</p>
            </div>

            <div className="bento-item wide glass-card">
              <h3 className="feature-title">The Stability Lifecycle</h3>
              <div className="command-pills" style={{ marginTop: '16px' }}>
                {['init', 'doctor', 'refresh', 'migrate'].map(cmd => (
                  <code key={cmd} className="cmd-pill">
                    docagent {cmd}
                  </code>
                ))}
              </div>
              <p className="feature-desc" style={{ marginTop: '16px' }}>
                Move from "initial generation" to "continuous health." The doc-for-agent lifecycle ensures your agent context stays as fresh as your main branch.
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
          <div className="glass-card" style={{ textAlign: 'center', padding: '80px 40px', background: 'linear-gradient(135deg, var(--bg) 0%, var(--primary-glow) 100%)', border: '1px solid var(--primary)' }}>
            <h2 style={{ fontSize: '3rem' }}>Ready to systemize your repository?</h2>
            <p className="hero-text" style={{ margin: '24px auto' }}>
              Join the developers who prioritize durable context over single-use prompts. 
              Install doc-for-agent in minutes and start your documentation lifecycle today.
            </p>
            <div className="hero-actions" style={{ justifyContent: 'center' }}>
              <a className="button button-primary" href="#how-it-works">Get Started for Free</a>
              <a className="button button-secondary" href="https://github.com/Doc-For-Agent">View on GitHub</a>
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
