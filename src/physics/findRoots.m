function [apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val, impact_time, impact_vel] = findRoots(time, altitude, velocity, acceleration)
% FINDROOTS Find key flight events (apogee, max velocity, max acceleration, impact)
%   [apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val, impact_time, impact_vel] = findRoots(time, altitude, velocity, acceleration)
%
%   Note: This function uses a mix of direct search (max) and root finding
%   where appropriate. For discrete data, finding the exact root of v=0
%   might require interpolation, but finding the index of max height is simpler.

% 1. Apogee (Maximum Height)
% Physical definition: Velocity = 0
% Data definition: Max altitude
[apogee_height, idx_apogee] = max(altitude);
apogee_time = time(idx_apogee);

% Refinement: Find where velocity crosses 0 near the peak
% We can use bisection on the velocity array indices if we want,
% or just take the max altitude index which is robust for noisy data.
% Let's stick to the max altitude index for robustness.

% 2. Maximum Velocity
[max_vel_val, idx_vel] = max(velocity);
max_vel_time = time(idx_vel);

% 3. Maximum Acceleration
[max_acc_val, idx_acc] = max(acceleration);
max_acc_time = time(idx_acc);

% 4. Ground Impact
% Find where altitude crosses 0 after apogee
% We search in the data after the apogee
time_descent = time(idx_apogee:end);
alt_descent = altitude(idx_apogee:end);

% Find index where altitude goes negative or is minimum
idx_impact_local = find(alt_descent <= 0, 1);

if isempty(idx_impact_local)
    % If it never crosses 0 (maybe data cut off), take the last point
    impact_time = time(end);
    impact_vel = velocity(end);
else
    % Adjust index to global time vector
    idx_impact = idx_apogee + idx_impact_local - 1;

    % Linear interpolation for more precise time where alt = 0
    t1 = time(idx_impact - 1);
    t2 = time(idx_impact);
    y1 = altitude(idx_impact - 1);
    y2 = altitude(idx_impact);

    % 0 = y1 + (y2 - y1)/(t2 - t1) * (t_impact - t1)
    % t_impact = t1 - y1 * (t2 - t1) / (y2 - y1)
    impact_time = t1 - y1 * (t2 - t1) / (y2 - y1);

    % Interpolate velocity at impact time
    impact_vel = interp1(time, velocity, impact_time);
end
end
