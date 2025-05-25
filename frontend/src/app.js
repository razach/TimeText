// (Remove: import { DEFAULT_TIMEZONE } from './config.js';)

document.addEventListener('DOMContentLoaded', () => {
    // Wait for moment-timezone to be fully loaded
    if (typeof moment !== 'undefined' && typeof moment.tz !== 'undefined') {
        initializeApp();
    } else {
        // If moment-timezone isn't loaded yet, wait for it
        const checkMoment = setInterval(() => {
            if (typeof moment !== 'undefined' && typeof moment.tz !== 'undefined') {
                clearInterval(checkMoment);
                initializeApp();
            }
        }, 100);
    }
});

function initializeApp() {
    // Initialize the calendar
    const calendar = new Calendar();

    // Populate timezone dropdowns
    populateTimezones();

    // Set up event listeners
    setupEventListeners(calendar);
}

function populateTimezones() {
    const timezones = moment.tz.names();
    const userTimezoneSelect = document.getElementById('userTimezone');
    const recipientTimezoneSelect = document.getElementById('recipientTimezone');

    // Clear existing options
    userTimezoneSelect.innerHTML = '';
    recipientTimezoneSelect.innerHTML = '<option value="">No conversion</option>';

    // Sort timezones for better usability
    timezones.sort();

    // Populate both dropdowns with timezones
    timezones.forEach(timezone => {
        const userOption = new Option(timezone, timezone);
        const recipientOption = new Option(timezone, timezone);
        userTimezoneSelect.add(userOption);
        recipientTimezoneSelect.add(recipientOption);
    });

    // Set default timezone to user's local timezone or the default from config
    const localTimezone = moment.tz.guess();
    userTimezoneSelect.value = localTimezone || window.DEFAULT_TIMEZONE;
}

function setupEventListeners(calendar) {
    // Timezone change handlers
    document.getElementById('userTimezone').addEventListener('change', () => {
        calendar.updateTextOutput();
    });

    document.getElementById('recipientTimezone').addEventListener('change', () => {
        calendar.updateTextOutput();
    });

    // Format change handlers
    document.getElementById('slotGranularity').addEventListener('change', (e) => {
        const minutes = parseInt(e.target.value);
        calendar.updateSlotDuration(minutes);
        calendar.updateTextOutput();
    });

    document.getElementById('outputFormat').addEventListener('change', () => {
        calendar.updateTextOutput();
    });

    // Copy to clipboard functionality
    document.getElementById('copyButton').addEventListener('click', async () => {
        const text = document.getElementById('availabilityText').textContent;
        try {
            await navigator.clipboard.writeText(text);
            const button = document.getElementById('copyButton');
            const originalText = button.textContent;
            button.textContent = 'Copied!';
            button.style.backgroundColor = 'var(--success-color)';
            setTimeout(() => {
                button.textContent = originalText;
                button.style.backgroundColor = '';
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    });
} 