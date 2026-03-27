import React, { useEffect } from 'react';

// --- Icon Components (Inline SVG for Zero-Dependency) ---
const IconInstall = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
);
const IconInit = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
);
const IconRefresh = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><polyline points="21 3 21 8 16 8"/></svg>
);
const IconDoctor = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m12 14 4-4"/><path d="m3.34 19 1.4-1.4"/><path d="m19.07 4.93-1.4 1.4"/><path d="M7.5 7.5c1.4-1.4 4.5-.4 4.5.5C12 9 10 11 10 12s2 2 3 3c.9 0 1.9 3.1.5 4.5-1.4 1.4-4.5.4-4.5-.5 0-1 2-3 2-4s-2-2-3-3c-.9 0-1.9-3.1-.5-4.5Z"/></svg>
);
const IconMigrate = () => (
  <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v8"/><path d="m16 6-4 4-4-4"/><rect width="20" height="8" x="2" y="14" rx="2"/></svg>
);

const lifecycleSteps = [
  { id: 'init', label: 'Init', icon: <IconInit />, desc: 'Deep-scan repository to establish your first knowledge baseline.' },
  { id: 'doctor', label: 'Doctor', icon: <IconDoctor />, desc: 'Identify health gaps and inconsistencies in your current docs.' },
  { id: 'refresh', label: 'Refresh', icon: <IconRefresh />, desc: 'Sync documentation automatically as your code evolving.' },
  { id: 'migrate', label: 'Migrate', icon: <IconMigrate />, desc: 'Absorb legacy notes into a systemized source-of-truth.' },
];

const platforms = [
  { name: 'Claude Code', cmd: 'claude' },
  { name: 'Codex / Cursor', cmd: 'codex' },
  { name: 'CodeBuddy', cmd: 'codex' },
  { name: 'Continue', cmd: 'continue' },
  { name: 'GitHub Copilot', cmd: 'copilot' },
];

