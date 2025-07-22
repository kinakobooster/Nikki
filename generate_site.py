#!/usr/bin/env python3
import os
import re
from pathlib import Path

def simple_markdown_to_html(text):
    """Simple markdown to HTML converter without external dependencies"""
    html = text
    
    # Convert headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    
    # Convert bold
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__(.+?)__', r'<strong>\1</strong>', html)
    
    # Convert italic
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    html = re.sub(r'_(.+?)_', r'<em>\1</em>', html)
    
    # Convert code blocks
    html = re.sub(r'```[\w]*\n(.*?)\n```', r'<pre><code>\1</code></pre>', html, flags=re.DOTALL)
    
    # Convert inline code
    html = re.sub(r'`(.+?)`', r'<code>\1</code>', html)
    
    # Convert blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Convert lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^[0-9]+\. (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Wrap consecutive list items in ul tags
    html = re.sub(r'(<li>.*?</li>\n?)+', lambda m: '<ul>\n' + m.group(0) + '</ul>\n', html, flags=re.DOTALL)
    
    # Convert paragraphs - handle single line breaks properly for Japanese text
    paragraphs = []
    current_para = []
    in_pre = False
    in_list = False
    
    for line in html.split('\n'):
        if '<pre>' in line:
            in_pre = True
        if '</pre>' in line:
            in_pre = False
        if '<ul>' in line:
            in_list = True
        if '</ul>' in line:
            in_list = False
            
        if line.strip() == '' and not in_pre and not in_list:
            if current_para:
                # Join lines without spaces for Japanese text
                paragraphs.append('<p>' + ''.join(current_para) + '</p>')
                current_para = []
        elif not line.startswith('<') or in_pre:
            if not in_pre and not in_list:
                current_para.append(line.strip())
            else:
                paragraphs.append(line)
        else:
            if current_para:
                # Join lines without spaces for Japanese text
                paragraphs.append('<p>' + ''.join(current_para) + '</p>')
                current_para = []
            paragraphs.append(line)
    
    if current_para:
        # Join lines without spaces for Japanese text
        paragraphs.append('<p>' + ''.join(current_para) + '</p>')
    
    return '\n'.join(paragraphs)

