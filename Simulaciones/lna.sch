<QucsStudio Schematic 5.8>
<Properties>
View=-666.088,-841.496,2545.68,446.919,0.538631,0,0
Grid=10,10,1
DataSet=*.dat
DataDisplay=*.dpl
OpenDisplay=1
showFrame=0
FrameText0=Title \n @PATH@@FILE@
FrameText1=Drawn By:
FrameText2=Date: @DATE@
FrameText3=Revision:
</Properties>
<Symbol>
</Symbol>
<Components>
.SP SP1 1 60 40 0 9 0 "lin"1"0.01 GHz"1"1 GHz"1"991"1"no"0"1"0"2"0"none"0
Pac P2 1 630 270 18 -26 0 "2"1"50 Ω"1"0 dBm"0"1 GHz"0"26.85"0"con_2"0
GND * 1 630 300 0 0 0
Pac P1 1 -190 260 18 -26 0 "1"1"50 Ω"1"0 dBm"0"1 GHz"0"26.85"0"con_2"0
GND * 1 -190 290 0 0 0
SPfile X1 1 220 190 -26 -40 0 "D:/Proyecto-CUBESAT-TRANSPODER-VHF-UHF/Librerias/mini-circuit/PSA-5454+/PSA-5454+_S2P/PSA-5454+_S-PAR_5V_20mA_25C_UNIT1.S2P"0"2"0"polar"0"linear"0"open"0"none"0"block"0"SOT23"0
GND * 1 220 260 0 0 0
GND * 1 30 310 0 0 0
C C6 1 30 260 -94 10 3 "12 pF"1"0"0""0"neutral"0"SMD0603"0
GND * 1 350 320 0 0 0
C C1 1 120 190 -26 17 0 "1 nF"1"0"0""0"neutral"0"SMD0603"0
C C7 1 530 190 -26 17 0 "1 nF"1"0"0""0"neutral"0"SMD0603"0
L L1 1 -70 190 -26 10 0 "51 nH"1"0"0""0"inductor_1mH"0
C C5 1 350 260 -85 19 3 "7.5 pF"1"0"0""0"neutral"0"SMD0603"0
L L2 1 420 190 -26 10 0 "36 nH"1"0"0""0"inductor_1mH"0
</Components>
<Wires>
220 220 220 260
-190 190 -190 230
-190 190 -100 190
30 190 30 230
30 290 30 310
-40 190 30 190
250 190 350 190
350 190 390 190
350 190 350 230
350 290 350 320
560 190 630 190
630 190 630 240
450 190 500 190
150 190 190 190
30 190 90 190
</Wires>
<Diagrams>
<Rect 778 346 652 606 31 #c0c0c0 1 00 1 0 1e+08 1e+09 1 -45.9143 10 30 1 -1 0.5 1 -1 -1 -1 "" "" "">
	<Legend 10 -100 0>
	<"dB(S[1,1])" "" #0000ff 2 3 0 0 0 1 "">
	  <Mkr 1.46e+08 72 -456 3 1 0 0 0 50>
	<"dB(S[1,2])" "" #00dcdc 2 3 0 0 0 1 "">
	  <Mkr 1.46e+08 272 -236 3 1 0 0 0 50>
	<"dB(S[2,1])" "" #ff0000 2 3 0 0 0 1 "">
	  <Mkr 1.46e+08 202 -596 3 1 0 0 0 50>
	<"dB(S[2,2])" "" #00dc00 2 3 0 0 0 1 "">
	  <Mkr 1.46e+08 82 -326 3 1 0 0 0 50>
</Rect>
<Rect 1527 344 755 606 31 #c0c0c0 1 00 1 0 1e+08 1e+09 1 20 10 110 1 -1 0.2 1 -1 -1 -1 "" "" "">
	<Legend 10 -100 0>
	<"stoz(S[1,1])" "" #0000ff 2 3 0 0 0 1 "">
	  <Mkr 1.46e+08 63 -224 3 1 0 0 0 50>
	<"stoz(S[2,2])" "" #ff0000 2 3 0 0 0 1 "">
	  <Mkr 1.45e+08 123 -64 3 1 0 0 0 50>
