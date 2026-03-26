#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function resolveCliScript() {
  const candidates = [
    path.resolve(__dirname, "..", "assets", "installer", "docagent.py"),
    path.resolve(__dirname, "..", "docagent.py")
  ];
  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  return null;
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

function printQuickStart() {
  console.error("[docagent] Quick start (Node entry):");
  console.error("  npx -y doc-for-agent doctor --target /path/to/repo");
  console.error("  npx -y doc-for-agent all --target /path/to/repo");
  console.error("  npx -y doc-for-agent --help");
  console.error("[docagent] All entry paths converge on the same `docagent` product CLI.");
}

function main() {
  const cliScript = resolveCliScript();
  if (!cliScript) {
    console.error("[docagent] Packaged runtime assets are missing.");
    console.error("[docagent] Expected one of:");
    console.error("  - doc-for-agent/installer/assets/installer/docagent.py");
    console.error("  - doc-for-agent/installer/docagent.py");
    return 2;
  }
  const forwardedArgs = process.argv.slice(2);
  if (forwardedArgs.length === 0) {
    printQuickStart();
    forwardedArgs.push("--help");
  } else if (forwardedArgs[0] === "help") {
    forwardedArgs[0] = "--help";
  }
  return runPython(cliScript, forwardedArgs);
}

process.exit(main());
