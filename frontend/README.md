# Availability Calendar Frontend

A simple and intuitive web interface for selecting and sharing availability time slots.

## Features

- Interactive calendar interface for selecting time slots
- Timezone selection and conversion
- Customizable time slot duration (15min, 30min, 1hour)
- Two output formats: continuous bands or individual slots
- Copy to clipboard functionality
- Responsive design for all devices

## Setup

1. Clone the repository
2. Navigate to the frontend directory
3. Open `index.html` in your browser

For development, you can use any local server. For example, with Python:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000` in your browser.

## API Integration

The frontend integrates with the Availability Calendar API at `https://timetext-1d1c.onrender.com`. You'll need to:

1. Get an API key from the backend service
2. Replace `'your-api-key-here'` in `calendar.js` with your actual API key

## Dependencies

The frontend uses the following external libraries:

- FullCalendar (v6.1.10) - For the calendar interface
- Moment.js (v2.29.1) - For date/time handling
- Moment Timezone (v0.5.34) - For timezone support

All dependencies are loaded from CDNs for simplicity.

## Development

The frontend is built with vanilla JavaScript and consists of three main files:

- `index.html` - The main HTML structure
- `styles.css` - Styling and responsive design
- `calendar.js` - Calendar component and interactions
- `app.js` - Application initialization and event handling

## Deployment

The frontend is designed to be hosted on GitHub Pages. To deploy:

1. Create a new GitHub repository
2. Push the frontend code to the repository
3. Enable GitHub Pages in the repository settings
4. Select the branch to deploy (usually `main` or `master`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 