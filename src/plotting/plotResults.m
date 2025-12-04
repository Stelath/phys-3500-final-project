function plotResults(time, altitude, velocity, acceleration, t_model, y_model, apogee_idx, accel_measured)
% PLOTRESULTS Visualize rocket flight data

figure('Name', 'Rocket Flight Analysis', 'NumberTitle', 'off', 'Position', [100, 100, 1200, 800]);

% 1. Altitude
subplot(2, 3, 1);
plot(time, altitude, 'b-', 'LineWidth', 1.5); hold on;
plot(t_model, y_model, 'r--', 'LineWidth', 1.5);
plot(time(apogee_idx), altitude(apogee_idx), 'ko', 'MarkerFaceColor', 'g');
title('Altitude vs. Time');
xlabel('Time (s)'); ylabel('Altitude (m)');
legend('Measured (Spline)', 'Model (ODE)', 'Apogee');
grid on;

% 2. Velocity
subplot(2, 3, 2);
plot(time, velocity, 'g-', 'LineWidth', 1.5);
yline(0, 'k--');
title('Velocity vs. Time');
xlabel('Time (s)'); ylabel('Velocity (m/s)');
grid on;

% 3. Acceleration
subplot(2, 3, 3);
plot(time, acceleration, 'm-', 'LineWidth', 1.5);
title('Acceleration vs. Time');
xlabel('Time (s)'); ylabel('Acceleration (m/s^2)');
grid on;

% 4. Trajectory (Altitude vs Velocity phase plot)
subplot(2, 3, 4);
plot(velocity, altitude, 'k-', 'LineWidth', 1.5);
title('Phase Plot: Altitude vs. Velocity');
xlabel('Velocity (m/s)'); ylabel('Altitude (m)');
grid on;

% 5. Acceleration Validation
subplot(2, 3, 5);
plot(time, acceleration, 'm-', 'LineWidth', 1.5); hold on;
% Measured acceleration includes gravity (approx +9.81 on pad).
% To compare with derived kinematic acceleration (which is net acceleration),
% we can subtract g from measured, or just plot them as is and explain.
% Let's plot (Measured - 9.81) to align with kinematic acceleration (approx).
plot(time, accel_measured - 9.81, 'c--', 'LineWidth', 1.5);
title('Acceleration Validation');
xlabel('Time (s)'); ylabel('Accel (m/s^2)');
legend('Derived (Alt)', 'Measured - g');
grid on;

end
