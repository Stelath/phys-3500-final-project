function [time_interp, alt_spline] = interpolateAltitude(time, altitude, num_points)
% INTERPOLATEALTITUDE Generate smooth altitude data using interpolation
%   [time_interp, alt_spline] = interpolateAltitude(time, altitude, num_points)
%
%   time       : original time vector
%   altitude   : original altitude vector
%   num_points : number of points for the interpolated vectors
%
%   time_interp : interpolated time vector
%   alt_spline  : cubic spline interpolated altitude

time_interp = linspace(min(time), max(time), num_points);
alt_spline = cubicSplineInterp(time, altitude, time_interp);
end
