function [apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val, impact_time, impact_vel] = findRoots(time, altitude, velocity, acceleration)
% FINDROOTS Find key flight events (apogee, max velocity, max acceleration, impact)
%   [apogee_time, apogee_height, max_vel_time, max_vel_val, max_acc_time, max_acc_val, impact_time, impact_vel] = findRoots(time, altitude, velocity, acceleration)
%

% Find the apogee which is just the maximum height (also when velocity = 0)
[apogee_height, idx_apogee] = max(altitude);
apogee_time = time(idx_apogee);

% Find the maximum velocity
[max_vel_val, idx_vel] = max(velocity);
max_vel_time = time(idx_vel);

% Find the maximum acceleration
[max_acc_val, idx_acc] = max(acceleration);
max_acc_time = time(idx_acc);

% Find where the rocket impacted the ground

% Clip to search only after apogee occurs, cause everything before that is ascent
alt_descent = altitude(idx_apogee:end);

% Whenever the altitude goes below 0, we have impact
idx_impact_local = find(alt_descent <= 0, 1);

if isempty(idx_impact_local)
    % If it never crosses 0 (sensors get shredded sometimes or rocket blows up), take the last point
    impact_time = time(end);
    impact_vel = velocity(end);
else
    % Adjust index to global time vector
    idx_impact = idx_apogee + idx_impact_local - 1;

    t1 = time(idx_impact - 1);
    t2 = time(idx_impact);
    y1 = altitude(idx_impact - 1);
    y2 = altitude(idx_impact);

    impact_time = t1 - y1 * (t2 - t1) / (y2 - y1);

    % Interpolate velocity at the exact time of impact so we can get it super precise
    impact_vel = interp1(time, velocity, impact_time);
end
