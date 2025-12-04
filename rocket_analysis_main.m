% Rocket Flight Analysis - Main Driver Script
%
% This script coordinates the analysis of rocket flight data.
% It performs data import, interpolation, differentiation, root finding,
% integration, and ODE modeling.

clear; close all; clc;

% Add src and subdirectories to path
addpath('src');
addpath('src/data');
addpath('src/numerical');
addpath('src/physics');
addpath('src/plotting');

%% 1. Setup and Constants
filename = 'ROCKET-FLIGHT-DATA.csv';
g = 9.81;       % Gravity (m/s^2)
mass = 0.5;     % Mass (kg) - ESTIMATE/PLACEHOLDER

fprintf('Running Rocket Flight Analysis...\n');

%% 2. Data Import
fprintf('Importing data...\n');
[time_raw, alt_raw, accel_raw] = importData(filename);


%% 3. Interpolation
fprintf('Interpolating altitude data...\n');
% Create a uniform high-res time vector for analysis
% Reduced from 10000 to 2000 to reduce noise amplification in differentiation
num_points = 2000;
[time, alt_linear, alt_spline] = interpolateAltitude(time_raw, alt_raw, num_points);

% Interpolate acceleration for validation
accel_interp = interp1(time_raw, accel_raw, time, 'linear');

% We will use the Spline interpolation for subsequent calculations as it's smoother
% Apply additional smoothing to remove high-frequency noise before differentiation
alt_analysis = smoothdata(alt_spline, 'gaussian', 50);

%% 4. Numerical Differentiation
fprintf('Calculating velocity and acceleration...\n');
[velocity, acceleration] = numericalDifferentiate(time, alt_analysis);

%% 5. Root Finding
fprintf('Finding key flight events...\n');
[apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val, impact_time, impact_vel] = ...
    findRoots(time, alt_analysis, velocity, acceleration);

fprintf('  Apogee:           %.2f m at %.2f s\n', apogee_height, apogee_time);
fprintf('  Max Velocity:     %.2f m/s at %.2f s\n', max_vel_val, max_vel_time);
fprintf('  Max Acceleration: %.2f m/s^2 at %.2f s\n', max_acc_val, max_acc_time);
fprintf('  Impact:           %.2f m/s at %.2f s\n', impact_vel, impact_time);

%% 6. Numerical Integration
fprintf('Calculating total distance traveled...\n');
total_dist = numericalIntegrate(time, velocity);
fprintf('  Total Distance:   %.2f m\n', total_dist);

%% 7. ODE Solving (Drag Estimation)
fprintf('Estimating drag coefficient...\n');
% Use max_vel_time (approx burnout) as start time for coast phase analysis
% Use apogee_time as end time (before parachute deployment)
[k_est, t_model, y_model] = solveDragODE(time, alt_analysis, velocity, mass, g, max_vel_time, apogee_time);
fprintf('  Estimated k:      %.4f kg/s\n', k_est);

%% 8. Visualization
fprintf('Plotting results...\n');
% Find index of apogee for plotting
[~, apogee_idx] = min(abs(time - apogee_time));
plotResults(time, alt_analysis, velocity, acceleration, t_model, y_model, apogee_idx, accel_interp, impact_time, impact_vel);

%% 9. Validation
% Validation removed as per user request
% validateResults(time, alt_analysis, velocity, acceleration, apogee_time);

fprintf('Analysis Complete.\n');
