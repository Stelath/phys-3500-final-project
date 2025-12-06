addpath('src');
addpath('src/data');
addpath('src/numerical');
addpath('src/physics');

fprintf('Running verification after fix...\n');
filename = 'ROCKET-FLIGHT-DATA.csv';
[time_raw, alt_raw, ~] = importData(filename);

num_points = 2000;
[time, ~, alt_spline] = interpolateAltitude(time_raw, alt_raw, num_points);
alt_analysis = smoothdata(alt_spline, 'gaussian', 50);
[velocity, ~] = numericalDifferentiate(time, alt_analysis);

[~, max_vel_idx] = max(velocity);
max_vel_time = time(max_vel_idx);
[~, apogee_idx] = max(alt_analysis);
apogee_time = time(apogee_idx);

mass = 0.5;
g = 9.81;

fprintf('Calling solveDragODE...\n');
[k_est, t_model, y_model] = solveDragODE(time, alt_analysis, velocity, mass, g, max_vel_time, apogee_time);

fprintf('Estimated Quadratic k: %.6f\n', k_est);
fprintf('Model trajectory: starts at %.2f m, ends at %.2f m\n', y_model(1), y_model(end));
fprintf('Max model altitude: %.2f m\n', max(y_model));

if k_est > 0 && k_est < 0.01 && max(y_model) > 400
    fprintf('VERIFICATION PASSED: k and trajectory look reasonable!\n');
else
    fprintf('VERIFICATION WARNING: Check results carefully.\n');
end
