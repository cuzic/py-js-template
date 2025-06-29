#!/usr/bin/env node
/**
 * JavaScript品質分析スクリプト
 * quality-analysis.yml ワークフローから抽出
 */

const fs = require('fs');
const path = require('path');

function loadJsonSafe(filepath) {
  try {
    return JSON.parse(fs.readFileSync(filepath, 'utf8'));
  } catch {
    return {};
  }
}

function analyzeJavaScriptQuality() {
  const summary = {
    timestamp: new Date().toISOString().split('T')[0],
    eslint_errors: 0,
    eslint_warnings: 0,
    typescript_errors: 0,
    bundle_size_kb: 0,
    test_coverage: 0,
    dependency_vulnerabilities: 0
  };
  
  // ESLint統計
  const eslintData = loadJsonSafe('quality-reports/eslint-detailed.json');
  if (Array.isArray(eslintData)) {
    summary.eslint_errors = eslintData.reduce((sum, file) => sum + file.errorCount, 0);
    summary.eslint_warnings = eslintData.reduce((sum, file) => sum + file.warningCount, 0);
  }
  
  // TypeScript統計
  try {
    const tsOutput = fs.readFileSync('quality-reports/typescript-detailed.txt', 'utf8');
    const errorMatches = tsOutput.match(/error TS\d+:/g);
    summary.typescript_errors = errorMatches ? errorMatches.length : 0;
  } catch {}
  
  // バンドルサイズ
  try {
    const bundleSizes = fs.readFileSync('quality-reports/bundle-sizes.txt', 'utf8');
    const totalSize = bundleSizes.split('\n')
      .filter(line => line.includes('.js'))
      .reduce((sum, line) => {
        const match = line.match(/(\d+)K/);
        return sum + (match ? parseInt(match[1]) : 0);
      }, 0);
    summary.bundle_size_kb = totalSize;
  } catch {}
  
  // 依存関係脆弱性
  const auditData = loadJsonSafe('quality-reports/dependency-audit.json');
  if (auditData.advisories) {
    summary.dependency_vulnerabilities = Object.keys(auditData.advisories).length;
  }
  
  // サマリーファイル出力
  fs.writeFileSync('quality-reports/javascript-summary.json', JSON.stringify(summary, null, 2));
  console.log('JavaScript品質サマリー:', summary);
  
  return summary;
}

function main() {
  if (!fs.existsSync('quality-reports')) {
    console.error('Error: quality-reports ディレクトリが見つかりません');
    process.exit(1);
  }
  
  try {
    const summary = analyzeJavaScriptQuality();
    console.log('✅ JavaScript品質分析完了');
  } catch (error) {
    console.error(`❌ JavaScript品質分析エラー: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { analyzeJavaScriptQuality, loadJsonSafe };