function App() {
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
          <a href="#lifecycle">Lifecycle</a>
          <a href="#dual-docs">Dual-Docs</a>
          <a href="#comparison">Stability</a>
          <a href="#platforms">Platforms</a>
          <a className="nav-cta" href="#cta">Install CLI</a>
        </nav>
      </header>

      <main>
        {/* HERO SECTION */}
        <section className="hero section" id="hero">
          <div className="hero-copy scroll-reveal">
            <span className="eyebrow">Beyond Prompting</span>
            <h1>
              Turn raw code into <br />
              <span style={{ color: 'var(--primary)' }}>Systemized Knowledge.</span>
            </h1>
            <p className="hero-text">
              Stop relying on one-off chat sessions. doc-for-agent builds a durable documentation lifecycle that keeps your AI agents sharp and your human team in sync.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#lifecycle">Explore the Lifecycle</a>
              <a className="button button-secondary" href="https://github.com/Doc-For-Agent">View Source</a>
            </div>
          </div>

          <div className="hero-preview scroll-reveal">
            <div className="glass-card floating">
              <div className="code-header">
                <div className="dot red" />
                <div className="dot yellow" />
                <div className="dot green" />
                <span style={{ marginLeft: '12px', fontSize: '12px', color: 'var(--text-muted)' }}>docagent init --ai codex</span>
              </div>
              <div className="code-body">
                <div style={{ color: 'var(--primary)', marginBottom: '8px' }}>$ docagent init --ai codex</div>
                <div style={{ color: 'var(--text-muted)' }}>[1/3] Analyzing repo architecture...</div>
                <div style={{ color: 'var(--accent)' }}>✓ Detected 4 microservices</div>
                <div style={{ color: 'var(--accent)' }}>✓ Found legacy docs in /wiki</div>
                <div style={{ color: 'var(--text-muted)' }}>[2/3] Synthesizing Dual-Docs...</div>
                <div style={{ color: '#fff' }}>+ Created /AGENTS/ (Source of Truth)</div>
                <div style={{ color: '#fff' }}>+ Structured /docs/ (Human Onboarding)</div>
                <div style={{ color: 'var(--warning)', marginTop: '8px' }}>Done. Your agent context is now grounded.</div>
              </div>
            </div>
          </div>
        </section>

        {/* LIFECYCLE SECTION */}
        <section className="section" id="lifecycle">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Documentation Lifecycle</span>
            <h2>Sustainable Context over One-off Prompts.</h2>
            <p className="feature-desc">
              Don't just generate docs once and let them rot. Use our CLI to maintain a living knowledge system.
            </p>
          </div>
          
          <div className="lifecycle-path scroll-reveal">
            <div className="steps-row">
              {lifecycleSteps.map(step => (
                <div className="step-card" key={step.id}>
                  <div className="step-icon">{step.icon}</div>
                  <h3>{step.label}</h3>
                  <p>{step.desc}</p>
                </div>
              ))}
            </div>
            
            <div className="code-window" style={{ width: '100%', maxWidth: '600px' }}>
              <div className="code-body" style={{ textAlign: 'center', fontSize: '1.2rem' }}>
                <code>npm install -g <span style={{ color: 'var(--primary)' }}>doc-for-agent</span></code>
              </div>
            </div>
          </div>
        </section>

        {/* DUAL DOCS SECTION */}
        <section className="section" id="dual-docs">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">The Dual-Doc Model</span>
            <h2>One engine, two audiences.</h2>
            <p className="feature-desc">
              We separate "Agent State" from "Human Guides" to ensure maximum efficiency for both.
            </p>
          </div>

          <div className="bento-grid scroll-reveal">
            <div className="bento-item wide">
              <h3 style={{ color: 'var(--primary)' }}>/AGENTS</h3>
              <p style={{ marginBottom: '24px' }}>Machine-readable source of truth optimized for CLI coding agents like Claude Code and Codex.</p>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                <ul className="feature-desc" style={{ paddingLeft: '20px', fontSize: '0.9rem' }}>
                  <li>Strict execution rules</li>
                  <li>High-density repo maps</li>
                </ul>
                <ul className="feature-desc" style={{ paddingLeft: '20px', fontSize: '0.9rem' }}>
                  <li>Multi-session context</li>
                  <li>Implicit knowledge capture</li>
                </ul>
              </div>
            </div>
            <div className="bento-item">
              <h3 style={{ color: 'var(--accent)' }}>/docs</h3>
              <p>Team-onboarding narratives. Clean, readable, and structured for human maintainers.</p>
            </div>
            <div className="bento-item">
              <h3>Zero-Doc Recovery</h3>
              <p>Reverse-engineer "ghost repositories" into structured baselines in seconds.</p>
            </div>
            <div className="bento-item wide">
              <h3>Intelligent Migration</h3>
              <p>Deduplicate scattered READMEs, outdated wikis, and hidden notes into a unified lifecycle model with zero manual copy-pasting.</p>
            </div>
          </div>
        </section>

        {/* COMPARISON SECTION */}
        <section className="section" id="comparison">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Stability Audit</span>
            <h2>Why a system tool?</h2>
            <p className="feature-desc">Compare systemic documentation with ad-hoc prompting.</p>
          </div>

          <div className="comparison-container scroll-reveal">
            <table className="comparison-table">
              <thead>
                <tr>
                  <th>Capability</th>
                  <th>Ad-hoc Prompting</th>
                  <th>Doc-for-Agent</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Repeatability</td>
                  <td className="status-bad">Session-dependent random</td>
                  <td className="status-good"><span className="status-check">✓</span> Pattern-enforced consistency</td>
                </tr>
                <tr>
                  <td>Sync State</td>
                  <td className="status-bad">Manual refresh only</td>
                  <td className="status-good"><span className="status-check">✓</span> Integrated refresh lifecycle</td>
                </tr>
                <tr>
                  <td>Legacy Context</td>
                  <td className="status-bad">Often ignored or hallucinated</td>
                  <td className="status-good"><span className="status-check">✓</span> Deep-scan migration engine</td>
                </tr>
                <tr>
                  <td>Multi-Agent</td>
                  <td className="status-bad">Locked to one platform</td>
                  <td className="status-good"><span className="status-check">✓</span> Multi-platform ground truth</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        {/* PLATFORMS SECTION */}
        <section className="section" id="platforms">
          <div className="section-head scroll-reveal">
            <span className="eyebrow">Interoperability</span>
            <h2>One command, all platforms.</h2>
          </div>
          <div className="platform-grid scroll-reveal">
            {platforms.map(p => (
              <div className="platform-pill" key={p.name}>
                <span style={{ fontWeight: 700 }}>{p.name}</span>
                <code>--ai {p.cmd}</code>
              </div>
            ))}
          </div>
        </section>

        {/* CTA SECTION */}
        <section className="section" id="cta">
          <div className="cta-card scroll-reveal">
            <h2>Ready to systemize?</h2>
            <p className="hero-text" style={{ margin: '0 auto 48px' }}>
              Join forward-thinking teams moving from chat history to durable repository knowledge.
            </p>
            <div className="hero-actions" style={{ justifyContent: 'center' }}>
              <a className="button button-primary" href="#lifecycle">Start the Lifecycle</a>
              <a className="button button-secondary" href="https://github.com/Doc-For-Agent">GitHub Repository</a>
            </div>
          </div>
        </section>
      </main>

      <footer>
        <p>&copy; 2026 doc-for-agent. Purpose-built for the Agentic Era.</p>
      </footer>
    </div>
  );
}

export default App;
