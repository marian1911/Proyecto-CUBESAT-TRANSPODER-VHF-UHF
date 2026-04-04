import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# PARÁMETROS DEL SISTEMA (Basados en datasheet real)
# =============================================================================
F_SIG = 146.0      # Frecuencia de entrada VHF
BW_SIG = 0.1       
F_LO = 580.0       # Frecuencia del Oscilador Local

# Potencias y parámetros del Mixer (LO = +7 dBm)
PWR_IN = 0.0           # Potencia de tu señal VHF entrando al mixer (Asumimos 0 dBm)
LO_DRIVE = 7.0         # Potencia inyectada en el puerto LO
CONV_LOSS = 6.6        # Conversion Loss típico a ~580 MHz
ISOLATION_LR = 40.0    # Aislación LO a RF (L-R) a ~580 MHz
ISOLATION_IF_RF = 35.0 # Aislación estimada de la entrada a la salida (IF-R)

# Cálculos de potencia a la salida del Mixer
PWR_LO_LEAK = LO_DRIVE - ISOLATION_LR         # Fuga del LO = -33.0 dBm
PWR_LSB = PWR_IN - CONV_LOSS                  # Señal útil LSB = -6.6 dBm
PWR_USB = PWR_IN - CONV_LOSS                  # Señal USB = -6.6 dBm
PWR_RF_LEAK = PWR_IN - ISOLATION_IF_RF        # Fuga de entrada = -35.0 dBm
PWR_3RD_HARM = PWR_LSB - 40.0                 # Estimación del 3er armónico

NOISE_FLOOR = -110.0   
RBW = 1.0              

# =============================================================================
# FUNCIONES MATEMÁTICAS
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
# MODELADO DEL FILTRO SAW (Filtro 3 - Mejor Opción)
# =============================================================================
filter_response = np.full_like(f_span, -80.0)

filter_response[(f_span >= 10) & (f_span < 380)] = -(60 + 2)
filter_response[(f_span >= 380) & (f_span < 414)] = -(56 + 2)
filter_response[(f_span >= 414) & (f_span < 427)] = -(52 + 2)
filter_response[(f_span >= 427) & (f_span < 431.52)] = -(29 + 2)
filter_response[(f_span >= 431.52) & (f_span < 432.9)] = -(20 + 2)
filter_response[(f_span >= 432.9) & (f_span < 433.1)] = -(20 + 2)

# Passband: 433.1 a 435.1 MHz
filter_response[(f_span >= 433.1) & (f_span <= 435.1)] = -2.0

filter_response[(f_span > 435.1) & (f_span < 444.5)] = -(30 + 2)
filter_response[(f_span >= 444.5) & (f_span < 450)] = -(45 + 2)
filter_response[(f_span >= 450) & (f_span <= 800)] = -(52 + 2)

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

ax1.plot(f_span, filter_response, color='red', linestyle='-', linewidth=2, label='Respuesta Filtro SAW ')
ax1.fill_between(f_span, NOISE_FLOOR - 5, filter_response, color='red', alpha=0.1)

ax1.axvline(F_SIG, color='gray', linestyle='--', alpha=0.6)
ax1.text(F_SIG, -5, f'VHF Fuga\n({F_SIG} MHz)', rotation=90, va='top', ha='right', fontsize=9)

ax1.axvline(f_lsb, color='green', linestyle='-', alpha=0.6)
ax1.text(f_lsb, 2, f'LSB\n({f_lsb} MHz)\n{PWR_LSB:.1f} dBm', rotation=90, va='bottom', ha='center', fontsize=9, color='green')

ax1.axvline(F_LO, color='red', linestyle='--', alpha=0.6)
ax1.text(F_LO, -15, f'LO Fuga\n({F_LO} MHz)\n{PWR_LO_LEAK:.1f} dBm', rotation=90, va='top', ha='right', fontsize=9, color='red')

ax1.axvline(f_usb, color='orange', linestyle='--', alpha=0.6)
ax1.text(f_usb, -10, f'USB\n({f_usb} MHz)\n{PWR_USB:.1f} dBm', rotation=90, va='top', ha='right', fontsize=9)

ax1.axvline(f_3rd_harm, color='purple', linestyle=':', alpha=0.6)
ax1.text(f_3rd_harm, -45, f'3er Arm. RF\n({f_3rd_harm} MHz)', rotation=90, va='bottom', ha='right', fontsize=9, color='purple')

ax1.grid(True, which='both', linestyle='--', alpha=0.5)
ax1.minorticks_on()

lines, labels = ax1.get_legend_handles_labels()
ax1.legend(lines, labels, loc='upper right')
plt.tight_layout()
plt.show()