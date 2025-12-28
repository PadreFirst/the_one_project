// Initialize Telegram WebApp
const tg = window.Telegram.WebApp;
tg.expand(); // Раскрываем Mini App на весь экран
tg.ready(); // Сообщаем Telegram что Mini App готов

// API Base URL (меняй на ngrok URL при деплое)
const API_BASE = window.location.origin;

// State
let currentKingData = null;

// Load current king data
async function loadCurrentKing() {
    try {
        const response = await fetch(`${API_BASE}/api/current`, {
            headers: {
                'ngrok-skip-browser-warning': 'true'
            }
        });
        const result = await response.json();
        
        if (result.success) {
            currentKingData = result.data;
            displayCurrentKing(result.data);
        } else {
            console.error('Error loading king:', result.error);
        }
    } catch (error) {
        console.error('API Error:', error);
        document.getElementById('kingPhoto').innerHTML = '<div class="loading">Error loading data</div>';
    }
}

// Display current king
function displayCurrentKing(data) {
    // Photo
    const photoContainer = document.getElementById('kingPhoto');
    if (data.photo_id && data.photo_id !== '') {
        // Показываем фото напрямую через наш API
        const photoUrl = `${API_BASE}/api/photo/${data.photo_id}`;
        photoContainer.innerHTML = `<img src="${photoUrl}" alt="THE ONE" onerror="this.parentElement.innerHTML='<div style=\\'font-size: 5em;\\'>👑</div>'">`;
    } else {
        photoContainer.innerHTML = '<div style="font-size: 5em;">👑</div>';
    }

    // Name with visual indication for anonymous
    const nameEl = document.getElementById('kingName');
    const isAnonymous = !data.user_link || data.user_link === 'Anonymous' || data.user_link === '';
    
    if (isAnonymous) {
        nameEl.innerHTML = '<span style="opacity: 0.5; text-decoration: line-through;">Anonymous</span>';
    } else {
        nameEl.textContent = data.user_link;
    }

    // Caption (text from user) - с кликабельными ссылками
    const captionEl = document.getElementById('kingCaption');
    if (data.text && data.text.trim() !== '') {
        // Конвертируем ссылки в кликабельные (простая реализация)
        const textWithLinks = data.text.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" style="color: #daa520; text-decoration: underline;">$1</a>'
        );
        captionEl.innerHTML = `💬 "${textWithLinks}"`;
    } else {
        captionEl.innerHTML = '';
    }

    // Price
    document.getElementById('priceXTR').textContent = data.simulated_price;
    document.getElementById('priceUSD').textContent = `~$${data.usd_estimate}`;
}

// Load Hall of Fame
async function loadHallOfFame() {
    try {
        const response = await fetch(`${API_BASE}/api/hall-of-fame`, {
            headers: {
                'ngrok-skip-browser-warning': 'true'
            }
        });
        const result = await response.json();
        
        if (result.success) {
            displayHallOfFame(result.data);
        } else {
            console.error('Error loading hall:', result.error);
        }
    } catch (error) {
        console.error('API Error:', error);
        document.getElementById('hallOfFame').innerHTML = '<div class="loading">Error loading Hall of Fame</div>';
    }
}

// Display Hall of Fame with photos
function displayHallOfFame(data) {
    const container = document.getElementById('hallOfFame');
    
    if (data.length === 0) {
        container.innerHTML = '<div style="text-align: center; opacity: 0.7; padding: 20px;">No entries yet. Be the first!</div>';
        return;
    }

    const medals = ['🥇', '🥈', '🥉'];
    const html = data.map((item, index) => {
        const rank = index < 3 ? medals[index] : `#${index + 1}`;
        const displayName = item.user_link && item.user_link !== 'Anonymous' && item.user_link !== '' 
            ? item.user_link 
            : 'Anonymous';
        
        // Фото для Hall of Fame
        const photoHtml = item.photo_id 
            ? `<div class="hall-photo"><img src="${API_BASE}/api/photo/${item.photo_id}" alt="${displayName}"></div>`
            : `<div class="hall-photo" style="display: flex; align-items: center; justify-content: center; font-size: 1.5em;">👑</div>`;
        
        // Текст (если есть)
        const captionHtml = item.text && item.text.trim() !== ''
            ? `<div class="hall-caption">"${item.text}"</div>`
            : '';
        
        return `
            <div class="hall-item">
                <div class="hall-rank">${rank}</div>
                ${photoHtml}
                <div class="hall-info">
                    <div class="hall-username">${displayName}</div>
                    ${captionHtml}
                </div>
                <div class="hall-price">${item.price} ⭐</div>
            </div>
        `;
    }).join('');
    
    container.innerHTML = html;
}

// Dethrone button handler
document.getElementById('dethroneBtn').addEventListener('click', () => {
    if (!currentKingData) {
        tg.showAlert('Loading data, please wait...');
        return;
    }

    // Открываем бота с командой /buy
    tg.openTelegramLink('https://t.me/the_worlds_frame_bot?start=buy');
    
    // Закрываем Mini App чтобы юзер сразу видел бота
    tg.close();
});

// Share button handler
document.getElementById('shareBtn').addEventListener('click', () => {
    const kingName = currentKingData?.user_link || 'Unclaimed';
    const price = currentKingData?.simulated_price || 1;
    
    // Viral share text
    const shareText = 
        `👑 THE WORLD'S FRAME\n\n` +
        `One photo. One message. Only ONE person in the world.\n\n` +
        `Current holder: ${kingName}\n` +
        `Throne price: ${price} ⭐ Stars\n\n` +
        `Can you take their place?`;
    
    const shareUrl = 'https://t.me/the_worlds_frame_bot/app';
    
    tg.openTelegramLink(`https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(shareText)}`);
});

// Initialize app
async function init() {
    await loadCurrentKing();
    await loadHallOfFame();
    
    // Обновляем данные каждые 30 секунд
    setInterval(async () => {
        await loadCurrentKing();
        await loadHallOfFame();
    }, 30000);
}

// Start app
init();
