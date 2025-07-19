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
    
    # Convert paragraphs
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
                paragraphs.append('<p>' + ' '.join(current_para) + '</p>')
                current_para = []
        elif not line.startswith('<') or in_pre:
            if not in_pre and not in_list:
                current_para.append(line)
            else:
                paragraphs.append(line)
        else:
            if current_para:
                paragraphs.append('<p>' + ' '.join(current_para) + '</p>')
                current_para = []
            paragraphs.append(line)
    
    if current_para:
        paragraphs.append('<p>' + ' '.join(current_para) + '</p>')
    
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
            text-orientation: upright;
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
        
        .content:last-child {
            margin-right: 0;
        }
        
        h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
            color: #333;
            font-weight: bold;
            letter-spacing: 0.1em;
        }
        
        h3 {
            font-size: 1.4em;
            margin-bottom: 15px;
            color: #444;
            font-weight: bold;
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
            
            // Update active dot based on scroll position
            function updateActiveDot() {
                const scrollLeft = container.scrollLeft;
                const containerWidth = container.clientWidth;
                const scrollWidth = container.scrollWidth;
                
                // Calculate which article is currently visible (reversed order)
                const scrollProgress = 1 - (scrollLeft / (scrollWidth - containerWidth));
                const activeIndex = Math.round(scrollProgress * (contents.length - 1));
                
                dots.forEach((dot, index) => {
                    if (index === activeIndex) {
                        dot.classList.add('active');
                    } else {
                        dot.classList.remove('active');
                    }
                });
            }
            
            // Add scroll event listener
            if (container) {
                container.addEventListener('scroll', updateActiveDot);
                updateActiveDot(); // Initial call
            }
            
            // Add click handlers to dots
            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => {
                    // Calculate scroll position for this article (reversed order)
                    const articleWidth = contents[0].offsetWidth + 60; // width + margin
                    const targetScroll = scrollWidth - containerWidth - (index * articleWidth);
                    
                    container.scrollTo({
                        left: targetScroll,
                        behavior: 'smooth'
                    });
                });
            });
        });
    </script>
</head>
<body>
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
    <div class="progress-dots">
'''
    
    # Add dots for each article (in original order)
    for i in range(len(md_files)):
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