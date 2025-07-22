// APIキーとエンドポイント
const ACCESS_API_KEY = 'ut_mne2sniPiULSMSTCuuMfYnBObykW7BGgIs813L1I';
const LIKE_API_KEY = 'ut_nrNhrSDG76KN3nmWb6I4eFmO8fFhi2YiVW81xQqG';
const API_BASE_URL = 'https://api.counterapi.dev/v1';

// ゾロ目をチェックする関数
function isZorome(num) {
    if (num < 11) return false;
    const str = num.toString();
    return str.split('').every(digit => digit === str[0]);
}

// アクセスカウンターの処理
async function updateAccessCounter() {
    try {
        // アクセス数を増やしてカウントを取得
        const response = await fetch(`${API_BASE_URL}/hit?key=${ACCESS_API_KEY}`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error('アクセスカウンターの更新に失敗しました');
        }
        
        const data = await response.json();
        const count = data.count;
        
        // カウント表示を更新
        document.getElementById('access-count').textContent = count.toLocaleString();
        
        // ゾロ目チェック
        const kiribanElement = document.getElementById('access-kiriban');
        if (isZorome(count)) {
            kiribanElement.textContent = 'キリ番！';
            kiribanElement.style.display = 'inline';
            
            // 5秒後に非表示
            setTimeout(() => {
                kiribanElement.style.display = 'none';
            }, 5000);
        }
    } catch (error) {
        console.error('アクセスカウンターエラー:', error);
        document.getElementById('access-count').textContent = 'エラー';
    }
}

// 現在のアクセス数を表示（増やさない）
async function showCurrentAccessCount() {
    try {
        const response = await fetch(`${API_BASE_URL}/get?key=${ACCESS_API_KEY}`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error('アクセス数の取得に失敗しました');
        }
        
        const data = await response.json();
        const count = data.count;
        
        document.getElementById('access-count').textContent = count.toLocaleString();
    } catch (error) {
        console.error('アクセス数取得エラー:', error);
    }
}

// いいねボタンの処理
async function handleLikeButton() {
    const button = document.getElementById('like-button');
    const messageDiv = document.getElementById('like-message');
    
    // ボタンを一時的に無効化
    button.disabled = true;
    
    try {
        // いいね数を増やす
        const response = await fetch(`${API_BASE_URL}/hit?key=${LIKE_API_KEY}`, {
            method: 'GET'
        });
        
        if (!response.ok) {
            throw new Error('いいねカウンターの更新に失敗しました');
        }
        
        const data = await response.json();
        const count = data.count;
        
        // メッセージをクリア
        messageDiv.innerHTML = '';
        
        // ありがとうメッセージ
        const thankYouDiv = document.createElement('div');
        thankYouDiv.className = 'thank-you';
        thankYouDiv.textContent = 'ありがとう！';
        messageDiv.appendChild(thankYouDiv);
        
        // カウント表示
        const countDiv = document.createElement('div');
        countDiv.className = 'like-count';
        countDiv.textContent = `いいね数: ${count.toLocaleString()}`;
        messageDiv.appendChild(countDiv);
        
        // ゾロ目チェック
        if (isZorome(count)) {
            const zoromeDiv = document.createElement('div');
            zoromeDiv.className = 'zorome';
            zoromeDiv.textContent = 'ゾロ目だ！';
            messageDiv.appendChild(zoromeDiv);
            
            // 紙吹雪エフェクト
            createConfetti();
        }
        
        // 3秒後にボタンを再度有効化
        setTimeout(() => {
            button.disabled = false;
        }, 3000);
        
    } catch (error) {
        console.error('いいねエラー:', error);
        messageDiv.innerHTML = '<div style="color: red;">エラーが発生しました</div>';
        button.disabled = false;
    }
}

// 紙吹雪エフェクト（ゾロ目時）
function createConfetti() {
    const confettiCount = 50;
    const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#e056fd'];
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${Math.random() * 100}%;
            top: -10px;
            opacity: ${Math.random() * 0.5 + 0.5};
            transform: rotate(${Math.random() * 360}deg);
            pointer-events: none;
            z-index: 9999;
        `;
        
        document.body.appendChild(confetti);
        
        // アニメーション
        const duration = Math.random() * 3 + 2;
        const horizontalMovement = (Math.random() - 0.5) * 100;
        
        confetti.animate([
            { transform: `translateY(0) translateX(0) rotate(0deg)`, opacity: 1 },
            { transform: `translateY(${window.innerHeight + 10}px) translateX(${horizontalMovement}px) rotate(${Math.random() * 720}deg)`, opacity: 0 }
        ], {
            duration: duration * 1000,
            easing: 'ease-out'
        }).onfinish = () => confetti.remove();
    }
}

// 現在のいいね数を表示
async function showCurrentLikeCount() {
    try {
        const response = await fetch(`${API_BASE_URL}/get?key=${LIKE_API_KEY}`, {
            method: 'GET'
        });
        
        if (response.ok) {
            const data = await response.json();
            const messageDiv = document.getElementById('like-message');
            messageDiv.innerHTML = `<div class="like-count">現在のいいね数: ${data.count.toLocaleString()}</div>`;
        }
    } catch (error) {
        console.error('いいね数取得エラー:', error);
    }
}

// ページ読み込み時の処理
document.addEventListener('DOMContentLoaded', () => {
    // アクセスカウンターを更新（初回アクセス時のみカウントアップ）
    if (!sessionStorage.getItem('counted')) {
        updateAccessCounter();
        sessionStorage.setItem('counted', 'true');
    } else {
        // 既にカウント済みの場合は現在の数を表示
        showCurrentAccessCount();
    }
    
    // 現在のいいね数を表示
    showCurrentLikeCount();
    
    // いいねボタンのイベントリスナー
    document.getElementById('like-button').addEventListener('click', handleLikeButton);
});