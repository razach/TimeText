## Online Availability Sharing Tool: Requirements and Technical Specifications

**Version:** 1.0
**Date:** May 23, 2025

**1. Introduction**

This document outlines the requirements and technical specifications for a simple online tool that allows users to select time slots on a calendar UI and export their availability as a text-based table. The primary goal is to provide a free, easy-to-use utility for quickly sharing availability via email or other text-based communication.

**2. User Stories**

*   As a user, I want to visually select dates and time slots on a calendar.
*   As a user, I want to be able to specify the timezone for my availability.
*   As a user, I want to be able to specify a different timezone for the recipient to see the converted times.
*   As a user, I want to choose the granularity of the time slots I select (e.g., 15-minute, 30-minute, 1-hour chunks).
*   As a user, I want to be able to select continuous bands of availability (e.g., 9 AM - 5 PM).
*   As a user, I want the tool to generate a plain text representation of my selected availability.
*   As a user, I want to easily copy the generated text to my clipboard.
*   As a user, I want to use the tool without needing to sign up or log in.
*   As a user, I want the tool to be simple and intuitive to use.

**3. Functional Requirements**

*   **FR1: Calendar Interface**
    *   The application must display a calendar interface (e.g., weekly view).
    *   Users must be able to navigate to different weeks/days.
    *   Users must be able to click and drag to select time slots.
    *   Selected time slots must be visually highlighted.
*   **FR2: Timezone Selection**
    *   The application must allow users to select their local timezone ("My Timezone").
    *   The application must allow users to select a target timezone for conversion ("Recipient's Timezone").
    *   A list of standard timezones must be available for selection.
*   **FR3: Availability Granularity**
    *   Users must be able to choose the duration of individual selectable slots (e.g., 15 minutes, 30 minutes, 1 hour).
    *   The calendar display should adjust to reflect the chosen granularity.
*   **FR4: Availability Export Format**
    *   Users must be able to choose between exporting availability as discrete chunks (e.g., 9:00 AM, 9:15 AM, 9:30 AM) or continuous bands (e.g., 9:00 AM - 12:00 PM).
*   **FR5: Text Output Generation**
    *   The application must generate a plain text table summarizing the selected availability.
    *   The table should clearly list dates and corresponding available time slots.
    *   If a "Recipient's Timezone" is selected, the output should show the times in both the user's timezone and the recipient's timezone.
    *   Example output format:
        ```
        Here's my availability:

        Date        | My Timezone (PDT) | Recipient's Timezone (EDT)
        ------------|-------------------|---------------------------
        Mon, May 26 | 9:00 AM - 11:00 AM| 12:00 PM - 2:00 PM
        Mon, May 26 | 2:00 PM - 3:00 PM | 5:00 PM - 6:00 PM
        Wed, May 28 | 10:00 AM          | 1:00 PM
        Wed, May 28 | 10:30 AM          | 1:30 PM
        ```
*   **FR6: Copy to Clipboard**
    *   A button must be provided to easily copy the generated text output to the user's clipboard.
*   **FR7: No User Authentication**
    *   The application must be usable without requiring user registration or login.

**4. Non-Functional Requirements**

*   **NFR1: Usability**
    *   The interface should be intuitive and require minimal instruction.
    *   The process of selecting slots and generating text should be quick and efficient.
*   **NFR2: Performance**
    *   The UI should be responsive.
    *   Text generation should be near instantaneous.
*   **NFR3: Cost**
    *   Hosting and operational costs should be minimized, ideally free.
*   **NFR4: Accessibility**
    *   The application should strive to meet basic web accessibility standards (WCAG AA).
*   **NFR5: Simplicity**
    *   The design and functionality should be kept simple, focusing on the core task.

**5. Technical Specifications**

*   **TS1: Frontend (User Interface)**
    *   **Technology:** HTML, CSS, JavaScript.
    *   **Framework/Libraries (Recommended):** A lightweight JavaScript library/framework for interactivity (e.g., Preact, Svelte, or even vanilla JavaScript if the calendar component is simple enough). A pre-built calendar component library could be considered to save development time (e.g., FullCalendar - ensure licensing allows free use, or a simpler custom-built one).
    *   **Functionality:**
        *   Render the calendar.
        *   Handle user interactions (date navigation, slot selection).
        *   Manage input fields for timezone and granularity.
        *   Make API calls to the backend.
        *   Display the generated text output.
        *   Implement the "Copy to Clipboard" feature.
