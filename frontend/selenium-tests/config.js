const path = require('path');

// Target URL for local web frontend file or server
const INDEX_HTML_PATH = path.resolve(__dirname, '../../index.html');
const BASE_URL = process.env.WEB_APP_URL || `file://${INDEX_HTML_PATH}`;

module.exports = {
    BASE_URL: BASE_URL,
    BROWSER: process.env.SELENIUM_BROWSER || 'chrome',
    HEADLESS: process.env.HEADLESS === 'true',
    DEFAULT_TIMEOUT: 15000,
    EXPLICIT_WAIT: 10000,
    TEST_USERS: {
        PATIENT: {
            email: 'patient@smileapp.com',
            password: 'PatientPassword123!',
            name: 'Little Buddy',
            doctorId: '1176'
        },
        DOCTOR: {
            email: 'doctor@smileapp.com',
            password: 'DoctorPassword123!',
            name: 'Dr. Smile Dental',
            doctorId: '1176'
        }
    }
};
