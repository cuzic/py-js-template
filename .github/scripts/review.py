#!/usr/bin/env python3
"""
AI Code Review Script using Google Gemini API

This script performs automated code review on pull request diffs using 
Google's Gemini AI model. It analyzes the code changes and provides 
detailed feedback on code quality, potential issues, and improvements.

Requirements:
    - GEMINI_API_KEY environment variable
    - requests library (pip install requests)

Usage:
    python review.py <pr_diff_file> [options]
    
Environment Variables:
    GEMINI_API_KEY: Google Gemini API key (required)
    GITHUB_TOKEN: GitHub token for API access (optional)
    PR_NUMBER: Pull request number (optional)
    REPO_NAME: Repository name (optional)
"""

import os
import sys
import json
import argparse
from typing import Optional, Dict, Any
import logging

try:
    import requests
except ImportError:
    print("Error: requests library is required. Install with: pip install requests")
    sys.exit(1)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GeminiReviewer:
    """AI Code Reviewer using Google Gemini API"""
    
    def __init__(self, api_key: str):
        """Initialize the reviewer with API key"""
        self.api_key = api_key
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
        
    def create_review_prompt(self, diff_content: str) -> str:
        """Create a comprehensive review prompt for the AI"""
        return f"""
# 🤖 AI Code Review

あなたは経験豊富なシニアソフトウェア開発者として、以下のPull Requestの差分をレビューしてください。

## レビューガイドライン

### 🔍 **重点チェック項目**
1. **セキュリティ**: 脆弱性、機密情報の露出、入力検証
2. **パフォーマンス**: アルゴリズムの効率性、メモリ使用量、データベースクエリ
3. **品質**: コードの可読性、保守性、テスト可能性
4. **ベストプラクティス**: 言語固有の慣例、設計パターン
5. **バグ**: 論理エラー、エッジケース、型安全性

### 📝 **レビュー形式**
- **重要度**: 🔴 Critical / 🟡 Warning / ℹ️ Suggestion
- **具体的なコード指摘**: ファイル名:行番号を明記
- **改善提案**: 具体的なコード例を提示
- **理由説明**: なぜその変更が必要かを明確に説明

### ✅ **良い点も評価**
- 優れた実装や改善点も積極的に評価してください
- チームのモチベーション向上に寄与する建設的なフィードバック

---

## Pull Request Diff

```diff
{diff_content}
```

---

## レビュー結果

以下の形式でレビューを行ってください：

### 📊 **総合評価**
- 全体的な品質スコア (1-10)
- 主な改善点の要約

### 🔍 **詳細レビュー**
#### セキュリティ 🔒
- [指摘事項があれば記載]

#### パフォーマンス ⚡
- [指摘事項があれば記載]

#### コード品質 ✨
- [指摘事項があれば記載]

#### ベストプラクティス 📋
- [指摘事項があれば記載]

### 👍 **Good Points**
- [優れている点を記載]

### 🚀 **Next Actions**
- [推奨される次のアクション]

---

レビューは建設的で実行可能なものにし、チーム全体のスキル向上に寄与するよう心がけてください。
"""

    def review_code(self, diff_content: str) -> Optional[str]:
        """
        Send code diff to Gemini API for review
        
        Args:
            diff_content: The git diff content to review
            
        Returns:
            AI review response or None if error occurred
        """
        if not diff_content.strip():
            logger.warning("Empty diff content provided")
            return "📝 **No code changes detected**\n\nThis pull request doesn't contain any code changes to review."
        
        prompt = self.create_review_prompt(diff_content)
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,  # Lower temperature for more consistent reviews
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 8192,
            },
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
        }
        
        try:
            url = f"{self.base_url}?key={self.api_key}"
            logger.info(f"Sending request to Gemini API (content length: {len(diff_content)} chars)")
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            
            if 'candidates' in data and len(data['candidates']) > 0:
                if 'content' in data['candidates'][0]:
                    review_text = data['candidates'][0]['content']['parts'][0]['text']
                    logger.info("Successfully received AI review")
                    return review_text
                else:
                    logger.error("No content in AI response")
                    return None
            else:
                logger.error("No candidates in AI response")
                return None
                
        except requests.exceptions.Timeout:
            logger.error("Request to Gemini API timed out")
            return "⏰ **Review Timeout**\n\nThe AI review service is currently experiencing delays. Please try again later."
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return f"❌ **Review Service Error**\n\nThere was an error connecting to the AI review service: {str(e)}"
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return "❌ **Response Parse Error**\n\nFailed to parse the AI review response."
            
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return f"❌ **Unexpected Error**\n\nAn unexpected error occurred: {str(e)}"

