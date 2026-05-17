import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# PARÁMETROS DEL SISTEMA
# =============================================================================
F_SIG = 146.0      
BW_SIG = 0.1       
F_LO = 580.0       

PWR_IN = 0.0           
LO_DRIVE = 8.0         
CONV_LOSS = 6.6        
ISOLATION_LR = 40.0    
ISOLATION_IF_RF = 35.0 

PWR_LO_LEAK = LO_DRIVE - ISOLATION_LR         
PWR_LSB = PWR_IN - CONV_LOSS                  
PWR_USB = PWR_IN - CONV_LOSS                  
PWR_RF_LEAK = PWR_IN - ISOLATION_IF_RF        
PWR_3RD_HARM = PWR_LSB - 40.0                 

NOISE_FLOOR = -115.0   
RBW = 1.0              

# =============================================================================
# FUNCIONES MATEMÁTICAS (ESPECTRO)
# =============================================================================
def add_modulated_signal(f_array, f_center, bw, peak_dbm):
    peak_lin = 10**(peak_dbm / 10.0)
    shape_lin = peak_lin * (np.sinc((f_array - f_center) / (bw / 1.5)))**2
    return shape_lin

def add_cw_tone(f_array, f_center, peak_dbm, rbw):
    peak_lin = 10**(peak_dbm / 10.0)
    shape_lin = peak_lin * np.exp(-0.5 * ((f_array - f_center) / (rbw / 3.0))**2)
    return shape_lin

# =============================================================================
# GENERACIÓN DEL ESPECTRO
# =============================================================================
f_span = np.linspace(50, 800, 200000)
spectrum_lin = np.full_like(f_span, 10**(NOISE_FLOOR / 10.0))

spectrum_lin += add_modulated_signal(f_span, F_SIG, BW_SIG, PWR_RF_LEAK)
spectrum_lin += add_cw_tone(f_span, F_LO, PWR_LO_LEAK, RBW)

f_lsb = F_LO - F_SIG
spectrum_lin += add_modulated_signal(f_span, f_lsb, BW_SIG, PWR_LSB)

f_usb = F_LO + F_SIG
spectrum_lin += add_modulated_signal(f_span, f_usb, BW_SIG, PWR_USB)

f_3rd_harm = 3 * F_SIG
spectrum_lin += add_modulated_signal(f_span, f_3rd_harm, BW_SIG * 3, PWR_3RD_HARM)

spectrum_dbm = 10 * np.log10(spectrum_lin)

# =============================================================================
# MODELADO DEL FILTRO CON COMPONENTES FÍSICOS (Matrices ABCD)
# =============================================================================
# Valores físicos de tu esquemático
C1 = 10e-12  # C27: 10 pF
L2 = 27e-9    # L6: 27 nH
C3 = 16e-12   # C28: 11 pF
L4 = 27e-9    # L7: 27 nH
C5 = 10e-12  # C29: 10 pF
Z0 = 50.0     # Impedancia del sistema

w = 2 * np.pi * f_span * 1e6 # Frecuencia angular en rad/s

# Inicializamos la matriz ABCD global como una matriz Identidad
A = np.ones_like(w, dtype=complex)
B = np.zeros_like(w, dtype=complex)
C = np.zeros_like(w, dtype=complex)
D = np.ones_like(w, dtype=complex)

# Función para multiplicar matrices ABCD iterativamente
def cascade(A1, B1, C1, D1, A2, B2, C2, D2):
    A_out = A1*A2 + B1*C2
    B_out = A1*B2 + B1*D2
    C_out = C1*A2 + D1*C2
    D_out = C1*B2 + D1*D2
    return A_out, B_out, C_out, D_out

# 1. Shunt C27
A, B, C, D = cascade(A, B, C, D, 1, 0, 1j*w*C1, 1)
# 2. Serie L6
A, B, C, D = cascade(A, B, C, D, 1, 1j*w*L2, 0, 1)
# 3. Shunt C28
A, B, C, D = cascade(A, B, C, D, 1, 0, 1j*w*C3, 1)
# 4. Serie L7
A, B, C, D = cascade(A, B, C, D, 1, 1j*w*L4, 0, 1)
# 5. Shunt C29
A, B, C, D = cascade(A, B, C, D, 1, 0, 1j*w*C5, 1)

# Calcular S21 a partir de los parámetros ABCD finales
S21 = 2 / (A + B/Z0 + C*Z0 + D)
filter_response = 20 * np.log10(np.abs(S21))

# Recortamos a -80 dB para visualización
filter_response = np.clip(filter_response, a_min=-80.0, a_max=0.0)

# =============================================================================
# GRAFICACIÓN
# =============================================================================
fig, ax1 = plt.subplots(figsize=(14, 7))

ax1.plot(f_span, spectrum_dbm, color='blue', linewidth=1.5, label='Espectro Real del Mixer')
ax1.set_xlabel('Frecuencia (MHz)', fontsize=12)
ax1.set_ylabel('Potencia (dBm)', fontsize=12, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(NOISE_FLOOR - 5, 5)
ax1.set_xlim(50, 800)

# Graficamos la respuesta de los componentes reales
ax1.plot(f_span, filter_response, color='red', linestyle='-', linewidth=2, label='Respuesta L-C Físicos')
ax1.fill_between(f_span, NOISE_FLOOR - 5, filter_response, color='red', alpha=0.1)

ax1.axvline(F_SIG, color='gray', linestyle='--', alpha=0.6)
ax1.text(F_SIG, -5, f'VHF Fuga\n({F_SIG} MHz)', rotation=90, va='top', ha='right', fontsize=9)

ax1.axvline(f_lsb, color='green', linestyle='-', alpha=0.6)
ax1.text(f_lsb, 2, f'LSB (Deseada)\n({f_lsb} MHz)', rotation=90, va='bottom', ha='center', fontsize=9, color='green')

ax1.axvline(F_LO, color='red', linestyle='--', alpha=0.6)
ax1.text(F_LO, -15, f'LO Fuga\n({F_LO} MHz)', rotation=90, va='top', ha='right', fontsize=9, color='red')

ax1.axvline(f_usb, color='orange', linestyle='--', alpha=0.6)
ax1.text(f_usb, -10, f'USB\n({f_usb} MHz)', rotation=90, va='top', ha='right', fontsize=9)

ax1.grid(True, which='both', linestyle='--', alpha=0.5)
ax1.minorticks_on()

lines, labels = ax1.get_legend_handles_labels()
ax1.legend(lines, labels, loc='upper right')
plt.tight_layout()
plt.show()