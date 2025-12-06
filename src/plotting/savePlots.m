function savePlots(time, altitude, velocity, acceleration, t_model, y_model, apogee_idx, accel_measured, impact_time, impact_vel)
% SAVEPLOTS Save rocket flight analysis plots to files
%   Saves high-quality images of the analysis plots to the 'results' directory.

% Create results directory if it doesn't exist
if ~exist('results', 'dir')
    mkdir('results');
end

fprintf('Saving plots to results/ directory...\n');

%% 1. Flight Analysis (Combined)
f1 = figure('Visible', 'off', 'Position', [0, 0, 1500, 500]);

% Altitude
subplot(1, 3, 1);
plot(time, altitude, 'b-', 'LineWidth', 1.5); hold on;
plot(t_model, y_model, 'r--', 'LineWidth', 1.5);
plot(time(apogee_idx), altitude(apogee_idx), 'ko', 'MarkerFaceColor', 'g');
plot(impact_time, 0, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title('Altitude vs. Time');
xlabel('Time (s)'); ylabel('Altitude (m)');
legend('Measured (Spline)', 'Model (ODE)', 'Apogee', 'Impact');
grid on;

% Velocity
subplot(1, 3, 2);
plot(time, velocity, 'g-', 'LineWidth', 1.5); hold on;
yline(0, 'k--');
plot(impact_time, impact_vel, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title('Velocity vs. Time');
xlabel('Time (s)'); ylabel('Velocity (m/s)');
grid on;

% Acceleration
subplot(1, 3, 3);
plot(time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
xline(impact_time, 'r:', 'LineWidth', 1.5);
title('Acceleration vs. Time');
xlabel('Time (s)'); ylabel('Acceleration (m/s^2)');
grid on;

exportgraphics(f1, 'results/flight_analysis.png', 'Resolution', 300);
close(f1);

%% 2. Altitude (Single)
f2 = figure('Visible', 'off');
plot(time, altitude, 'b-', 'LineWidth', 1.5); hold on;
plot(t_model, y_model, 'r--', 'LineWidth', 1.5);
plot(time(apogee_idx), altitude(apogee_idx), 'ko', 'MarkerFaceColor', 'g');
plot(impact_time, 0, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title('Altitude vs. Time');
xlabel('Time (s)'); ylabel('Altitude (m)');
legend('Measured (Spline)', 'Model (ODE)', 'Apogee', 'Impact');
grid on;
exportgraphics(f2, 'results/altitude.png', 'Resolution', 300);
close(f2);

%% 3. Velocity (Single)
f3 = figure('Visible', 'off');
plot(time, velocity, 'g-', 'LineWidth', 1.5); hold on;
yline(0, 'k--');
plot(impact_time, impact_vel, 'rx', 'MarkerSize', 10, 'LineWidth', 2);
title('Velocity vs. Time');
xlabel('Time (s)'); ylabel('Velocity (m/s)');
grid on;
exportgraphics(f3, 'results/velocity.png', 'Resolution', 300);
close(f3);

%% 4. Acceleration (Single)
f4 = figure('Visible', 'off');
plot(time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
xline(impact_time, 'r:', 'LineWidth', 1.5);
title('Acceleration vs. Time');
xlabel('Time (s)'); ylabel('Acceleration (m/s^2)');
grid on;
exportgraphics(f4, 'results/acceleration.png', 'Resolution', 300);
close(f4);

%% 5. Validation
f5 = figure('Visible', 'off');
plot(time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
plot(time, accel_measured, 'c-', 'LineWidth', 1.5);
accel_error = acceleration - accel_measured;
plot(time, accel_error, 'r:', 'LineWidth', 1.5);
title('Acceleration Validation: Derived vs. Measured');
xlabel('Time (s)'); ylabel('Accel (m/s^2)');
legend('Derived (Kinematic)', 'Measured (Sensor)', 'Difference (Error)');
grid on;
exportgraphics(f5, 'results/validation.png', 'Resolution', 300);
close(f5);

fprintf('Plots saved successfully.\n');
end