def generate_site(docs_dir='docs', output_file='index.html'):
    docs_path = Path(docs_dir)
    
    if not docs_path.exists():
        print(f"Error: {docs_dir} directory not found")
        return
    
    md_files = sorted([f for f in docs_path.glob('*.md')])
    
    if not md_files:
        print(f"No markdown files found in {docs_dir}")
        return
    
    html_content = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nikki</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            font-family: 'Hiragino Mincho ProN', 'Yu Mincho', serif;
            overflow-y: hidden;
        }
        
        .container {
            height: 80vh;
            margin-top: 10vh;
            overflow-x: scroll;
            overflow-y: hidden;
            display: flex;
            flex-direction: row;
            flex-wrap: nowrap;
            padding: 0 20px;
            box-sizing: border-box;
            align-items: center;
        }
        
        .content {
            height: 100%;
            margin-right: 60px;
            flex-shrink: 0;
            width: auto;
            writing-mode: vertical-rl;
            text-orientation: mixed;
        }
        
        
        .content:last-child {
            margin-right: 0;
        }
        
        h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
            font-family: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
            font-weight: 700;
            letter-spacing: 0.1em;
        }
        
        h3 {
            font-size: 1.4em;
            margin-bottom: 15px;
            color: #444;
            font-family: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
            font-weight: 700;
        }
        
        p {
            line-height: 2;
            font-size: 1.1em;
            color: #444;
            margin-bottom: 1.5em;
            text-align: justify;
        }
        
        ul, ol {
            margin-bottom: 1.5em;
            padding-right: 1.5em;
        }
        
        li {
            margin-bottom: 0.5em;
            line-height: 2;
        }
        
        code {
            background-color: #e8e8e8;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        
        pre {
            background-color: #e8e8e8;
            padding: 1em;
            border-radius: 5px;
            overflow-x: auto;
            margin-bottom: 1.5em;
        }
        
        pre code {
            background-color: transparent;
            padding: 0;
        }
        
        blockquote {
            border-right: 4px solid #ddd;
            padding-right: 1em;
            margin: 0 0 1.5em 0;
            color: #666;
        }
        
        ::-webkit-scrollbar {
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 6px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        
        .progress-dots {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 10px;
            z-index: 100;
        }
        
        .dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background-color: #ccc;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        
        .dot.active {
            background-color: #333;
        }
        
        .dot:hover {
            background-color: #666;
        }
        
        /* アクセスカウンター */
        .access-counter {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.95);
            padding: 10px 20px;
            border-radius: 25px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            font-size: 14px;
            z-index: 1000;
            writing-mode: horizontal-tb;
            font-family: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
        }
        
        .counter-label {
            color: #666;
            margin-right: 5px;
        }
        
        #access-count {
            font-weight: bold;
            color: #3498db;
            font-size: 16px;
        }
        
        .kiriban {
            margin-left: 10px;
            color: #e74c3c;
            font-weight: bold;
            display: none;
            animation: bounce 0.5s ease;
        }
        
        /* いいねボタン */
        .like-section {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 100;
            opacity: 0;
            transition: opacity 0.3s ease;
            pointer-events: none;
            background: white;
            border: 2px solid #667eea;
            border-radius: 30px;
            padding: 15px 30px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            writing-mode: horizontal-tb;
        }
        
        .like-section.visible {
            opacity: 1;
            pointer-events: auto;
        }
        
        .like-button {
            background: none;
            border: none;
            color: #667eea;
            font-size: 16px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
            text-decoration: none;
            padding: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .like-button:hover:not(:disabled) {
            color: #764ba2;
            transform: scale(1.05);
        }
        
        .like-button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .like-message {
            margin-left: 15px;
            font-size: 14px;
            font-family: 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }
        
        .thank-you {
            color: #27ae60;
            animation: fadeIn 0.5s ease;
        }
        
        .like-count {
            color: #667eea;
            font-weight: bold;
        }
        
        .zorome {
            color: #e74c3c;
            font-weight: bold;
            animation: pulse 1s ease infinite;
        }
        
        @keyframes bounce {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.2); }
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.1); }
        }
    </style>
    <script>
        window.addEventListener('load', function() {
            const container = document.querySelector('.container');
            const dots = document.querySelectorAll('.dot');
            const contents = document.querySelectorAll('.content');
            
            if (container) {
                // Scroll to the rightmost position
                container.scrollTo({
                    left: container.scrollWidth,
                    behavior: 'smooth'
                });
            }
            
            // Function to update active dot based on scroll position
            function updateActiveDot() {
                const scrollLeft = container.scrollLeft;
                const containerWidth = container.clientWidth;
                const scrollWidth = container.scrollWidth;
                
                // Calculate which article is currently most visible
                let currentArticleIndex = 0;
                let accumulatedWidth = 0;
                
                // Find which article the current scroll position corresponds to
                for (let i = 0; i < contents.length; i++) {
                    const articleWidth = contents[i].offsetWidth + 60; // include margin
                    const articleStartPos = scrollWidth - containerWidth - accumulatedWidth - articleWidth;
                    const articleEndPos = scrollWidth - containerWidth - accumulatedWidth;
                    
                    if (scrollLeft >= articleStartPos && scrollLeft <= articleEndPos) {
                        currentArticleIndex = i;
                        break;
                    }
                    
                    accumulatedWidth += articleWidth;
                }
                
                // Update dot active state
                dots.forEach((dot) => {
                    const dotIndex = parseInt(dot.getAttribute('data-index'));
                    const targetArticleIndex = dotIndex === 0 ? 0 : dotIndex - 1;
                    
                    if (targetArticleIndex === currentArticleIndex) {
                        dot.classList.add('active');
                    } else {
                        dot.classList.remove('active');
                    }
                });
            }
            
            // Function to check if scrolled to the end (left side)
            function checkLikeButtonVisibility() {
                const likeSection = document.querySelector('.like-section');
                if (container && likeSection) {
                    // Check if we're at the leftmost position (scrollLeft = 0)
                    if (container.scrollLeft <= 50) {
                        likeSection.classList.add('visible');
                    } else {
                        likeSection.classList.remove('visible');
                    }
                }
            }
            
            // Add scroll event listener
            if (container) {
                container.addEventListener('scroll', () => {
                    updateActiveDot();
                    checkLikeButtonVisibility();
                });
                // Initial call after page load
                setTimeout(() => {
                    updateActiveDot();
                    checkLikeButtonVisibility();
                }, 100);
            }
            
            // Add click handlers to dots
            dots.forEach((dot) => {
                dot.addEventListener('click', () => {
                    const dotIndex = parseInt(dot.getAttribute('data-index'));
                    
                    // Articles are in DOM from right to left (reversed order)
                    // Dots are now: rightmost dot = data-index 0, leftmost dot = data-index 2
                    // We want each dot to jump to its corresponding article's right edge (beginning)
                    
                    let targetScroll = 0;
                    
                    // Jump to article at index (dotIndex - 1) to correct the offset
                    const targetArticleIndex = dotIndex === 0 ? 0 : dotIndex - 1;
                    
                    if (targetArticleIndex === 0) {
                        // Jump to article 0's right edge (container's right edge)
                        targetScroll = container.scrollWidth - container.clientWidth;
                    } else {
                        // Calculate position to show right edge of target article
                        // Sum widths of articles from right (index 0) up to but not including target
                        for (let i = 0; i < targetArticleIndex; i++) {
                            targetScroll += contents[i].offsetWidth + 60; // 60px margin
                        }
                        // Position to show right edge of target article
                        targetScroll = container.scrollWidth - container.clientWidth - targetScroll;
                    }
                    
                    container.scrollTo({
                        left: targetScroll,
                        behavior: 'smooth'
                    });
                });
            });
            
            // CounterAPI V2設定（公開カウンター）
            const WORKSPACE = 'nikkisite2025';
            const ACCESS_COUNTER = 'totalvisits';
            const LIKE_COUNTER = 'totallikes';
            
            // ゾロ目チェック
            function isZorome(num) {
                if (num < 11) return false;
                const str = num.toString();
                return str.split('').every(digit => digit === str[0]);
            }
            
            // アクセスカウンター（V2 API: カウントアップして値を取得）
            async function updateAccessCounter() {
                try {
                    // V2エンドポイント（公開カウンター、認証不要）
                    const url = `https://api.counterapi.dev/v2/${WORKSPACE}/${ACCESS_COUNTER}/up`;
                    const response = await fetch(url);
                    
                    if (response.ok) {
                        const data = await response.json();
                        const count = data.data.up_count;
                        document.getElementById('access-count').textContent = count.toLocaleString();
                        
                        if (isZorome(count)) {
                            const kiribanEl = document.getElementById('access-kiriban');
                            kiribanEl.textContent = 'キリ番！';
                            kiribanEl.style.display = 'inline';
                            setTimeout(() => { kiribanEl.style.display = 'none'; }, 5000);
                        }
                    } else {
                        console.error('アクセスカウンターエラー:', response.status, await response.text());
                        document.getElementById('access-count').textContent = '-';
                    }
                } catch (error) {
                    console.error('アクセスカウンターエラー:', error);
                    document.getElementById('access-count').textContent = '-';
                }
            }
            
            // 現在のアクセス数表示（V2 API: カウントアップせずに値を取得）
            async function showCurrentAccessCount() {
                try {
                    const url = `https://api.counterapi.dev/v2/${WORKSPACE}/${ACCESS_COUNTER}`;
                    const response = await fetch(url);
                    
                    if (response.ok) {
                        const data = await response.json();
                        const count = data.data.up_count;
                        document.getElementById('access-count').textContent = count.toLocaleString();
                    }
                } catch (error) {
                    console.error('アクセス数取得エラー:', error);
                }
            }
            
            // いいねボタン処理（V2 API）
            async function handleLikeButton() {
                const button = document.getElementById('like-button');
                const messageDiv = document.getElementById('like-message');
                button.disabled = true;
                
                try {
                    const url = `https://api.counterapi.dev/v2/${WORKSPACE}/${LIKE_COUNTER}/up`;
                    const response = await fetch(url);
                    
                    if (response.ok) {
                        const data = await response.json();
                        const count = data.data.up_count;
                        
                        messageDiv.innerHTML = `
                            <span class="thank-you">ありがとう！</span>
                            <span class="like-count">${count.toLocaleString()}</span>
                            ${isZorome(count) ? '<span class="zorome">ゾロ目だ！</span>' : ''}
                        `;
                        
                        if (isZorome(count)) {
                            createConfetti();
                        }
                        
                        setTimeout(() => { 
                            button.disabled = false;
                            messageDiv.innerHTML = `<span class="like-count">${count.toLocaleString()}</span>`;
                        }, 3000);
                    } else {
                        console.error('いいねエラー:', response.status, await response.text());
                        messageDiv.innerHTML = '<span style="color: red;">エラー</span>';
                        button.disabled = false;
                    }
                } catch (error) {
                    console.error('いいねエラー:', error);
                    messageDiv.innerHTML = '<span style="color: red;">エラー</span>';
                    button.disabled = false;
                }
            }
            
            // 紙吹雪エフェクト
            function createConfetti() {
                const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#e056fd'];
                for (let i = 0; i < 50; i++) {
                    const confetti = document.createElement('div');
                    confetti.style.cssText = `
                        position: fixed;
                        width: 10px;
                        height: 10px;
                        background: ${colors[Math.floor(Math.random() * colors.length)]};
                        left: ${Math.random() * 100}%;
                        top: -10px;
                        opacity: ${Math.random() * 0.5 + 0.5};
                        pointer-events: none;
                        z-index: 9999;
                    `;
                    document.body.appendChild(confetti);
                    
                    confetti.animate([
                        { transform: 'translateY(0) rotate(0deg)', opacity: 1 },
                        { transform: `translateY(${window.innerHeight + 10}px) rotate(${Math.random() * 720}deg)`, opacity: 0 }
                    ], {
                        duration: (Math.random() * 3 + 2) * 1000,
                        easing: 'ease-out'
                    }).onfinish = () => confetti.remove();
                }
            }
            
            // 現在のいいね数表示（V2 API）
            async function showCurrentLikeCount() {
                try {
                    const url = `https://api.counterapi.dev/v2/${WORKSPACE}/${LIKE_COUNTER}`;
                    const response = await fetch(url);
                    
                    if (response.ok) {
                        const data = await response.json();
                        const count = data.data.up_count;
                        document.getElementById('like-message').innerHTML = 
                            `<span class="like-count">${count.toLocaleString()}</span>`;
                    }
                } catch (error) {
                    console.error('いいね数取得エラー:', error);
                    document.getElementById('like-message').innerHTML = '';
                }
            }
            
            // カウンター初期化
            if (!sessionStorage.getItem('counted')) {
                updateAccessCounter();
                sessionStorage.setItem('counted', 'true');
            } else {
                showCurrentAccessCount();
            }
            
            showCurrentLikeCount();
            
            // いいねボタンイベント
            document.getElementById('like-button').addEventListener('click', handleLikeButton);
        });
    </script>
