# Listado de variables, listas, diccionarios y funciones

Este documento resume los elementos principales del sistema y a que parte del proyecto pertenecen.

## 1. Listas

| Elemento | Archivo | Pertenece a | Uso |
|---|---|---|---|
| `centrales` | `m01_servidores.py` | Metodologia / sistema | centrales monitoreadas |
| `agentes_norte` | `m01_servidores.py` | Metodologia | usuarios autorizados norte |
| `agentes_centro` | `m01_servidores.py` | Metodologia | usuarios autorizados centro |
| `agentes_sur` | `m01_servidores.py` | Metodologia | usuarios autorizados sur |
| `agentes_autorizados` | `m01_servidores.py` | Fundamentos | validar usuario permitido |
| `usuarios_sospechosos` | `m01_servidores.py` | Fundamentos / ciberseguridad | simular accesos no autorizados |
| `ips_internas` | `m01_servidores.py` | Metodologia | origen normal de paquetes |
| `ips_sospechosas` | `m01_servidores.py` | Fundamentos | origen de ataques |
| `tipos_expediente` | `m01_servidores.py` | Metodologia | tipo de registro simulado |
| `TIPOS_ATAQUE` | `m03_atacante.py` | Fundamentos | clasificar incidentes simulados |
| `historial` | `m00_pdi_slp.py` | Todas las materias | guardar cada segundo para graficas y CSV |
| `ips_bloqueadas` | `m00_pdi_slp.py` | Fundamentos | registrar IPs bloqueadas |
| `alertas` | `m04_logica_matematica.py` | Fundamentos | mensajes de riesgo |
| `protecciones` | `m04_logica_matematica.py` | Fundamentos | acciones defensivas |
| `t`, `paquetes`, `intentos`, `flujo` | `m06_graficas.py` | Algebra / Calculo | listas para graficar |
| `temperatura`, `temperatura_sin_enfriamiento` | `m06_graficas.py` | Fisica | graficar temperatura |

## 2. Diccionarios

| Diccionario | Archivo | Pertenece a | Claves principales |
|---|---|---|---|
| `estado_actual` | `m00_pdi_slp.py` | Metodologia / Fundamentos | `estado`, `estado_arrastrado`, `cifrado`, `refrigeracion`, `login_bloqueado`, `ips_bloqueadas`, `historial` |
| `estado_calculo` | `m04_logica_matematica.py` | Calculo | `paquetes_anteriores`, `temperatura_anterior`, `cpu_anterior`, `primera_derivada_sigmoide_anterior` |
| `paquete` | `m02_trafico_normal.py` | Todas las materias | `segundo`, `central`, `usuario`, `ip`, `paquetes`, `intentos_login`, `cambios_archivos`, `salida_datos`, `cpu`, `temperatura`, `incidente` |
| `metricas_calculo` | `m04_logica_matematica.py` | Calculo | `tasa`, `primera_derivada_sigmoide`, `segunda_derivada_sigmoide`, `primera_derivada_paquetes` |
| `fila_reporte` | `m07_reporte_tabla.py` | Metodologia | datos por columna para CSV |

## 3. Variables numericas principales

| Variable | Pertenece a | Uso |
|---|---|---|
| `segundo` | Metodologia / Calculo | contador de ciclo |
| `prob` | Metodologia | probabilidad de ataque por tramo |
| `tasa` | Calculo | cambio de paquetes |
| `flujo` | Algebra | indice ponderado |
| `senal` | Algebra / Trigonometria | patron esperado |
| `indice_oscilatorio` | Algebra / Fundamentos | desviacion del patron |
| `cpu` | Fisica | carga de procesador |
| `potencia_cpu_watts` | Fisica | watts de CPU |
| `temperatura` | Fisica | temperatura final |
| `temperatura_sin_enfriamiento` | Fisica | temperatura antes de enfriar |
| `velocidad_ventilador` | Fisica | velocidad del aire |
| `velocidad_refrigerante` | Fisica | velocidad del fluido |
| `P1`, `P2` | Fisica | presion de entrada y salida |
| `consumo_total_watts` | Fisica | consumo total del segundo |

## 4. Constantes y umbrales

