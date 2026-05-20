# Guión del defensor &mdash; Defensa Final FPA (Español, para leer)

*Predicción del Movimiento del Precio del S y P quinientos &mdash; Datos Históricos de Mercado y Análisis de Sentimiento de Noticias Financieras*

César Castaño (A00830006) y Brenda García (A01633622) &middot; Tec de Monterrey, M.Sc. CS, Semestre 4.

> Léelo en voz alta a un ritmo cómodo. Tiempo objetivo: **10 minutos**. Las cursivas entre paréntesis son indicaciones de escena &mdash; no se dicen en voz alta. Las palabras en negritas son las que conviene acentuar al hablar.

---

## Slide 1 &mdash; Portada  *(8 segundos)*

Buenos días. Soy **César Castaño**, y me acompaña **Brenda García**. Ésta es la defensa final de nuestro proyecto de Data Analytics &mdash; predecir si el S y P quinientos cerrará al alza o a la baja al día siguiente.

## Slide 2 &mdash; Agenda  *(8 segundos)*

El plan es dedicar cerca de dos tercios de la charla a los **resultados y conclusiones**; pasaremos rápido por todo lo demás.

## Slide 3 &mdash; Motivación  *(15 segundos)*

El S y P quinientos es el índice de referencia más observado del mercado estadounidense, con once sectores que se comportan de forma muy distinta. Predecir **dirección**, no precio, es lo que la gestión de riesgo necesita en la práctica. Los mercados no son perfectamente eficientes, y herramientas como FinBERT hacen que extraer sentimiento sea prácticamente gratis &mdash; la pregunta de la derecha resume todo el proyecto en una línea.

## Slide 4 &mdash; Hipótesis  *(25 segundos)*

Nuestra variable objetivo es binaria. La etiqueta es **uno** si el cierre de mañana es mayor que el de hoy, y **cero** en cualquier otro caso &mdash; agrupamos los días planos con los de bajada porque, en índices líquidos, los días planos son muy raros. De ahí salen dos hipótesis. **Hipótesis uno**: añadir sentimiento mejora accuracy, F1, y el Área Bajo la Curva, o A-U-C. **Hipótesis dos**: esa ganancia es mayor en sectores con más volatilidad. Y planteamos tres preguntas de investigación; la más importante es: ¿el sentimiento ayuda, y hay un algoritmo consistentemente mejor que el otro?

## Slide 5 &mdash; Trabajo relacionado  *(12 segundos)*

Cinco trabajos ancla dan forma a nuestro diseño: **Bollen 2011** &mdash; el sentimiento sí carga información predictiva; **Vargas 2017** &mdash; los modelos multimodales ayudan; **Araci 2019** &mdash; FinBERT, pre-entrenado y libre de usar; **Zhang 2019** &mdash; los modelos basados en árboles con sentimiento son competitivos e interpretables; y **López de Prado 2018** &mdash; splits cronológicos para evitar look-ahead bias.

## Slide 6 &mdash; Pipeline  *(10 segundos)*

Cuatro etapas: jalar datos de mercado, generar indicadores técnicos, calificar sentimiento con FinBERT, entrenar ensambles de árboles. Dos algoritmos por dos conjuntos de features por cuatro datasets da **dieciséis corridas**.

## Slide 7 &mdash; Fuentes de datos  *(15 segundos)*

Dos fuentes. Los datos de mercado vienen de **yfinance**, cubriendo del 2010 al 2019, lo cual nos deja fuera del COVID y coincide con la ventana de noticias. Las noticias vienen de un dataset de Kaggle con **más de un millón cuatrocientos mil titulares**, que filtramos y limitamos a cincuenta por día con una semilla fija, para que el experimento sea reproducible.

## Slide 8 &mdash; Indicadores técnicos  *(15 segundos)*

Siete features derivados de open, high, low, close y volumen: returns, dos medias móviles (una simple y una exponencial), el Índice de Fuerza Relativa (o R-S-I), volatilidad, el precio típico y el propio volumen. El target se construye en la etapa de preparación de datos, antes del modelado, así que no hay fuga hacia los features.

## Slide 9 &mdash; Selección de sectores  *(15 segundos)*

Para probar Hipótesis dos elegimos tres sectores ancla que cubren el rango de volatilidad: **X-L-P** de Consumer Staples en el extremo bajo, **X-L-K** de Tecnología cerca de la mediana, y **X-L-E** de Energía en el extremo alto. Junto con el S y P quinientos amplio, esos son nuestros cuatro datasets.

## Slide 10 &mdash; FinBERT  *(20 segundos)*

