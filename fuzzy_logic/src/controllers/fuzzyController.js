// src/controllers/fuzzyController.js
const fuzzyEngine = require('../logic/fuzzyEngine');

exports.simulateHVAC = (req, res) => {
    try {
        // Recibimos rateOfChange (Derivada) del body
        const { currentTemp, targetTemp, rateOfChange } = req.body;

        // Si no envían rateOfChange, asumimos 0 (estable)
        const delta = rateOfChange !== undefined ? parseFloat(rateOfChange) : 0;

        if (currentTemp === undefined || targetTemp === undefined) {
            return res.status(400).json({ error: 'Faltan parámetros' });
        }

        const result = fuzzyEngine.calculateFanSpeed(
            parseFloat(currentTemp), 
            parseFloat(targetTemp),
            delta
        );

        res.json({ success: true, data: result });

    } catch (error) {
        res.status(500).json({ error: error.message });
    }
};