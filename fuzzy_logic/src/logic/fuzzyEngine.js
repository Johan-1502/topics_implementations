// src/logic/fuzzyEngine.js

class FuzzyEngine {
    
    // --- Funciones de Pertenencia ---
    triangular(x, a, b, c) {
        return Math.max(0, Math.min((x - a) / (b - a), (c - x) / (c - b)));
    }

    leftShoulder(x, a, b) {
        if (x <= a) return 1;
        if (x >= b) return 0;
        return (b - x) / (b - a);
    }

    rightShoulder(x, a, b) {
        if (x <= a) return 0;
        if (x >= b) return 1;
        return (x - a) / (b - a);
    }

    // --- 1. Fuzzificación ---
    fuzzify(error, dError) {
        // VARIABLE 1: ERROR (Temperatura Actual - Meta)
        // Rango: -10 a +10
        const errorSets = {
            frio: this.leftShoulder(error, -5, 0),
            ideal: this.triangular(error, -2, 0, 2),
            caliente: this.rightShoulder(error, 0, 5)
        };

        // VARIABLE 2: DERIVADA (¿Qué tan rápido cambia?)
        // Rango: -5 (Enfriando rápido) a +5 (Calentando rápido)
        const deltaSets = {
            enfriando: this.leftShoulder(dError, -3, -0.5),
            estable: this.triangular(dError, -1, 0, 1),
            calentando: this.rightShoulder(dError, 0.5, 3)
        };

        return { errorSets, deltaSets };
    }

    // --- 2. Evaluación de Reglas (Matriz de Inferencia) ---
    evaluateRules(f) {
        const e = f.errorSets; // Sets del Error
        const d = f.deltaSets; // Sets de la Derivada

        // Matriz de Reglas (9 Casos Posibles)
        // Usamos Math.min (AND lógico) para combinar condiciones
        const rules = [
            // CASO 1: Hace CALOR
            { strength: Math.min(e.caliente, d.calentando), output: 100 }, // Calor + Subiendo = MAXIMA POTENCIA
            { strength: Math.min(e.caliente, d.estable),    output: 80 },  // Calor + Estable = Alta
            { strength: Math.min(e.caliente, d.enfriando),  output: 50 },  // Calor + Bajando = Media (inercia)

            // CASO 2: Temperatura IDEAL (Aquí está la magia de la predicción)
            { strength: Math.min(e.ideal, d.calentando), output: 40 },     // Ideal + Subiendo = Prender suave (Anticipación)
            { strength: Math.min(e.ideal, d.estable),    output: 0 },      // Ideal + Estable = Apagado
            { strength: Math.min(e.ideal, d.enfriando),  output: 0 },      // Ideal + Bajando = Apagado

            // CASO 3: Hace FRIO
            { strength: Math.min(e.frio, d.calentando), output: 0 },
            { strength: Math.min(e.frio, d.estable),    output: 0 },
            { strength: Math.min(e.frio, d.enfriando),  output: 0 }      // Frío + Bajando = Apagado (o Calefacción si tuvieras)
        ];

        return rules;
    }

    // --- 3. Defuzzificación ---
    defuzzify(rules) {
        let numerator = 0;
        let denominator = 0;

        rules.forEach(rule => {
            if (rule.strength > 0) {
                numerator += (rule.strength * rule.output);
                denominator += rule.strength;
            }
        });

        return denominator === 0 ? 0 : numerator / denominator;
    }

    calculateFanSpeed(currentTemp, targetTemp, rateOfChange) {
        const error = currentTemp - targetTemp;
        
        // 1. Fuzzificar ambas entradas
        const fuzzyInputs = this.fuzzify(error, rateOfChange);
        
        // 2. Inferir con reglas complejas
        const activeRules = this.evaluateRules(fuzzyInputs);
        
        // 3. Obtener salida concreta
        const speed = this.defuzzify(activeRules);

        return {
            inputs: { currentTemp, targetTemp, error, rateOfChange },
            fuzzyAnalysis: fuzzyInputs,
            output: { fanSpeed: Math.round(speed) }
        };
    }
}

module.exports = new FuzzyEngine();