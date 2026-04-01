"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

function isGlobal(args) {
  return args.includes("--global");
}

function getGlobalRoot(args) {
  const customIndex = args.indexOf("--global-root");
  if (customIndex !== -1 && customIndex + 1 < args.length) {
    return path.resolve(args[customIndex + 1]);
  }
  return process.env.DOCAGENT_GLOBAL_ROOT ? path.resolve(process.env.DOCAGENT_GLOBAL_ROOT) : os.homedir();
}

function getTargetDir(args) {
  let target = process.cwd();
  const targetIndex = args.indexOf("--target");
  if (targetIndex !== -1 && targetIndex + 1 < args.length) {
    target = path.resolve(args[targetIndex + 1]);
  }
  return target;
}

function getAiPlatform(args) {
  const aiIndex = args.indexOf("--ai");
  if (aiIndex !== -1 && aiIndex + 1 < args.length) {
    return args[aiIndex + 1].toLowerCase();
  }
  return "all";
}

function setupClaudeSkill(targetDir, isGlobalRun) {
  const claudeDir = path.join(targetDir, ".claude", "skills", "doc-for-agent");
  if (!fs.existsSync(claudeDir)) {
    fs.mkdirSync(claudeDir, { recursive: true });
  }

  const templateFile = path.join(__dirname, "templates", "CLAUDE.md");
  const destFile = path.join(claudeDir, "CLAUDE.md");

  if (fs.existsSync(templateFile)) {
    fs.copyFileSync(templateFile, destFile);
  }
}

function setupCursorRules(targetDir, isGlobalRun) {
  const ruleFileName = isGlobalRun ? ".cursorrules_global_placeholder" : ".cursorrules";
  if (isGlobalRun) {
    return;
  }
  
  const destFile = path.join(targetDir, ruleFileName);
  const templateFile = path.join(__dirname, "templates", "cursorrules");

  if (fs.existsSync(templateFile)) {
    let existingContent = "";
    if (fs.existsSync(destFile)) {
      existingContent = fs.readFileSync(destFile, "utf-8");
      if (existingContent.includes("doc-for-agent")) {
        return;
      }
      existingContent += "\n\n";
    }
    const injectedContent = fs.readFileSync(templateFile, "utf-8");
    fs.writeFileSync(destFile, existingContent + injectedContent);
  }
}

function runInit(args) {
  const globalMode = isGlobal(args);
  const platform = getAiPlatform(args);
  
  const globalTarget = getGlobalRoot(args);
  const localTarget = getTargetDir(args);

  const injectToTarget = (targetDir, isGlobalRun) => {
    if (platform === "claudecode" || platform === "claude" || platform === "all") {
      setupClaudeSkill(targetDir, isGlobalRun);
    }
    if (platform === "codex" || platform === "cursor" || platform === "continue" || platform === "copilot" || platform === "all") {
      setupCursorRules(targetDir, isGlobalRun);
    }
  };

  injectToTarget(globalTarget, true);
  
  if (!globalMode) {
    injectToTarget(localTarget, false);
  }
}

module.exports = { runInit };