</Rect>
</Diagrams>
<Paintings>
Text 2395 -219 16 #000000 0 # ==================================================================== \n # DESARROLLO TEORICO: ADAPTACION SIMULTANEA CONJUGADA BILATERAL (S12) \n # Proyecto: LNA PSA5454 @ 146 MHz \n # ==================================================================== \n  \n # 1. DEFINICION DE LA FRECUENCIA DE DISEÑO \n F_sim = 146e6 \n W_sim = 2 * pi * F_sim \n  \n # 2. CALCULO DEL DETERMINANTE (DELTA) Y FACTORES DE ESTABILIDAD MATRICIAL \n # Reflejan analiticamente la interaccion del aislamiento inverso S12 \n Delta = S[1,1]*S[2,2] - S[1,2]*S[2,1] \n B1 = 1 + abs(S[1,1])^2 - abs(S[2,2])^2 - abs(Delta)^2 \n B2 = 1 + abs(S[2,2])^2 - abs(S[1,1])^2 - abs(Delta)^2 \n C1 = S[1,1] - Delta*conj(S[2,2]) \n C2 = S[2,2] - Delta*conj(S[1,1]) \n  \n # 3. COEFICIENTES DE REFLEXION OPTIMOS SIMULTANEOS \n # Solucion de las ecuaciones cuadraticas conjugadas bilaterales \n Gms = (B1 - sqrt(B1^2 - 4*abs(C1)^2)) / (2*C1) \n Gml = (B2 - sqrt(B2^2 - 4*abs(C2)^2)) / (2*C2) \n  \n # 4. IMPEDANCIAS COMPLEJAS OBJETIVO QUE DEBEN VER LOS PUERTOS DEL CHIP \n Z_source_opt = 50 * (1 + Gms) / (1 - Gms) \n Z_load_opt = 50 * (1 + Gml) / (1 - Gml) \n  \n # 5. RED DE ENTRADA (Topologia: L1 Serie -> C6 Paralelo a Masa) \n # Transforma los 50 ohms de la antena a Z_source_opt \n G_so = real(1 / Z_source_opt) \n B_so = imag(1 / Z_source_opt) \n L1_calc = sqrt(50 / G_so - 2500) / W_sim \n C6_calc = (B_so + (W_sim * L1_calc * G_so) / 50) / W_sim \n  \n # 6. RED DE SALIDA (Topologia: C5 Paralelo a Masa -> L2 Serie) \n # Transforma la salida del chip a los 50 ohms de la etapa BJT \n G_lo = real(1 / Z_load_opt) \n B_lo = imag(1 / Z_load_opt) \n L2_calc = sqrt(50 / G_lo - 2500) / W_sim \n C5_calc = (B_lo + (W_sim * L2_calc * G_lo) / 50) / W_sim \n  \n # ==================================================================== \n # COMENTARIOS DE REFERENCIA - RESULTADOS EVALUADOS A 146 MHz: \n # ==================================================================== \n # Impedancia Entrada Target: Z_source_opt = 91.3 - j10.5 Ohm \n # Impedancia Salida Target:  Z_load_opt   = 72.5 + j31.1 Ohm \n # \n # VALORES CALCULADOS FINALES ASIGNADOS AUTOMATICAMENTE: \n # -> L1_calc = ~49.5 nH  (Inductor de Entrada Serie) \n # -> C6_calc = ~12.0 pF  (Capacitor de Entrada Paralelo a Masa) \n # -> C5_calc = ~7.7 pF   (Capacitor de Salida Paralelo a Masa) \n # -> L2_calc = ~36.6 nH  (Inductor de Salida Serie) \n # ====================================================================
</Paintings>
