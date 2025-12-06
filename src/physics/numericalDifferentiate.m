function [velocity, acceleration] = numericalDifferentiate(time, position)
% NUMERICALDIFFERENTIATE Calculate velocity and acceleration
%   [velocity, acceleration] = numericalDifferentiate(time, position)
%
%   time     : time vector
%   position : position vector
%
%   velocity     : calculated velocity (m/s)
%   acceleration : calculated acceleration (m/s^2)

% Calculate Velocity and Acceleration by taking the first and second derivatives
velocity = my_diff_ctr(time, position);
acceleration = my_diff_ctr(time, velocity);
end
