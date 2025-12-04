function [time_interp, alt_linear, alt_spline] = interpolateAltitude(time, altitude, num_points)
% INTERPOLATEALTITUDE Generate smooth altitude data using interpolation
%   [time_interp, alt_linear, alt_spline] = interpolateAltitude(time, altitude, num_points)
%
%   time       : original time vector
%   altitude   : original altitude vector
%   num_points : number of points for the interpolated vectors
%
%   time_interp : new high-resolution time vector
%   alt_linear  : linearly interpolated altitude
%   alt_spline  : cubic spline interpolated altitude

% Create high-resolution time vector
time_interp = linspace(min(time), max(time), num_points);

% Linear Interpolation
alt_linear = interp1(time, altitude, time_interp, 'linear');

% Cubic Spline Interpolation
% Using our custom function
alt_spline = cubicSplineInterp(time, altitude, time_interp);
end