| Constante | Archivo | Pertenece a | Uso |
|---|---|---|---|
| `U_PAQUETES_SOSP` | `m01_servidores.py` | Fundamentos | trafico sospechoso |
| `U_PAQUETES_ALERTA` | `m01_servidores.py` | Fundamentos | alerta de trafico |
| `U_PAQUETES_CRIT` | `m01_servidores.py` | Fundamentos | trafico critico |
| `U_LOGIN_ALERTA` | `m01_servidores.py` | Fundamentos | login en alerta |
| `U_LOGIN_CRIT` | `m01_servidores.py` | Fundamentos | login critico |
| `U_FLUJO_ELEVADO`, `U_FLUJO_RIESGO`, `U_FLUJO_CRITICO` | `m01_servidores.py` | Algebra / Fundamentos | umbrales de flujo |
| `U_TASA` | `m01_servidores.py` | Calculo | umbral de cambio |
| `U_OSCILACION_SOSP`, `U_OSCILACION_CRIT` | `m01_servidores.py` | Algebra / Fundamentos | desviacion periodica |
| `U_TEMP_REFRIG`, `U_TEMP_CRITICA` | `m01_servidores.py` | Fisica | umbrales termicos |
| `CLAVE_CESAR` | `m04_logica_matematica.py` | Fundamentos | desplazamiento Cesar |
| `CLAVE_MULTIPLICATIVA_LETRAS` | `m04_logica_matematica.py` | Fundamentos | cifrado multiplicativo letras |
| `AREA_VENTILACION` | `m04_logica_matematica.py` | Fisica | velocidad del ventilador |
| `P1_REFRIGERANTE`, `RHO_REFRIGERANTE` | `m04_logica_matematica.py` | Fisica | Bernoulli |

## 5. Funciones por archivo

| Funcion | Archivo | Pertenece a | Uso |
|---|---|---|---|
| `generar_trafico_normal` | `m02_trafico_normal.py` | Metodologia | crea el paquete base |
| `inyectar_ataque` | `m03_atacante.py` | Fundamentos | altera el paquete con incidente |
| `crear_estado_calculo` | `m04_logica_matematica.py` | Calculo | guarda valores anteriores |
| `calcular_metricas_calculo` | `m04_logica_matematica.py` | Calculo | tasa, derivadas y segunda derivada |
| `calcular_tasa` | `m04_logica_matematica.py` | Calculo | cambio actual-anterior |
| `calcular_derivada_discreta` | `m04_logica_matematica.py` | Calculo | derivada por segundo |
| `calcular_sigmoide` | `m04_logica_matematica.py` | Calculo | suavizar valores |
| `aplicar_sigmoide_derivada` | `m04_logica_matematica.py` | Calculo | derivada ajustada |
| `calcular_flujo_digital` | `m04_logica_matematica.py` | Algebra | combinacion ponderada |
| `senal_periodica` | `m04_logica_matematica.py` | Algebra / Trigonometria | onda esperada |
| `calcular_analisis_oscilatorio` | `m04_logica_matematica.py` | Algebra | desviacion contra senal |
| `evaluar_estado` | `m04_logica_matematica.py` | Fundamentos | reglas logicas y protecciones |
| `cifrado_cesar` | `m04_logica_matematica.py` | Fundamentos | cifrado basico |
| `cifrado_multiplicativo` | `m04_logica_matematica.py` | Fundamentos | cifrado modular |
| `cifrado_reforzado` | `m04_logica_matematica.py` | Fundamentos | Cesar + multiplicativo |
| `generar_direccion_registro` | `m04_logica_matematica.py` | Fundamentos | ruta normal/cifrada |
| `descifrar_direccion_registro` | `m04_logica_matematica.py` | Fundamentos | servidor descifrado |
| `calcular_cpu_temperatura` | `m04_logica_matematica.py` | Fisica | CPU, watts y temperatura |
| `calcular_ventilador` | `m04_logica_matematica.py` | Fisica | velocidad y descenso por ventilacion |
| `calcular_refrigeracion` | `m04_logica_matematica.py` | Fisica | fluido y Bernoulli critico |
| `calcular_consumo_watts` | `m04_logica_matematica.py` | Fisica | consumo total |
| `imprimir_inicio` | `m05_monitor.py` | Metodologia | pantalla inicial |
| `imprimir_ciclo` | `m05_monitor.py` | Metodologia | salida por segundo |
| `imprimir_panel` | `m05_monitor.py` | Metodologia | salida cada 5 segundos |
| `imprimir_resumen` | `m05_monitor.py` | Metodologia | reporte final en consola |
| `generar_graficas` | `m06_graficas.py` | Todas las materias | genera PNG |
| `generar_reporte_tabla` | `m07_reporte_tabla.py` | Metodologia | genera CSV |

## 6. Vinculacion por materia

| Materia | Datos de entrada | Transformacion | Salida |
|---|---|---|---|
| Metodologia | input, paquete, listas y diccionarios | ciclos, condicionales, llamadas a funciones | consola, historial, CSV |
| Fundamentos | usuario, IP, flujo, estado, ruta | reglas logicas y cifrado | estado, protecciones, ruta cifrada |
| Algebra | paquetes, login, cambios, salida, tiempo | flujo digital y senal periodica | flujo, indice oscilatorio, graficas 01, 05, 07 |
| Calculo | valores actuales y anteriores | tasa, derivadas, sigmoide | grafica 06, alertas de cambio |
| Fisica | flujo, CPU, temperatura, estado | potencia, ventilador, refrigeracion, Bernoulli | temperatura final, consumo, grafica 03 |
