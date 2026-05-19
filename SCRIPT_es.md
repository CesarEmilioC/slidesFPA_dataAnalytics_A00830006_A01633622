# Guión del defensor &mdash; Defensa Final FPA (Español)

*Predicción del Movimiento del Precio del S&P 500 &mdash; Datos Históricos de Mercado y Análisis de Sentimiento de Noticias Financieras*

Autores: **César Castaño (A00830006)** &middot; **Brenda García (A01633622)** &middot; Tec de Monterrey, M.Sc. CS, Semestre 4.

> **Tiempo objetivo: 10 minutos.** Énfasis en **resultados y conclusiones** &mdash; el setup y la metodología se cuentan rápido; donde nos detenemos es a partir del slide 15. *Las líneas en cursiva* son conectores que se dicen al pasar el slide.

---

## 1. Portada &mdash; 10 s

Buenos días. **César Castaño** y **Brenda García**. Maestría en Ciencias de la Computación, Tec de Monterrey. Defendemos nuestro proyecto final de Data Analytics: **predicción del movimiento del S&P 500 al día siguiente, con sentimiento de noticias**.

## 2. Agenda &mdash; 10 s

Diez bloques. Setup y metodología los pasamos rápido; el grueso de la charla son **resultados, interpretación y conclusiones**.

## 3. Motivación &mdash; 30 s

El S&P 500 es el índice de referencia más seguido en Estados Unidos, con once sectores que difieren mucho en volatilidad y flujo de noticias. Predecimos **dirección**, no precio &mdash; eso es lo que la gestión de riesgo realmente necesita. El NLP reciente hace que extraer sentimiento estructurado de texto financiero sea prácticamente gratis. La pregunta de la derecha resume todo el proyecto en una sola línea.

## 4. Hipótesis &mdash; 25 s

Variable objetivo: **1 si el cierre de mañana es mayor que el de hoy, 0 en caso contrario**. Dos hipótesis: **H1** el sentimiento mejora accuracy, F1 y AUC sobre la línea base técnica; **H2** la mejora crece con la volatilidad del sector. De ahí salen tres preguntas de investigación.

## 5. Trabajo relacionado &mdash; 20 s

Cinco referencias ancla: **Bollen 2011** (el sentimiento sí predice), **Vargas 2017** (lo multimodal ayuda), **Araci 2019** (FinBERT), **Zhang 2019** (XGBoost + sentimiento es competitivo), **López de Prado 2018** (splits cronológicos, sin look-ahead).

## 6. Pipeline &mdash; 15 s

Cuatro etapas: datos de mercado, indicadores técnicos, sentimiento FinBERT, ensambles de árboles &mdash; **dieciséis corridas en total**.

## 7. Datos &mdash; 15 s

Mercado: `yfinance`, 2010-2019. Noticias: Kaggle Analyst Ratings, **1.4 millones de titulares** filtrados y limitados a 50 por día de trading con semilla fija.

## 8. Indicadores técnicos &mdash; 15 s

Siete features derivados de OHLCV: returns, dos medias móviles, RSI, volatilidad, HLC3 y volumen. El target se calcula antes de modelar &mdash; cero leakage.

## 9. Selección de sectores &mdash; 15 s

Tres anclas que cubren el rango de volatilidad: **XLP** Consumer Staples (baja), **XLK** Tecnología (mediana), **XLE** Energía (alta).

## 10. FinBERT &mdash; 20 s

Por cada titular, FinBERT devuelve positivo menos negativo como un score entre menos uno y más uno. Lo agregamos por día de trading: media, desviación estándar y conteo. `ProsusAI/finbert` pre-entrenado, batch de 32, neutro en días sin noticias.

## 11. EDA &mdash; balance de clases &mdash; 10 s

**Sesgo leve al alza**: la regla "siempre sube" ya da ~0.55 de accuracy. Por eso reportamos AUC en paralelo.

## 12. EDA &mdash; flujo de noticias &mdash; 10 s

~386 mil titulares, **cobertura del 100% de los días de trading**, sentimiento medio ligeramente positivo.

## 13. Diseño experimental &mdash; 10 s

Dos algoritmos por dos conjuntos de features por cuatro datasets &mdash; **dieciséis corridas** bajo splits idénticos.

## 14. Entrenamiento &mdash; 15 s

Split cronológico 80/20: ~2 mil días de entrenamiento, **501 días de prueba**. Hiperparámetros por defecto para que las dieciséis corridas sean comparables entre sí.

*Aquí empiezan los resultados &mdash; aquí nos detenemos.*

## 15. Resultados &mdash; solo técnico &mdash; 25 s