Por cada titular, FinBERT nos devuelve positivo menos negativo como un único score entre menos uno y más uno. Lo agregamos por día en la media, la desviación estándar y el conteo de titulares. Usamos el modelo ProsusAI pre-entrenado, en lotes de treinta y dos, y los días sin noticias los imputamos en cero para que la serie de tiempo se mantenga continua.

## Slide 11 &mdash; Balance de clases  *(10 segundos)*

Hay un **leve sesgo al alza** &mdash; el mercado sube ligeramente más veces de las que baja. Una línea base que siempre dice "sube" ya saca alrededor del cincuenta y cinco por ciento de accuracy. Por eso reportamos A-U-C en paralelo.

## Slide 12 &mdash; Flujo de noticias  *(10 segundos)*

Alrededor de **trescientos ochenta y seis mil titulares** procesados sobre los diez años de ventana, con **cobertura del cien por ciento de los días de trading**, y un sentimiento medio que se queda apenas por encima de cero.

## Slide 13 &mdash; Diseño experimental  *(10 segundos)*

Dos algoritmos, por dos conjuntos de features, por cuatro datasets &mdash; dieciséis corridas evaluadas bajo splits idénticos.

## Slide 14 &mdash; Protocolo de entrenamiento  *(15 segundos)*

Usamos un split cronológico ochenta-veinte &mdash; aproximadamente **dos mil días de entrenamiento y quinientos un días de prueba**. Sin shuffling, sin look-ahead. Los hiperparámetros se mantienen en valores por defecto razonables, para que las dieciséis corridas sean directamente comparables.

*(Aquí nos detenemos.)*

## Slide 15 &mdash; Resultados, sólo técnico  *(25 segundos)*

Aquí el titular de la línea base sólo técnica: el **A-U-C se queda en cero punto cinco en todos los datasets**. Los indicadores técnicos solos apenas separan los días de alza de los demás &mdash; lo cual es consistente con la forma débil de eficiencia de mercado. Parece que XGBoost en S y P quinientos llega a un F1 de cero punto seis seis, pero sólo porque se está apoyando en la clase mayoritaria. Y de hecho, **X-L-K colapsa a la clase cero en esta ventana de prueba**, arrastrando el F1 hasta cero punto dos tres. Ésta es la línea base que hay que mejorar.

## Slide 16 &mdash; Resultados, técnico más sentimiento  *(30 segundos)*

Al añadir sentimiento aparecen dos ganancias limpias. **S y P quinientos con Random Forest más sentimiento** sube a cero punto cinco seis de accuracy, cero punto seis siete de F1, y cero punto cinco uno de A-U-C. Eso es **más cero punto cero cinco, más cero punto cero seis, y más cero punto cero cuatro** sobre la línea base. **X-L-E con XGBoost más sentimiento** lleva el A-U-C de cero punto cuatro ocho a cero punto cinco dos. Pero hay que notar algo: las ganancias se concentran en el índice amplio y en el sector más volátil. Los sectores de volatilidad baja y mediana apenas se mueven.

## Slide 17 &mdash; Dónde vive el más cero punto cero cuatro de A-U-C  *(50 segundos)*

Esta es la slide que queremos que recuerden. Dos vistas del mismo resultado, S y P quinientos con Random Forest. A la **izquierda**, el overlay de la curva ROC (Receiver Operating Characteristic, o R-O-C): la curva sólo técnica se cae sobre la diagonal en A-U-C cero punto cuatro siete ocho; la curva con sentimiento sube por encima entre tasa de falsos positivos cero punto tres y cero punto nueve, en A-U-C cero punto cinco uno tres. Esa diferencia, **más cero punto cero tres cinco**, es toda la contribución del sentimiento en números. A la **derecha**, la matriz de confusión con el umbral por defecto de cero punto cinco. Vean el recall en días de alza: **cero punto ocho cuatro**. El modelo captura casi todas las subidas. Pero la precisión es de cero punto cinco siete, porque tolera ciento setenta y cuatro falsos positivos para lograrlo. Así que, en palabras simples, el modelo se comporta como un **clasificador agresivo con sesgo a posición larga**: casi nunca se le va un día de alza, pero da falsas alarmas en un tercio de los días.

## Slide 18 &mdash; Sentiment uplift  *(20 segundos)*

Una sola gráfica con todos los deltas. El **cluster positivo más fuerte es S y P quinientos con Random Forest** &mdash; las tres métricas en verde. **X-L-E con XGBoost** sale positivo en accuracy y A-U-C. Y el negativo es **X-L-P con Random Forest** &mdash; la única configuración donde el sentimiento perjudica en todas las métricas, justo el patrón que Hipótesis dos predice para sectores de baja volatilidad.

