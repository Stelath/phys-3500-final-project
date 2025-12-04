function [apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val] = findRoots(time, altitude, velocity, acceleration)
% FINDROOTS Find key flight events (apogee, max velocity, max acceleration)
%   [apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val] = findRoots(time, altitude, velocity, acceleration)
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
end