El titular: **el AUC se concentra en 0.50 en todos los datasets**. Los indicadores técnicos solos apenas separan los días al alza de los que no &mdash; consistente con eficiencia débil de mercado. XGB en SP500 llega a F1 0.66 sólo apoyándose en la clase mayoritaria. **XLK colapsa a clase cero**, F1 cae a 0.23. Esta es la línea base que hay que mejorar.

## 16. Resultados &mdash; técnico + sentimiento &mdash; 30 s

Dos ganancias limpias. **SP500 + Random Forest + sentimiento**: 0.56 accuracy, 0.67 F1, **0.51 AUC** &mdash; es decir, más 0.05, más 0.06, más 0.04 sobre la línea base. **XLE + XGBoost + sentimiento**: el AUC pasa de 0.48 a 0.52. Las ganancias se concentran en el índice amplio y en el sector más volátil. Los sectores de volatilidad baja y mediana prácticamente no se mueven.

## 17. Dónde vive el +0.04 de AUC &mdash; ROC + matriz de confusión &mdash; 50 s

Dos vistas del mismo resultado SP500 + Random Forest. **A la izquierda**: el overlay ROC. La curva técnico-solo cae sobre la diagonal en AUC 0.478; **técnico + sentimiento** queda por encima entre FPR 0.3 y 0.9, AUC 0.513. Esa brecha, más 0.035, es toda la contribución del sentimiento. **A la derecha**: matriz de confusión con umbral 0.5. **El recall en días al alza es 0.84** &mdash; el modelo captura casi todas las subidas &mdash; pero la precisión es 0.57 porque tolera 174 falsos positivos. Se comporta como un **clasificador agresivo con sesgo largo**: casi nunca pierde un día al alza, pero da falsas alarmas un tercio del tiempo.

## 18. Sentiment uplift &mdash; 20 s

Cada barra es un delta. **SP500 + RF positivo en las tres métricas**, **XLE + XGB positivo en Acc y AUC**, **XLP + RF es el negativo claro** &mdash; exactamente el patrón que H2 predice para sectores de baja volatilidad.

## 19. Feature importance &mdash; 20 s

`sentiment_mean`, en dorado, queda **top tres** en las dos configuraciones donde mejoró el AUC. Los features técnicos se distribuyen parejo &mdash; la señal de sentimiento es genuinamente aditiva.

## 20. Evaluación de hipótesis &mdash; 25 s

**H1 parcialmente respaldada** &mdash; funciona en el índice y en el sector de alta volatilidad, pero el panorama sectorial es mixto. **H2 parcialmente respaldada** &mdash; XLE el más volátil tiene la mayor ganancia con XGBoost, pero XLK de volatilidad mediana no se beneficia, así que el gradiente no es estrictamente monótono. **RQ2**: empate en AUC; Random Forest gana en el índice, XGBoost gana en el sector de alta volatilidad.

## 21. ¿Qué significa realmente un AUC ≈ 0.50? &mdash; 45 s

Tres puntos de referencia sobre los mismos 501 días de prueba. **Moneda al aire**: 0.50 / 0.50 / 0.50. **"Siempre sube"**: 0.55 de accuracy, 0.71 de F1 *gratis*, AUC sigue en 0.50 (no hay capacidad de ranking). **Nuestro mejor**: 0.56, 0.67, 0.51. Las barras lo hacen obvio: en accuracy y F1 estamos **encima de la línea base "siempre sube"**, más 0.05, más 0.06; en AUC las tres barras son indistinguibles. **El resultado real es el delta del sentimiento**, más 0.04 de AUC, no el nivel absoluto. Exactamente lo que predice la forma débil de la EMH.

## 22. Comparación con la literatura &mdash; 30 s

Bollen 87.6% en el Dow con ánimo de Twitter, pero en una ventana de siete meses; reproducciones en ventanas más largas caen a ~60%. Vargas ~62% con encoders profundos sobre el cuerpo completo de Reuters. FinBERT de Araci es **sentimiento a nivel de oración, no dirección al día siguiente**. Zhang ~0.56 AUC en acciones chinas con tuning por ticker. Normalizando el setup, **nuestro 0.52 AUC en el sector de alta volatilidad está en el orden correcto** &mdash; diario + sólo títulos es el régimen más difícil de la tabla.

## 23. Demo en vivo &mdash; 20 s

Demo grabada en Drive. El notebook de Colab carga los cuatro clasificadores, jala el OHLCV de hoy, califica los titulares con FinBERT y imprime UP / DOWN / STABLE por modelo. La curva de calibración a la derecha justifica el corredor 0.45-0.55 que usamos para STABLE.

## 24. Discusión &mdash; 25 s

