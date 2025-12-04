function [velocity, acceleration] = numericalDifferentiate(time, position)
% NUMERICALDIFFERENTIATE Calculate velocity and acceleration
%   [velocity, acceleration] = numericalDifferentiate(time, position)
%
%   time     : time vector
%   position : position vector (e.g., altitude)
%
%   velocity     : calculated velocity (m/s)
%   acceleration : calculated acceleration (m/s^2)

% Calculate Velocity (1st derivative)
% Using centered difference for better accuracy
velocity = my_diff_ctr(time, position);

% Calculate Acceleration (2nd derivative)
% Differentiating velocity
acceleration = my_diff_ctr(time, velocity);
end
