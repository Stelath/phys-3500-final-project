function [time, altitude, accel_vertical] = importData(filename)
% IMPORTDATA Import and preprocess rocket flight data
%   [time, altitude, accelz] = importData(filename)

data = readtable(filename);

% Extract columns
% Extract columns
raw_time = data.time;
altitude = data.altitude;
accel_vertical = data.accelx; % accelx is vertical (approx 9.8 on pad)

% Normalize time (assuming nanoseconds based on magnitude)
% Shift to start at 0 and convert to seconds
time = (raw_time - raw_time(1)) / 1e9;

% Ensure data is sorted by time
[time, sortIdx] = sort(time);
altitude = altitude(sortIdx);
accel_vertical = accel_vertical(sortIdx);
end