*   **TS2: Backend (API Service)**
    *   **Technology:** Python.
    *   **Framework (Recommended):** A lightweight Python web framework like Flask or FastAPI.
    *   **Functionality:**
        *   Expose an API endpoint that accepts a JSON object containing selected slots, timezones, and output preferences.
        *   Implement the logic for timezone conversion.
        *   Implement the logic for formatting the availability data into the specified plain text table.
        *   Return the formatted text string.
*   **TS3: API Design**
    *   **Endpoint:** `/api/generate_availability_text`
    *   **Method:** `POST`
    *   **Request Body (JSON):**
        ```json
        {
          "selected_slots": [ // Array of selected time slots
            { "start": "YYYY-MM-DDTHH:mm:ssZ", "end": "YYYY-MM-DDTHH:mm:ssZ" },
            // ... more slots
          ],
          "user_timezone": "America/Los_Angeles", // IANA timezone string
          "recipient_timezone": "America/New_York", // IANA timezone string (optional)
          "output_format": "continuous" // "continuous" or "chunks"
          "slot_granularity_minutes": 30 // e.g., 15, 30, 60 (used if output_format is "chunks")
        }
        ```
    *   **Success Response (200 OK):**
        *   **Content-Type:** `text/plain`
        *   **Body:** The generated plain text availability table.
    *   **Error Response (e.g., 400 Bad Request):**
        *   **Content-Type:** `application/json`
        *   **Body:**
            ```json
            {
              "error": "Descriptive error message"
            }
            ```
*   **TS4: Python Function (Core Logic)**
    *   **Input:** A Python dictionary representing the parsed JSON request body.
    *   **Processing:**
        *   Use a library like `pytz` or Python's built-in `zoneinfo` (Python 3.9+) for accurate timezone conversions.
        *   Logic to group and format slots based on `output_format` and `slot_granularity_minutes`.
        *   String manipulation to build the text table.
    *   **Output:** A string containing the formatted plain text.

**6. Deployment (Hosting)**

*   **Frontend (Static UI):**
    *   **Options:**
        *   **Netlify:** Offers a generous free tier for static sites with CI/CD integration.
        *   **Vercel:** Similar to Netlify, good free tier for static sites and serverless functions.
        *   **GitHub Pages:** Free hosting directly from a GitHub repository.
        *   **Render:** Free static site hosting with auto-deploys from Git.
        *   **AWS S3:** Can host static websites, free tier for limited requests.
        *   **Cloudflare Pages:** Another strong option for static site hosting with a global CDN.
    *   **Recommendation:** Start with Netlify, Vercel, or GitHub Pages for simplicity and free tier.
*   **Backend (Python API):**
    *   **Options (Serverless Functions are ideal for cost-effectiveness):**
        *   **Render:** Supports Python web services; free tier available for services (might have limitations like spin-down).
        *   **Vercel:** Supports serverless functions in Python on its free tier.
        *   **Netlify Functions:** Can deploy Python functions.
        *   **AWS Lambda + API Gateway:** Very scalable and cost-effective (pay-per-use, generous free tier), but slightly more complex setup.
        *   **Google Cloud Functions:** Similar to AWS Lambda, pay-per-use with a free tier.
        *   **PythonAnywhere:** Offers free tiers that can host simple Flask/Django apps, though custom domain might be paid.
        *   **Heroku:** Historically popular, offers a free tier (dynos sleep after inactivity).
    *   **Recommendation:**
        *   For maximum simplicity with a web framework like Flask/FastAPI: **Render**'s free service tier.
        *   For a serverless approach (potentially more cost-effective at scale): **Vercel Serverless Functions** or **Netlify Functions** if the frontend is also hosted there, or AWS Lambda / Google Cloud Functions if more AWS/GCP ecosystem integration is desired later.

**7. Inspirations Review**

*   **Microsoft Support Article:** Illustrates the desired end-output (text-based availability). The proposed tool automates the manual process described.
*   **WhenAvailable.com:** A more feature-rich application. The proposed tool aims for a much simpler subset of its functionality, focusing on the core "select and export text" without accounts or event management. The visual calendar selection is a key inspiration.