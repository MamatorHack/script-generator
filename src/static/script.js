// Variables globales
let currentScript = null;

// Éléments DOM
const articleInput = document.getElementById('articleInput');
const charCount = document.getElementById('charCount');
const generateBtn = document.getElementById('generateBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const scriptParts = document.getElementById('scriptParts');
const totalDuration = document.getElementById('totalDuration');
const errorMessage = document.getElementById('errorMessage');
const downloadBtn = document.getElementById('downloadBtn');
const newScriptBtn = document.getElementById('newScriptBtn');
const retryBtn = document.getElementById('retryBtn');
const emotionsModal = document.getElementById('emotionsModal');

// Émotions avec leurs icônes
const emotionIcons = {
    happy: '😊',
    sad: '😢',
    angry: '😠',
    fearful: '😨',
    disgusted: '🤢',
    surprised: '😲',
    neutral: '😐'
};

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    updateCharCount();
});

// Configuration des écouteurs d'événements
function setupEventListeners() {
    articleInput.addEventListener('input', updateCharCount);
    generateBtn.addEventListener('click', generateScript);
    downloadBtn.addEventListener('click', downloadScript);
    newScriptBtn.addEventListener('click', resetForm);
    retryBtn.addEventListener('click', generateScript);
    
    // Fermer la modal en cliquant à l'extérieur
    emotionsModal.addEventListener('click', function(e) {
        if (e.target === emotionsModal) {
            hideEmotions();
        }
    });
}

// Mise à jour du compteur de caractères
function updateCharCount() {
    const text = articleInput.value;
    const count = text.length;
    
    charCount.textContent = `${count} caractères`;
    
    // Activer/désactiver le bouton selon la longueur
    if (count >= 50) {
        generateBtn.disabled = false;
        charCount.style.color = 'var(--success-color)';
    } else {
        generateBtn.disabled = true;
        charCount.style.color = 'var(--text-secondary)';
    }
}

// Génération du script
async function generateScript() {
    const article = articleInput.value.trim();
    
    if (article.length < 50) {
        showError('L\'article doit contenir au moins 50 caractères.');
        return;
    }
    
    // Afficher le loading
    showLoading();
    
    try {
        const response = await fetch('/api/script/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ article: article })
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            currentScript = data;
            showResults(data);
        } else {
            showError(data.error || 'Erreur lors de la génération du script.');
        }
    } catch (error) {
        console.error('Erreur:', error);
        showError('Erreur de connexion. Vérifiez que le serveur est démarré.');
    }
}

// Affichage du loading
function showLoading() {
    hideAllSections();
    loadingSection.classList.remove('hidden');
}

