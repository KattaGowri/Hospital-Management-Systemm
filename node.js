const express = require('express');
const app = express();

app.use(express.urlencoded({ extended: true }));

// Mock data for demonstration
const appointments = [
    { patient: 'John Doe', time: '10:00 AM', reason: 'Routine Check-up' },
];
const patients = [
    { name: 'Jane Smith', age: 45, condition: 'Hypertension', id: 123 },
];

app.get('/doctor-dashboard', (req, res) => {
    res.send(`
        <html>
            <body>
                <h1>Welcome, Dr. Paul Angie Cho</h1>
                <p>Appointments and records will be fetched here.</p>
            </body>
        </html>
    `);
});

app.post('/schedule', (req, res) => {
    const { date, availability } = req.body;
    console.log(`Updated schedule for ${date}: ${availability}`);
    res.redirect('/doctor-dashboard');
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
