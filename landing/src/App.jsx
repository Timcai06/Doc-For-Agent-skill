import { LogoMark } from './components/LogoMark';

const steps = [
  {
    id: '01',
    label: 'Install',
    title: 'Choose the shortest path for your setup',
    body: 'Node-first users can start with npm or npx. Python-first users can use pipx and land on the same docagent command surface.',
    command: 'npm install -g doc-for-agent',
  },
  {
    id: '02',
    label: 'Init',
    title: 'Pick your CLI coding-agent entrypoint',
    body: 'Claude Code, Codex, CodeBuddy, Continue, and Copilot users all start from the same init model instead of separate documentation rituals.',
    command: 'docagent init --ai codex --target <repo-root>',
  },
  {
    id: '03',
    label: 'Refresh',
    title: 'Keep docs current as the repository changes',
    body: 'Refresh generates agent-facing and human-facing outputs as a system, not as an isolated one-off export.',
    command: 'docagent refresh --root <repo-root> --output-mode dual',
  },
];

const platforms = [
  { name: 'Claude Code', flag: 'claude' },
  { name: 'Codex', flag: 'codex' },
  { name: 'CodeBuddy', flag: 'codex' },
  { name: 'Continue', flag: 'continue' },
  { name: 'GitHub Copilot', flag: 'copilot' },
];

const differentiators = [
  {
    title: 'Built for low-doc and messy-doc repos',
    text: 'The first version of the page frames doc-for-agent as useful when a repo has almost no docs, scattered docs, or legacy agent notes that need structure.',
  },
  {
    title: 'Two outputs, one product model',
    text: 'The page keeps docs/ and AGENTS/ side by side to show that the product serves maintainers and agents together.',
  },
  {
    title: 'Lifecycle instead of one-shot generation',
    text: 'init, doctor, refresh, and migrate are presented as a repeatable operating model. That is the product, not just a markdown dump.',
  },
];

const lifecycle = [
  {
    name: 'docs/',
    points: ['Project narrative', 'System orientation', 'Human onboarding'],
  },
  {
    name: 'AGENTS/',
    points: ['Execution guardrails', 'Repo source-of-truth', 'Agent handoff'],
  },
];

const operations = ['init', 'doctor', 'refresh', 'migrate'];