// Affichage des résultats
function showResults(data) {
    hideAllSections();
    
    // Mettre à jour la durée totale
    totalDuration.textContent = `${data.total_duration} secondes`;
    
    // Générer les parties du script
    scriptParts.innerHTML = '';
    
    data.script.forEach((part, index) => {
        const partElement = createScriptPartElement(part, index + 1);
        scriptParts.appendChild(partElement);
    });
    
    resultsSection.classList.remove('hidden');
    
    // Scroll vers les résultats
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

// Création d'un élément de partie de script
function createScriptPartElement(part, index) {
    const partDiv = document.createElement('div');
    partDiv.className = 'script-part';
    
    const typeLabels = {
        accroche: 'Accroche',
        content: 'Contenu',
        call_to_action: 'Appel à l\'action'
    };
    
    partDiv.innerHTML = `
        <div class="part-header">
            <div class="part-title">
                <span>Partie ${index}</span>
                <span class="part-type ${part.type}">${typeLabels[part.type]}</span>
            </div>
            <div class="emotion-badge">
                <span>${emotionIcons[part.emotion] || '😐'}</span>
                <span>${part.emotion}</span>
            </div>
        </div>
        <div class="part-content">
            ${part.text}
        </div>
        <div class="part-meta">
            <span><i class="fas fa-font"></i> ${part.character_count} caractères</span>
            <span><i class="fas fa-clock"></i> ${part.duration_seconds} secondes</span>
        </div>
    `;
    
    return partDiv;
}

// Affichage des erreurs
function showError(message) {
    hideAllSections();
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
}

// Masquer toutes les sections
function hideAllSections() {
    loadingSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    errorSection.classList.add('hidden');
}

// Téléchargement du script
function downloadScript() {
    if (!currentScript) {
        showError('Aucun script à télécharger.');
        return;
    }
    
    const dataStr = JSON.stringify(currentScript, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = `script_${new Date().toISOString().slice(0, 10)}.json`;
    link.click();
    
    // Nettoyer l'URL
    URL.revokeObjectURL(link.href);
}

// Réinitialisation du formulaire
function resetForm() {
    articleInput.value = '';
    currentScript = null;
    updateCharCount();
    hideAllSections();
    
    // Scroll vers le haut
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Affichage de la modal des émotions
function showEmotions() {
    emotionsModal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
}

// Masquage de la modal des émotions
function hideEmotions() {
    emotionsModal.classList.add('hidden');
    document.body.style.overflow = 'auto';
}

// Gestion des touches clavier
document.addEventListener('keydown', function(e) {
    // Échapper pour fermer la modal
    if (e.key === 'Escape' && !emotionsModal.classList.contains('hidden')) {
        hideEmotions();
    }
    
    // Ctrl+Enter pour générer le script
    if (e.ctrlKey && e.key === 'Enter' && !generateBtn.disabled) {
        generateScript();
    }
});

// Animation d'entrée pour les éléments
function animateElements() {
    const elements = document.querySelectorAll('.script-part');
    elements.forEach((element, index) => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            element.style.transition = 'all 0.5s ease';
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Validation en temps réel
function validateInput() {
    const text = articleInput.value;
    const words = text.trim().split(/\s+/).filter(word => word.length > 0);
    
    if (words.length < 10) {
        return 'L\'article doit contenir au moins 10 mots.';
    }
    
    if (text.length > 5000) {
        return 'L\'article ne doit pas dépasser 5000 caractères.';
    }
    
    return null;
}

// Copie du texte dans le presse-papiers
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        // Afficher une notification de succès
        showNotification('Texte copié dans le presse-papiers !');
    }).catch(err => {
        console.error('Erreur lors de la copie:', err);
    });
}

// Notification toast
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: var(--success-color);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        z-index: 1001;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    if (type === 'error') {
        notification.style.background = 'var(--error-color)';
    }
    
    document.body.appendChild(notification);
    
    // Animation d'entrée
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Suppression automatique
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Sauvegarde automatique dans le localStorage
function saveToLocalStorage() {
    const data = {
        article: articleInput.value,
        script: currentScript,
        timestamp: new Date().toISOString()
    };
    
    localStorage.setItem('scriptGenerator_data', JSON.stringify(data));
}

// Chargement depuis le localStorage
function loadFromLocalStorage() {
    const saved = localStorage.getItem('scriptGenerator_data');
    if (saved) {
        try {
            const data = JSON.parse(saved);
            
            // Charger l'article si moins de 24h
            const savedTime = new Date(data.timestamp);
            const now = new Date();
            const hoursDiff = (now - savedTime) / (1000 * 60 * 60);
            
            if (hoursDiff < 24 && data.article) {
                articleInput.value = data.article;
                updateCharCount();
            }
        } catch (e) {
            console.error('Erreur lors du chargement des données sauvegardées:', e);
        }
    }
}

// Sauvegarde automatique lors de la saisie
articleInput.addEventListener('input', debounce(saveToLocalStorage, 1000));

// Fonction de debounce
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Charger les données sauvegardées au démarrage
document.addEventListener('DOMContentLoaded', loadFromLocalStorage);

