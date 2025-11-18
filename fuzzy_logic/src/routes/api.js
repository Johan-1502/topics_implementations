// src/routes/api.js
const express = require('express');
const router = express.Router();
const fuzzyController = require('../controllers/fuzzyController');

// Ruta para el Tema 1: Lógica Difusa
router.post('/fuzzy/simulate', fuzzyController.simulateHVAC);

// Aquí agregaremos los otros dos temas después
// router.post('/tema2/simulate', ...);

module.exports = router;