def post_github_comment(review_text: str, pr_number: str, repo_name: str, github_token: str) -> bool:
    """
    Post the review as a comment on the GitHub pull request
    
    Args:
        review_text: The AI review text
        pr_number: Pull request number
        repo_name: Repository name (format: owner/repo)
        github_token: GitHub API token
        
    Returns:
        True if comment was posted successfully, False otherwise
    """
    try:
        url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json'
        }
        
        # Add header and footer to the review
        formatted_review = f"""# 🤖 AI Code Review

{review_text}

---
*🤖 This review was generated automatically by AI. Please use it as a reference and apply human judgment for final decisions.*

*Generated with [Google Gemini](https://ai.google.dev/) • [Claude Code](https://claude.ai/code)*
"""
        
        payload = {
            'body': formatted_review
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        logger.info(f"Successfully posted comment to PR #{pr_number}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to post GitHub comment: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error posting comment: {e}")
        return False

def main():
    """Main function to orchestrate the AI review process"""
    parser = argparse.ArgumentParser(description='AI Code Review using Google Gemini')
    parser.add_argument('diff_file', help='Path to the PR diff file')
    parser.add_argument('--pr-number', help='Pull request number')
    parser.add_argument('--repo-name', help='Repository name (owner/repo)')
    parser.add_argument('--post-comment', action='store_true', 
                       help='Post review as GitHub comment')
    parser.add_argument('--output', help='Output file for review (default: stdout)')
    
    args = parser.parse_args()
    
    # Get API key from environment
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is required")
        print("❌ **Configuration Error**: GEMINI_API_KEY environment variable is required")
        sys.exit(1)
    
    # Read diff file
    try:
        with open(args.diff_file, 'r', encoding='utf-8') as f:
            diff_content = f.read()
    except FileNotFoundError:
        logger.error(f"Diff file not found: {args.diff_file}")
        print(f"❌ **File Error**: Diff file not found: {args.diff_file}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error reading diff file: {e}")
        print(f"❌ **File Error**: Failed to read diff file: {e}")
        sys.exit(1)
    
    # Perform AI review
    reviewer = GeminiReviewer(api_key)
    review_text = reviewer.review_code(diff_content)
    
    if review_text is None:
        logger.error("Failed to get AI review")
        print("❌ **Review Failed**: Could not generate AI review")
        sys.exit(1)
    
    # Output review
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(review_text)
            logger.info(f"Review saved to {args.output}")
        except Exception as e:
            logger.error(f"Error writing output file: {e}")
            print(f"❌ **Output Error**: Failed to write output file: {e}")
            sys.exit(1)
    else:
        print(review_text)
    
    # Post as GitHub comment if requested
    if args.post_comment:
        github_token = os.getenv('GITHUB_TOKEN')
        pr_number = args.pr_number or os.getenv('PR_NUMBER')
        repo_name = args.repo_name or os.getenv('REPO_NAME')
        
        if not all([github_token, pr_number, repo_name]):
            logger.warning("Missing GitHub configuration for comment posting")
            print("⚠️ **Warning**: Missing GitHub configuration (GITHUB_TOKEN, PR_NUMBER, REPO_NAME)")
        else:
            success = post_github_comment(review_text, pr_number, repo_name, github_token)
            if not success:
                sys.exit(1)
    
    logger.info("AI review completed successfully")

if __name__ == '__main__':
    main()