La gráfica de la derecha hace visible la claim central: **las dieciséis configuraciones están dentro de ±0.03 de AUC = 0.50**. El sentimiento diario es una señal delgada &mdash; pierde el timing intra-día, los sectores ruidosos lo enmascaran. El colapso de XLK es el sesgo de clase de la ventana de prueba. SP500 es el que más se beneficia porque los retornos del índice agregan ruido idiosincrático y dejan una señal sistemática más limpia.

## 25. Limitaciones &mdash; 25 s

Dos nuevas primero. **Significancia**: el más 0.04 de AUC es un estimador puntual &mdash; falta un test de DeLong o un CI por bootstrap. **Realidad de costos de transacción**, en la gráfica: un costo round-trip de 5 a 10 puntos básicos erosiona la ventaja hasta break-even alrededor de 9 bp. Luego las clásicas: sesgo de cobertura de noticias, sentimiento sólo en titulares, cap de muestreo, split cronológico único, hiperparámetros sin tunear.

## 26. Realidad de trading &mdash; 35 s

Cuatro curvas de equity sobre los 501 días de prueba, partiendo de un dólar, antes de costos. **Buy-and-hold** termina en **\$1.19** &mdash; la ventana fue la cola del mercado alcista 2017-2019. Nuestro **RF + sentimiento con probabilidad ≥ 0.55** termina en **\$1.17**, con la mitad del tiempo fuera del mercado &mdash; **casi toda la subida, con menos exposición**. La estrategia aleatoria termina en \$1.09 &mdash; muy por debajo de buy-and-hold, lo que confirma que nuestra señal **no es casualidad**. Antes de costos seguimos sin ganarle a la línea base fácil; con costos realistas el cuadro se invierte. El más 0.04 de AUC es una **señal real, todavía no operable**.

## 27. Conclusiones &mdash; 50 s

Seis conclusiones. **Uno**: el sentimiento FinBERT ayuda en el índice con Random Forest, más 0.05 accuracy, más 0.06 F1, más 0.04 AUC &mdash; **pequeño pero consistente**. **Dos**: el efecto **no es monótono en la volatilidad sectorial** &mdash; XLE se beneficia, XLP y XLK no, H2 sólo parcialmente respaldada. **Tres**: el techo AUC = 0.50 es **consistente con la EMH débil** &mdash; nuestra contribución es el **signo del delta**, no una señal operable. **Cuatro**: la elección de algoritmo es **dependiente de la configuración** &mdash; Random Forest en el índice, XGBoost en el sector volátil, RQ2 no tiene un ganador universal. **Cinco**: `sentiment_mean` queda top tres en feature importance **sólo** donde realmente mejoró el AUC &mdash; la contribución es real, no un artefacto del modelo. **Seis**: antes de costos, nuestra estrategia long/flat llega a \$1.17 vs \$1.19 de buy-and-hold y \$1.09 aleatorio &mdash; **mejor que el azar, no mejor que la línea base fácil**.

## 28. Trabajo futuro &mdash; 15 s

En orden de prioridad: **test de significancia** con DeLong / bootstrap, **backtest con costos**, walk-forward, sentimiento multi-resolución, ruteo de noticias por sector, re-pesaje de clases, stress test 2020-2024.

## 29. Referencias &mdash; 5 s

Las anclas citadas; la bibliografía completa está en el manuscrito.

## 30. Gracias &mdash; 5 s

Gracias. Preguntas, por favor.

---

## Apéndices &mdash; sólo bajo demanda

A1 acrónimos, A2/A3 glosarios, A4 variante mejorada (árboles tuneados + features extra de sentimiento &mdash; estabiliza XLE pero no rompe el techo AUC = 0.50), A5 definiciones detalladas de métricas. Subir sólo si la pregunta lo pide.

---

## Reloj objetivo

| Bloque | Slides | Objetivo |
|---|---|---|
| Portada + agenda | 1&ndash;2 | 20 s |
| Setup (motivación, hipótesis, related work) | 3&ndash;5 | 75 s |
| Metodología (pipeline, datos, indicadores, sectores, FinBERT) | 6&ndash;10 | 80 s |
| EDA + diseño experimental + entrenamiento | 11&ndash;14 | 50 s |
| **Resultados + ROC/confusión + uplift + importancia + hipótesis** | 15&ndash;20 | **170 s** |
| **Interpretación honesta + literatura** | 21&ndash;22 | **75 s** |
| Demo en vivo | 23 | 20 s |
| **Discusión + limitaciones + trading + conclusiones** | 24&ndash;27 | **135 s** |
| Trabajo futuro + refs + gracias | 28&ndash;30 | 25 s |
| **Total** | | **~10 min** |

Los bloques de resultados y conclusiones suman ~6.5 minutos &mdash; aproximadamente dos tercios de la charla, como se pidió.