</head>
<body>
    <!-- アクセスカウンター（右上） -->
    <div id="access-counter" class="access-counter">
        <span class="counter-label">訪問者数:</span>
        <span id="access-count">-</span>
        <span id="access-kiriban" class="kiriban"></span>
    </div>
    
    <div class="container">
'''
    
    # Reverse the order so 001 is rightmost
    for md_file in reversed(md_files):
        file_content = md_file.read_text(encoding='utf-8')
        html_body = simple_markdown_to_html(file_content)
        
        html_content += f'''        <div class="content">
            <h2>{md_file.stem}</h2>
            {html_body}
        </div>
'''
    
    html_content += '''    </div>
    
    <!-- いいねボタン（下中央固定） -->
    <div class="like-section">
        <div style="display: flex; align-items: center;">
            <button id="like-button" class="like-button" type="button">
                <span class="like-icon">✨</span>
                <span class="like-text">いいね！</span>
            </button>
            <div id="like-message" class="like-message"></div>
        </div>
    </div>
    
    <div class="progress-dots">
'''
    
    # Add dots for each article (reverse order so rightmost dot is index 0)
    for i in range(len(md_files) - 1, -1, -1):
        html_content += f'        <div class="dot" data-index="{i}"></div>\n'
    
    html_content += '''    </div>
</body>
</html>'''
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Static site generated: {output_file}")
    print(f"Processed {len(md_files)} markdown files")

if __name__ == "__main__":
    generate_site()