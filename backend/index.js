const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const cookieParser = require('cookie-parser');
const multer = require('multer');
const axios = require('axios');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 5000;

app.use(express.json());
app.use(bodyParser.json());
app.use(cors());
app.use(cookieParser());

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, "./public/files");
    },
    filename: function (req, file, cb) {
        cb(null, `${Date.now()}_${file.originalname}`);
    },
});
const upload = multer({
    storage,
});

app.post("/upload", upload.single("file"), async (req, res) => {
    const file = req.file;

    if (!file) {
        return res.status(400).send('No file uploaded.');
    }

    const filePath = file.path;
    console.log(`File uploaded to: ${filePath}`);

    try {
        // Call the FastAPI service to get metrics
        const metricsResponse = await axios.get('http://localhost:8000/saas-metrics');

        if (metricsResponse.status === 200) {
            console.log('Metrics fetched successfully:', metricsResponse.data);
            res.json(metricsResponse.data);
        } else {
            console.error('Failed to fetch metrics', metricsResponse.statusText);
            res.status(metricsResponse.status).send('Failed to fetch metrics');
        }
    } catch (error) {
        console.error('Error fetching metrics:', error);
        res.status(500).send('Error fetching metrics');
    } finally {
        // Optionally, clean up the uploaded file
        fs.unlink(filePath, (err) => {
            if (err) {
                console.error('Failed to delete the file:', err);
            } else {
                console.log('File deleted successfully');
            }
        });
    }
});

app.get('/', (req, res) => {
    res.send("Startup App");
});

app.listen(port, () => {
    console.log(`Server started on http://localhost:${port}`);
});
