function plotResults(time, altitude, velocity, acceleration, t_model, y_model, apogee_idx, accel_measured, impact_time, impact_vel)
% PLOTRESULTS Visualize rocket flight data

f = figure('Name', 'Rocket Flight Analysis', 'NumberTitle', 'off', 'Position', [100, 100, 1500, 600]);

tabgp = uitabgroup(f);

%% Tab 1: Flight Analysis (Combined)
tab1 = uitab(tabgp, 'Title', 'Flight Analysis');
axes('Parent', tab1);

% 1. Altitude
subplot(1, 3, 1, 'Parent', tab1);
plot(time, altitude, 'b-', 'LineWidth', 1.5); hold on;
plot(t_model, y_model, 'r--', 'LineWidth', 1.5);
plot(time(apogee_idx), altitude(apogee_idx), 'ko', 'MarkerFaceColor', 'g');
plot(impact_time, 0, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title('Altitude vs. Time');
xlabel('Time (s)'); ylabel('Altitude (m)');
legend('Measured (Spline)', 'Model (ODE)', 'Apogee', 'Impact');
grid on;

% 2. Velocity
subplot(1, 3, 2, 'Parent', tab1);
plot(time, velocity, 'g-', 'LineWidth', 1.5); hold on;
yline(0, 'k--');
plot(impact_time, impact_vel, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title('Velocity vs. Time');
xlabel('Time (s)'); ylabel('Velocity (m/s)');
grid on;

% 3. Acceleration
subplot(1, 3, 3, 'Parent', tab1);
plot(time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
xline(impact_time, 'r:', 'LineWidth', 1.5);
title('Acceleration vs. Time');
xlabel('Time (s)'); ylabel('Acceleration (m/s^2)');
grid on;

%% Tab 2: Altitude (Single)
tab2 = uitab(tabgp, 'Title', 'Altitude');
ax2 = axes('Parent', tab2);
plot(ax2, time, altitude, 'b-', 'LineWidth', 1.5); hold on;
plot(ax2, t_model, y_model, 'r--', 'LineWidth', 1.5);
plot(ax2, time(apogee_idx), altitude(apogee_idx), 'ko', 'MarkerFaceColor', 'g');
plot(ax2, impact_time, 0, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title(ax2, 'Altitude vs. Time');
xlabel(ax2, 'Time (s)'); ylabel(ax2, 'Altitude (m)');
legend(ax2, 'Measured (Spline)', 'Model (ODE)', 'Apogee', 'Impact');
grid(ax2, 'on');

%% Tab 3: Velocity (Single)
tab3 = uitab(tabgp, 'Title', 'Velocity');
ax3 = axes('Parent', tab3);
plot(ax3, time, velocity, 'g-', 'LineWidth', 1.5); hold on;
yline(ax3, 0, 'k--');
plot(ax3, impact_time, impact_vel, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title(ax3, 'Velocity vs. Time');
xlabel(ax3, 'Time (s)'); ylabel(ax3, 'Velocity (m/s)');
grid(ax3, 'on');

%% Tab 4: Acceleration (Single)
tab4 = uitab(tabgp, 'Title', 'Acceleration');
ax4 = axes('Parent', tab4);
plot(ax4, time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
xline(ax4, impact_time, 'r:', 'LineWidth', 1.5);
title(ax4, 'Acceleration vs. Time');
xlabel(ax4, 'Time (s)'); ylabel(ax4, 'Acceleration (m/s^2)');
grid(ax4, 'on');

%% Tab 5: Validation
tab5 = uitab(tabgp, 'Title', 'Validation');
ax5 = axes('Parent', tab5);

% Acceleration Comparison
plot(ax5, time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
plot(ax5, time, accel_measured, 'c-', 'LineWidth', 1.5);

% Calculate and plot error (Difference)
accel_error = acceleration - accel_measured;
plot(ax5, time, accel_error, 'r:', 'LineWidth', 1.5);

title(ax5, 'Acceleration Validation: Derived vs. Measured');
xlabel(ax5, 'Time (s)'); ylabel(ax5, 'Accel (m/s^2)');
legend(ax5, 'Derived (Kinematic)', 'Measured (Sensor)', 'Difference (Error)');
grid(ax5, 'on');

end
