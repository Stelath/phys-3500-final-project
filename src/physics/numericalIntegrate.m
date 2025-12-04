function total_distance = numericalIntegrate(time, velocity)
% NUMERICALINTEGRATE Calculate total distance traveled
%   total_distance = numericalIntegrate(time, velocity)
%
%   time     : time vector
%   velocity : velocity vector
%
%   total_distance : integral of |velocity| dt

% We want total distance, so we integrate absolute velocity (speed)
speed = abs(velocity);

% Use trapezoidal rule for non-uniform or uniform data
% Using built-in trapz for robustness with potentially non-uniform time.
total_distance = trapz(time, speed);

% Note: If strict adherence to 'trapezoid.m' is required, we would need to ensure uniformity.
% But trapz is safer for general data.
end