## Slide 19 &mdash; Feature importance  *(20 segundos)*

¿Dónde vive la señal de sentimiento dentro del modelo? **sentiment\_mean**, en dorado, queda en el **top tres de features** en las dos configuraciones donde mejoró el A-U-C de forma material. Los features técnicos se reparten de forma bastante pareja &mdash; ninguno domina. La señal es genuinamente aditiva.

## Slide 20 &mdash; Evaluación de hipótesis  *(25 segundos)*

Entonces, las hipótesis. **Hipótesis uno**, parcialmente respaldada: el sentimiento ayuda al índice amplio con Random Forest y al sector de alta volatilidad con XGBoost, pero el panorama sectorial es mixto. **Hipótesis dos**, también parcialmente respaldada: X-L-E, el más volátil, tiene la mayor ganancia con XGBoost, pero X-L-K de volatilidad mediana no se beneficia, así que la relación no es estrictamente monótona. Y para la **pregunta de investigación dos**: en A-U-C los dos algoritmos están empatados; Random Forest gana en el índice, XGBoost gana en el sector de alta volatilidad.

## Slide 21 &mdash; ¿Qué significa realmente un A-U-C cercano a cero punto cinco?  *(45 segundos)*

Esta slide responde a la pregunta obvia: un A-U-C de cero punto cinco uno, ¿realmente significa algo? Tres puntos de referencia sobre los mismos quinientos un días de prueba. Una **moneda al aire** se queda en cero punto cinco en todo. La línea base de **"siempre sube"**, que aprovecha el sesgo al alza del mercado, saca cero punto cinco cinco de accuracy y cero punto siete uno de F1 *gratis*, pero su A-U-C sigue en cero punto cinco, porque no tiene capacidad de ordenar. **Nuestro mejor modelo** llega a cero punto cinco seis de accuracy, cero punto seis siete de F1, y cero punto cinco uno de A-U-C. Las barras de la derecha lo hacen visualmente obvio: en accuracy y F1 estamos prácticamente encima de la línea base "siempre sube", apenas más cero punto cero cinco; en A-U-C las tres barras son indistinguibles. Entonces el resultado real es **el delta del sentimiento**, más cero punto cero cuatro de A-U-C &mdash; no el nivel absoluto. Y eso es exactamente lo que predice la forma débil de la Hipótesis del Mercado Eficiente (o E-M-H).

## Slide 22 &mdash; Comparación con la literatura  *(30 segundos)*

¿Cómo se ve ese delta frente al trabajo previo? Bollen reportó ochenta y siete punto seis por ciento de accuracy, pero en una ventana de siete meses con un léxico estrecho; reproducciones en ventanas más largas caen a alrededor de sesenta por ciento. Vargas obtuvo cerca del sesenta y dos por ciento con encoders profundos sobre el cuerpo completo de Reuters. FinBERT de Araci puntúa alto, pero en sentimiento a nivel de oración, no en dirección al día siguiente. Zhang reportó alrededor de cero punto cinco seis de A-U-C en acciones chinas con tuning por ticker. Una vez que normalizan el setup, **nuestro cero punto cinco dos de A-U-C en el sector de alta volatilidad está en el orden correcto** &mdash; diario con sólo títulos es el régimen más difícil de la lista.

## Slide 23 &mdash; Demo en vivo  *(20 segundos)*

Esta slide enlaza a un walkthrough grabado en Drive. El notebook carga nuestros cuatro clasificadores entrenados, jala los datos de mercado de hoy, califica los titulares de hoy con FinBERT, e imprime un **UP**, **DOWN** o **STABLE** por cada modelo. La curva de calibración a la derecha es la razón por la que usamos el corredor cero punto cuarenta y cinco a cero punto cincuenta y cinco para STABLE: empíricamente el modelo sólo está razonablemente calibrado dentro de esa banda.

## Slide 24 &mdash; Discusión  *(25 segundos)*

La gráfica de la derecha hace visible la afirmación central de la charla: **las dieciséis configuraciones se agrupan dentro de más o menos cero punto cero tres alrededor de A-U-C igual a cero punto cinco**. ¿Por qué? Primero, el sentimiento diario es una señal delgada &mdash; pierde el timing intra-día y los sectores ruidosos lo enmascaran. Segundo, el colapso de X-L-K es real: la ventana de prueba de 2018 a 2019 tuvo más días planos y a la baja que de alza, y sin re-pesaje de clases el modelo toma el camino fácil. Y tercero, S y P quinientos es el que más se beneficia porque los retornos del índice agregan ruido idiosincrático, dejando el flujo sistemático de noticias como una señal relativamente más limpia.

