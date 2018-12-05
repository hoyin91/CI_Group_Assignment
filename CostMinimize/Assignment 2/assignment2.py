import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

# Generate universe variables
x_verticalVelocity = np.arange(-30, 30, 1) #meter
x_height = np.arange(0, 500, 1) #speed
x_controlForce  = np.arange(-30, 30, 1) #braking force percentage

# Generate fuzzy membership functions
vv_df = fuzz.trimf(x_verticalVelocity, [-2000, -20, -10])
vv_ds = fuzz.trimf(x_verticalVelocity, [-20, -10, 0])
vv_z = fuzz.trimf(x_verticalVelocity, [-10, 0, 10])
vv_us = fuzz.trimf(x_verticalVelocity, [0, 10, 20])
vv_uf = fuzz.trimf(x_verticalVelocity, [10, 20, 2000])

h_g = fuzz.trimf(x_height, [0, 0, 250])
h_l = fuzz.trimf(x_height, [0, 100, 350])
h_m = fuzz.trimf(x_height, [150, 400, 650])
h_h = fuzz.trimf(x_height, [250, 500, 500])

cc_dl = fuzz.trimf(x_controlForce, [-2000, -20, -10])
cc_ds = fuzz.trimf(x_controlForce, [-20, -10, 0])
cc_z = fuzz.trimf(x_controlForce, [-10, 0, 10])
cc_us = fuzz.trimf(x_controlForce, [0, 10, 20])
cc_ul = fuzz.trimf(x_controlForce, [10, 20, 2000])

# Visualize these universes and membership functions
fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

ax0.plot(x_verticalVelocity, vv_df, 'b', linewidth=1.5, label='Down Fast')
ax0.plot(x_verticalVelocity, vv_ds, 'g', linewidth=1.5, label='Down Slow')
ax0.plot(x_verticalVelocity, vv_z, 'r', linewidth=1.5, label='Zero')
ax0.plot(x_verticalVelocity, vv_us, 'r', linewidth=1.5, label='Up Slow')
ax0.plot(x_verticalVelocity, vv_uf, 'r', linewidth=1.5, label='Up Fast')
ax0.set_title('Vertical Velocity')
ax0.legend()

ax1.plot(x_height, h_g, 'b', linewidth=1.5, label='Ground')
ax1.plot(x_height, h_l, 'g', linewidth=1.5, label='Low')
ax1.plot(x_height, h_m, 'r', linewidth=1.5, label='Medium')
ax1.plot(x_height, h_h, 'r', linewidth=1.5, label='High')
ax1.set_title('Height')
ax1.legend()

ax2.plot(x_controlForce, cc_dl, 'b', linewidth=1.5, label='Down Large')
ax2.plot(x_controlForce, cc_ds, 'g', linewidth=1.5, label='Down Small')
ax2.plot(x_controlForce, cc_z, 'r', linewidth=1.5, label='Zero')
ax2.plot(x_controlForce, cc_us, 'r', linewidth=1.5, label='Up Small')
ax2.plot(x_controlForce, cc_ul, 'r', linewidth=1.5, label='Up Large')
ax2.set_title('Control force')
ax2.legend()

# Turn off top/right axes
for ax in (ax0, ax1, ax2):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
#plt.show()

velocity = -12
height = 325

# We need the activation of our fuzzy membership functions at these values.
# This is what fuzz.interp_membership exists for!
vv_level_df = fuzz.interp_membership(x_verticalVelocity, vv_df, velocity)
vv_level_ds = fuzz.interp_membership(x_verticalVelocity, vv_ds, velocity)
vv_level_z = fuzz.interp_membership(x_verticalVelocity, vv_z, velocity)
vv_level_us = fuzz.interp_membership(x_verticalVelocity, vv_us, velocity)
vv_level_uf = fuzz.interp_membership(x_verticalVelocity, vv_uf, velocity)

h_level_g = fuzz.interp_membership(x_height, h_g, height)
h_level_l = fuzz.interp_membership(x_height, h_l, height)
h_level_m = fuzz.interp_membership(x_height, h_m, height)
h_level_h = fuzz.interp_membership(x_height, h_h, height)



vv_level_us_uf = np.fmax(vv_level_us, vv_level_uf)
h_level_l_g = np.fmax(h_level_l, h_level_g)
h_level_h_m = np.fmax(h_level_h, h_level_m)

active_rule1 = np.fmin(vv_level_z, h_level_l_g)
cf_activation_zero = np.fmin(active_rule1, cc_z)

active_rule2 = np.fmin(vv_level_df, h_level_l_g)
cf_activation_ul = np.fmin(active_rule2, cc_ul)

active_rule3 = np.fmin(vv_level_us_uf, h_level_l_g)
cf_activation_ds = np.fmin(active_rule3, cc_ds)

active_rule4 = np.fmin(vv_level_ds, h_level_l)
cf_activation_us = np.fmin(active_rule4, cc_us)

active_rule5 = np.fmin(vv_level_us, h_level_h_m)
cf_activation_dl = np.fmin(active_rule5, cc_dl)


tip0 = np.zeros_like(x_controlForce)
# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.fill_between(x_controlForce, tip0, cf_activation_zero, facecolor='b', alpha=0.7)
ax0.plot(x_controlForce, cc_dl, 'b', linewidth=0.5, linestyle='--', )
ax0.fill_between(x_controlForce, tip0, cf_activation_ul, facecolor='g', alpha=0.7)
ax0.plot(x_controlForce, cc_ds, 'g', linewidth=0.5, linestyle='--')
ax0.fill_between(x_controlForce, tip0, cf_activation_ds, facecolor='r', alpha=0.7)
ax0.plot(x_controlForce, cc_z, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(x_controlForce, tip0, cf_activation_us, facecolor='y', alpha=0.7)
ax0.plot(x_controlForce, cc_ul, 'y', linewidth=0.5, linestyle='--')
ax0.fill_between(x_controlForce, tip0, cf_activation_dl, facecolor='m', alpha=0.7)
ax0.plot(x_controlForce, cc_us, 'm', linewidth=0.5, linestyle='--')
ax0.set_title('Output membership activity')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()

# Aggregate all three output membership functions together
#aggregated = np.fmax(cf_activation_zero, np.fmax(cf_activation_ul, np.fmax(cf_activation_ds, np.fmax(cf))))
aggregated = np.fmax(cf_activation_zero, np.fmax(np.fmax(cf_activation_ds, cf_activation_ul), np.fmax(cf_activation_us, cf_activation_dl)))

# Calculate defuzzified result
tip = fuzz.defuzz(x_controlForce, aggregated, 'centroid')
tip_activation = fuzz.interp_membership(x_controlForce, aggregated, tip)  # for plot

# Visualize this
fig, ax0 = plt.subplots(figsize=(8, 3))

ax0.plot(x_controlForce, cc_dl, 'b', linewidth=0.5, linestyle='--', )
ax0.plot(x_controlForce, cc_ds, 'g', linewidth=0.5, linestyle='--')
ax0.plot(x_controlForce, cc_z, 'r', linewidth=0.5, linestyle='--')
ax0.plot(x_controlForce, cc_ul, 'r', linewidth=0.5, linestyle='--')
ax0.plot(x_controlForce, cc_us, 'r', linewidth=0.5, linestyle='--')
ax0.fill_between(x_controlForce, tip0, aggregated, facecolor='Orange', alpha=0.7)
ax0.plot([tip, tip], [0, tip_activation], 'k', linewidth=1.5, alpha=0.9)
ax0.set_title('Aggregated membership and result (line)')

# Turn off top/right axes
for ax in (ax0,):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

plt.tight_layout()
plt.show()