const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Ensure data directory exists
const dataDir = path.join(__dirname, 'data');
if (!fs.existsSync(dataDir)) {
    fs.mkdirSync(dataDir);
}

const feedbackFile = path.join(dataDir, 'feedback.csv');

// Initialize CSV file if it doesn't exist
if (!fs.existsSync(feedbackFile)) {
    const headers = 'timestamp,date,student_name,student_id,teacher_name,subject,class_section,rating,feedback_type,message,suggestions\n';
    fs.writeFileSync(feedbackFile, headers);
}

// POST endpoint to save feedback
// Admin API endpoints
app.get('/api/admin/teachers', (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        const csvPath = path.join(__dirname, '..', 'Admin_Data', 'Teachers', 'teacher_performance.csv');
        
        if (fs.existsSync(csvPath)) {
            const csvData = fs.readFileSync(csvPath, 'utf8');
            const lines = csvData.trim().split('\n');
            const headers = lines[0].split(',');
            const teachers = lines.slice(1).map(line => {
                const values = line.split(',');
                const obj = {};
                headers.forEach((header, index) => {
                    obj[header] = values[index] || '';
                });
                return obj;
            });
            res.json(teachers);
        } else {
            res.json([]);
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load teacher data' });
    }
});

app.get('/api/admin/live-classes', (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        const csvPath = path.join(__dirname, '..', 'Admin_Data', 'live_monitoring.csv');
        
        if (fs.existsSync(csvPath)) {
            const csvData = fs.readFileSync(csvPath, 'utf8');
            const lines = csvData.trim().split('\n');
            const headers = lines[0].split(',');
            const classes = lines.slice(1).map(line => {
                const values = line.split(',');
                const obj = {};
                headers.forEach((header, index) => {
                    obj[header] = values[index] || '';
                });
                return obj;
            });
            res.json(classes);
        } else {
            res.json([]);
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load live data' });
    }
});

app.get('/api/admin/comparison', (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        const csvPath = path.join(__dirname, '..', 'Admin_Data', 'Reports', 'teacher_comparison.csv');
        
        if (fs.existsSync(csvPath)) {
            const csvData = fs.readFileSync(csvPath, 'utf8');
            const lines = csvData.trim().split('\n');
            const headers = lines[0].split(',');
            const comparison = lines.slice(1).map(line => {
                const values = line.split(',');
                const obj = {};
                headers.forEach((header, index) => {
                    obj[header] = values[index] || '';
                });
                return obj;
            });
            res.json(comparison);
        } else {
            res.json([]);
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load comparison data' });
    }
});

app.get('/api/admin/industry', (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        const csvPath = path.join(__dirname, '..', 'Admin_Data', 'Reports', 'industry_alignment.csv');
        
        if (fs.existsSync(csvPath)) {
            const csvData = fs.readFileSync(csvPath, 'utf8');
            const lines = csvData.trim().split('\n');
            const headers = lines[0].split(',');
            const industry = lines.slice(1).map(line => {
                const values = line.split(',');
                const obj = {};
                headers.forEach((header, index) => {
                    obj[header] = values[index] || '';
                });
                return obj;
            });
            res.json(industry);
        } else {
            res.json([]);
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load industry data' });
    }
});

app.get('/api/admin/summary', (req, res) => {
    try {
        const fs = require('fs');
        const path = require('path');
        const csvPath = path.join(__dirname, '..', 'Admin_Data', 'Reports', 'dashboard_summary.csv');
        
        if (fs.existsSync(csvPath)) {
            const csvData = fs.readFileSync(csvPath, 'utf8');
            const lines = csvData.trim().split('\n');
            const headers = lines[0].split(',');
            const values = lines[1].split(',');
            const summary = {};
            headers.forEach((header, index) => {
                summary[header] = values[index] || '';
            });
            res.json(summary);
        } else {
            res.json({});
        }
    } catch (error) {
        res.status(500).json({ error: 'Failed to load summary data' });
    }
});

app.post('/api/feedback', (req, res) => {
    try {
        const {
            timestamp,
            date,
            student_name,
            student_id,
            teacher_name,
            subject,
            class_section,
            rating,
            feedback_type,
            message,
            suggestions
        } = req.body;

        // Validate required fields
        if (!student_name || !student_id || !teacher_name || !subject || !class_section || !rating || !feedback_type || !message) {
            return res.status(400).json({ error: 'Missing required fields' });
        }

        // Escape commas and quotes in CSV data
        const escapeCsv = (str) => {
            if (str.includes(',') || str.includes('"') || str.includes('\n')) {
                return `"${str.replace(/"/g, '""')}"`;
            }
            return str;
        };

        // Create CSV row
        const csvRow = [
            timestamp,
            date,
            escapeCsv(student_name),
            escapeCsv(student_id),
            escapeCsv(teacher_name),
            escapeCsv(subject),
            escapeCsv(class_section),
            rating,
            escapeCsv(feedback_type),
            escapeCsv(message),
            escapeCsv(suggestions || '')
        ].join(',') + '\n';

        // Append to CSV file
        fs.appendFileSync(feedbackFile, csvRow);

        console.log(`Student feedback saved: ${student_name} (${student_id}) rated ${teacher_name} - ${subject} - Rating: ${rating}`);
        
        res.json({ 
            success: true, 
            message: 'Feedback saved successfully',
            data: req.body
        });

    } catch (error) {
        console.error('Error saving feedback:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// GET endpoint to retrieve feedback
app.get('/api/feedback', (req, res) => {
    try {
        if (!fs.existsSync(feedbackFile)) {
            return res.json([]);
        }

        const csvData = fs.readFileSync(feedbackFile, 'utf8');
        const lines = csvData.trim().split('\n');
        
        if (lines.length <= 1) {
            return res.json([]);
        }

        const headers = lines[0].split(',');
        const feedback = lines.slice(1).map(line => {
            const values = line.split(',');
            const obj = {};
            headers.forEach((header, index) => {
                obj[header] = values[index] || '';
            });
            return obj;
        });

        res.json(feedback);

    } catch (error) {
        console.error('Error reading feedback:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

// GET endpoint for feedback statistics
app.get('/api/feedback/stats', (req, res) => {
    try {
        if (!fs.existsSync(feedbackFile)) {
            return res.json({ total: 0, averageRating: 0, subjectBreakdown: {} });
        }

        const csvData = fs.readFileSync(feedbackFile, 'utf8');
        const lines = csvData.trim().split('\n');
        
        if (lines.length <= 1) {
            return res.json({ total: 0, averageRating: 0, subjectBreakdown: {} });
        }

        const feedback = lines.slice(1).map(line => {
            const values = line.split(',');
            return {
                rating: parseInt(values[5]) || 0,
                subject: values[3] || 'Unknown'
            };
        });

        const total = feedback.length;
        const averageRating = feedback.reduce((sum, f) => sum + f.rating, 0) / total;
        
        const subjectBreakdown = feedback.reduce((acc, f) => {
            acc[f.subject] = (acc[f.subject] || 0) + 1;
            return acc;
        }, {});

        res.json({
            total,
            averageRating: Math.round(averageRating * 100) / 100,
            subjectBreakdown
        });

    } catch (error) {
        console.error('Error calculating stats:', error);
        res.status(500).json({ error: 'Internal server error' });
    }
});

app.listen(PORT, () => {
    console.log(`Feedback server running on http://localhost:${PORT}`);
    console.log(`Feedback data will be saved to: ${feedbackFile}`);
});