function App() {
  return (
    <div className="page-shell">
      <div className="page-backdrop" aria-hidden="true" />
      <header className="topbar">
        <a className="brand" href="#hero">
          <LogoMark />
          <span>
            <strong>doc-for-agent</strong>
            <small>Landing v1</small>
          </span>
        </a>
        <nav className="nav-links" aria-label="Primary">
          <a href="#flow">Flow</a>
          <a href="#difference">Difference</a>
          <a href="#platforms">Platforms</a>
          <a className="nav-cta" href="#cta">Open the path</a>
        </nav>
      </header>

      <main>
        <section className="hero section" id="hero">
          <div className="hero-copy">
            <p className="eyebrow">For CLI coding-agent users</p>
            <h1>Turn repository knowledge into a maintained documentation system.</h1>
            <p className="hero-text">
              doc-for-agent is for Claude Code, Codex, CodeBuddy, Continue, and Copilot users who need a real project documentation system, not a one-off markdown generator.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#flow">See install to refresh</a>
              <a className="button button-secondary" href="#difference">Why it is different</a>
            </div>
            <ul className="platform-strip" aria-label="Supported platforms">
              {platforms.map((platform) => (
                <li key={platform.name}>{platform.name}</li>
              ))}
            </ul>
          </div>

          <aside className="hero-panel" aria-label="Core workflow preview">
            <div className="panel card command-card">
              <p className="panel-label">Shortest path</p>
              <code>install -&gt; init -&gt; refresh</code>
              <p>
                A short product path for terminal-first teams that want repo docs to stay usable across sessions.
              </p>
            </div>
            <div className="panel-grid">
              <div className="panel card">
                <p className="panel-label">Outputs</p>
                <strong>docs/ + AGENTS/</strong>
                <p>Human-facing guidance and agent-facing operating context.</p>
              </div>
              <div className="panel card">
                <p className="panel-label">Ops model</p>
                <strong>{operations.join(' / ')}</strong>
                <p>Lifecycle commands for ongoing documentation maintenance.</p>
              </div>
            </div>
          </aside>
        </section>

        <section className="section narrative-band">
          <div className="band-card">
            <p className="eyebrow">Product framing</p>
            <h2>Not another prompt wrapper for “scan repo and write docs”.</h2>
            <p>
              The page positions doc-for-agent as a system tool for repo knowledge. It absorbs sparse docs, restructures messy docs, and keeps both human and agent outputs refreshable.
            </p>
          </div>
        </section>

        <section className="section" id="flow">
          <div className="section-heading">
            <p className="eyebrow">Install to refresh</p>
            <h2>One page, one path, three visible steps.</h2>
            <p>
              The first conversion job of the landing page is clarity. Visitors should understand the path before they scroll past the fold.
            </p>
          </div>
          <div className="steps-grid">
            {steps.map((step) => (
              <article className="step-card card" key={step.id}>
                <div className="step-head">
                  <span>{step.id}</span>
                  <p>{step.label}</p>
                </div>
                <h3>{step.title}</h3>
                <p>{step.body}</p>
                <code>{step.command}</code>
              </article>
            ))}
          </div>
        </section>

        <section className="section" id="difference">
          <div className="section-heading split-heading">
            <div>
              <p className="eyebrow">Why this exists</p>
              <h2>Product difference anchored in lifecycle, not in prose style.</h2>
            </div>
            <p>
              The page avoids vague AI claims. It explains the durable product surface: dual outputs, repo-state fit, and repeatable maintenance commands.
            </p>
          </div>
          <div className="difference-grid">
            {differentiators.map((item) => (
              <article className="card difference-card" key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </section>

        <section className="section system-layout">
          <div className="section-heading">
            <p className="eyebrow">System outputs</p>
            <h2>docs/ and AGENTS/ are presented as one documentation operating model.</h2>
          </div>
          <div className="system-grid">
            {lifecycle.map((column) => (
              <article className="card system-card" key={column.name}>
                <h3>{column.name}</h3>
                <ul>
                  {column.points.map((point) => (
                    <li key={point}>{point}</li>
                  ))}
                </ul>
              </article>
            ))}
            <article className="card system-card system-card-accent">
              <p className="panel-label">Repository fit</p>
              <h3>Useful when the repo is under-documented or structurally messy.</h3>
              <p>
                The message is explicit: this is for low-doc repos, messy-doc repos, and teams that need refreshable agent context instead of brittle one-time output.
              </p>
            </article>
          </div>
        </section>

        <section className="section" id="platforms">
          <div className="section-heading split-heading">
            <div>
              <p className="eyebrow">Platform entrypoints</p>
              <h2>One product surface for multiple CLI coding-agent workflows.</h2>
            </div>
            <p>
              The landing page makes platform support obvious without letting the page collapse into a logo wall.
            </p>
          </div>
          <div className="platform-grid">
            {platforms.map((platform) => (
              <article className="card platform-card" key={platform.name}>
                <p>{platform.name}</p>
                <code>docagent init --ai {platform.flag}</code>
              </article>
            ))}
          </div>
        </section>

        <section className="section cta-section" id="cta">
          <div className="cta-card">
            <p className="eyebrow">Landing direction v1</p>
            <h2>A React homepage skeleton that can grow into the public product surface.</h2>
            <p>
              This version focuses on hierarchy, narrative, and conversion flow. It gives the repo a product-home foundation before adding screenshots, demos, or deeper proof.
            </p>
            <div className="hero-actions">
              <a className="button button-primary" href="#flow">Review the flow</a>
              <a className="button button-secondary" href="#platforms">Check platform entrypoints</a>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
