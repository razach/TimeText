// Import configuration
// (Remove: import { API_CONFIG, ENDPOINTS } from './config.js';)

class Calendar {
    constructor() {
        this.calendar = null;
        this.selectedSlots = [];
        this.initializeCalendar();
    }

    initializeCalendar() {
        const calendarEl = document.getElementById('calendar');
        
        this.calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'timeGridWeek',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'timeGridWeek,timeGridDay'
            },
            slotMinTime: '08:00:00',
            slotMaxTime: '20:00:00',
            slotDuration: '00:30:00',
            selectable: true,
            selectMirror: true,
            dayMaxEvents: true,
            select: this.handleSelect.bind(this),
            eventClick: this.handleEventClick.bind(this),
            events: this.selectedSlots,
            height: 'auto',
            allDaySlot: false,
            slotLabelInterval: '01:00',
            slotLabelFormat: {
                hour: 'numeric',
                minute: '2-digit',
                meridiem: 'short'
            },
            views: {
                timeGridWeek: {
                    slotDuration: '00:30:00',
                    slotLabelInterval: '01:00'
                },
                timeGridDay: {
                    slotDuration: '00:30:00',
                    slotLabelInterval: '01:00'
                }
            }
        });

        this.calendar.render();
    }

    handleSelect(selectInfo) {
        const start = selectInfo.start;
        const end = selectInfo.end;
        
        // Add the new slot to our array
        this.selectedSlots.push({
            start: start.toISOString(),
            end: end.toISOString()
        });

        // Update the calendar display
        this.calendar.addEvent({
            start: start,
            end: end,
            display: 'block'
        });

        // Trigger the update of the text output
        this.updateTextOutput();
    }

    handleEventClick(clickInfo) {
        // Remove the clicked event
        clickInfo.event.remove();
        
        // Remove from our array
        const start = clickInfo.event.start.toISOString();
        const end = clickInfo.event.end.toISOString();
        this.selectedSlots = this.selectedSlots.filter(slot => 
            slot.start !== start || slot.end !== end
        );

        // Update the text output
        this.updateTextOutput();
    }

    updateTextOutput() {
        // Get the current settings
        const userTimezone = document.getElementById('userTimezone').value;
        const recipientTimezone = document.getElementById('recipientTimezone').value;
        const outputFormat = document.getElementById('outputFormat').value;
        const slotGranularity = parseInt(document.getElementById('slotGranularity').value);

        // Prepare the request data
        const requestData = {
            selected_slots: this.selectedSlots,
            user_timezone: userTimezone,
            recipient_timezone: recipientTimezone || null,
            output_format: outputFormat,
            slot_granularity_minutes: slotGranularity
        };

        // Call the API to generate the text
        this.generateAvailabilityText(requestData);
    }

    async generateAvailabilityText(requestData) {
        try {
            const response = await fetch(`${window.API_CONFIG.BASE_URL}${window.ENDPOINTS.GENERATE_AVAILABILITY}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-API-Key': window.API_CONFIG.API_KEY
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error('Failed to generate availability text');
            }

            const data = await response.json();
            document.getElementById('availabilityText').textContent = data.text_output;
        } catch (error) {
            console.error('Error:', error);
            document.getElementById('availabilityText').textContent = 'Error generating availability text. Please try again.';
        }
    }

    // Method to update slot duration
    updateSlotDuration(minutes) {
        // Convert minutes to HH:mm:ss format
        const hours = Math.floor(minutes / 60).toString().padStart(2, '0');
        const mins = (minutes % 60).toString().padStart(2, '0');
        this.calendar.setOption('slotDuration', `${hours}:${mins}:00`);
    }

    // Method to clear all selected slots
    clearAllSlots() {
        this.selectedSlots = [];
        this.calendar.removeAllEvents();
        this.updateTextOutput();
    }
}

// Export the Calendar class
window.Calendar = Calendar; 