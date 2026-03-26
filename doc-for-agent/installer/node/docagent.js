#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function resolveCliScript() {
  const candidate = path.resolve(__dirname, "..", "assets", "installer", "docagent.py");
  return fs.existsSync(candidate) ? candidate : null;
}

function runPython(cliScript, args) {
  const pythonCandidates = [];
  if (process.env.DOCAGENT_PYTHON) {
    pythonCandidates.push([process.env.DOCAGENT_PYTHON, []]);
  }
  pythonCandidates.push(["python3", []], ["python", []], ["py", ["-3"]]);

  for (const [executable, preArgs] of pythonCandidates) {
    const run = spawnSync(executable, [...preArgs, cliScript, ...args], { stdio: "inherit" });
    if (run.error && run.error.code === "ENOENT") {
      continue;
    }
    if (run.error) {
      console.error(`[docagent] Failed to start ${executable}: ${run.error.message}`);
      return 2;
    }
    return run.status == null ? 1 : run.status;
  }

  console.error("[docagent] Python runtime was not found.");
  console.error("[docagent] Install Python 3, then run one of:");
  console.error("  - pipx install doc-for-agent");
  console.error("  - python3 -m pip install doc-for-agent");
  return 2;
}

function main() {
  const cliScript = resolveCliScript();
  if (!cliScript) {
    console.error("[docagent] Packaged runtime assets are missing.");
    console.error("[docagent] Expected script: doc-for-agent/installer/assets/installer/docagent.py");
    return 2;
  }
  return runPython(cliScript, process.argv.slice(2));
}

process.exit(main());
