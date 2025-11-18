// src/index.js
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const apiRoutes = require('./routes/api');

const app = express();
const PORT = process.env.PORT || 3000;

// Middlewares
app.use(cors()); // Permitir peticiones desde el frontend
app.use(bodyParser.json());

// Rutas
app.use(express.static('public'));
app.use('/api', apiRoutes);

// Server
app.listen(PORT, () => {
    console.log(`Servidor de simulación corriendo en http://localhost:${PORT}`);
    console.log(`Endpoint disponible: POST /api/fuzzy/simulate`);
});