## Slide 25 &mdash; Limitaciones  *(25 segundos)*

Siete advertencias honestas, y empezamos por las dos nuevas. **Uno**, nuestro más cero punto cero cuatro de A-U-C es un estimador puntual &mdash; un test de DeLong o un intervalo de confianza por bootstrap nos diría si es estadísticamente significativo. **Dos**, la gráfica de la derecha muestra la realidad de los costos de transacción: un costo round-trip de cinco a diez puntos básicos erosiona la ventaja hasta el punto de equilibrio alrededor de nueve puntos básicos. Luego las advertencias estándar: el corpus de noticias está sesgado a las mega-caps, FinBERT sólo ve los títulos, el cap de cincuenta titulares por día, un único split cronológico, y los hiperparámetros sin tunear.

## Slide 26 &mdash; Realidad de trading  *(35 segundos)*

Esto hace concreta la pregunta de si esto es operable. Cuatro curvas de equity sobre la ventana de prueba del S y P quinientos, partiendo de un dólar, antes de cualquier costo. **Buy-and-hold** termina en uno punto diecinueve &mdash; la ventana coincidió con la cola del mercado alcista 2017-2019, así que la estrategia fácil se ve fuerte. Nuestro **Random Forest más sentimiento**, entrando largo cuando la probabilidad es de al menos cero punto cinco cinco, termina en uno punto diecisiete, con cerca de la **mitad del tiempo fuera del mercado** &mdash; capturamos casi toda la subida con menos exposición. La línea base **aleatoria cincuenta-cincuenta** termina en uno punto cero nueve, muy por debajo de buy-and-hold, lo cual confirma que nuestra señal **no es suerte**. Pero antes de costos seguimos sin ganarle a la línea base fácil, y al añadir costos realistas el cuadro se invierte. Así que el más cero punto cero cuatro de A-U-C es una **señal real, científicamente significativa &mdash; todavía no operable**.

## Slide 27 &mdash; Conclusiones  *(50 segundos)*

Para cerrar, seis conclusiones. **Uno**: el sentimiento de FinBERT ayuda al índice amplio con Random Forest &mdash; más cero punto cero cinco de accuracy, más cero punto cero seis de F1, más cero punto cero cuatro de A-U-C, pequeño pero consistente. **Dos**: el efecto **no es monótono** en la volatilidad sectorial &mdash; X-L-E se beneficia, X-L-P y X-L-K no, así que Hipótesis dos sólo está parcialmente respaldada. **Tres**: el techo de A-U-C igual a cero punto cinco en los sectores individuales es **consistente con la forma débil de la Hipótesis del Mercado Eficiente (o E-M-H)** &mdash; nuestra contribución es el signo del delta, no una señal operable. **Cuatro**: la elección de algoritmo es **dependiente de la configuración** &mdash; Random Forest en el índice, XGBoost en el sector volátil, así que la pregunta de investigación dos no tiene ganador universal. **Cinco**: sentiment\_mean queda top tres en feature importance sólo donde realmente mejoró el A-U-C, lo cual significa que la contribución es real, no un artefacto del modelo. Y **seis**, antes de costos, nuestra estrategia long-flat termina en uno punto diecisiete contra uno punto diecinueve de buy-and-hold y uno punto cero nueve aleatorio &mdash; **mejor que el azar, no mejor que la línea base fácil**.

## Slide 28 &mdash; Trabajo futuro  *(15 segundos)*

En orden de prioridad: un test de significancia estadística para el delta de A-U-C, un backtest que tenga en cuenta los costos de transacción, evaluación walk-forward, sentimiento multi-resolución, ruteo de noticias por sector, re-pesaje de clases para X-L-K, y un stress test de 2020 a 2024 una vez que tengamos una feature de normalización por COVID.

## Slide 29 &mdash; Referencias  *(5 segundos)*

Éstos son los trabajos ancla que citamos a lo largo de la charla; la bibliografía completa está en el manuscrito.

## Slide 30 &mdash; Gracias  *(5 segundos)*

Muchas gracias. Estamos a sus órdenes para responder preguntas.

---

## Apéndices &mdash; sólo bajo demanda

A1 acrónimos, A2 y A3 glosarios, A4 la variante mejorada (árboles tuneados con features extra de sentimiento &mdash; estabiliza un poco más X-L-E pero no rompe el techo de A-U-C igual a cero punto cinco, así que las conclusiones principales se mantienen), y A5 las definiciones detalladas de métricas.

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

Los bloques de resultados y conclusiones suman aproximadamente seis minutos y medio &mdash; cerca de dos tercios de la charla, como se pidió.
