function total_distance = numericalIntegrate(time, velocity)
% NUMERICALINTEGRATE Calculate total distance traveled by integrating velocity with the trapezoid rule
%   total_distance = numericalIntegrate(time, velocity)
%
%   time     : time vector
%   velocity : velocity vector
%
%   total_distance : integral of velocity

% We want total distance, so we integrate absolute velocity (speed)
speed = abs(velocity);
total_distance = trapz(time, speed);
end
