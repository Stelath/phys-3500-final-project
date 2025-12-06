function [k_est, t_model, y_model] = solveDragODE(time, altitude, velocity, mass, g, t_start, t_end)
% SOLVEDRAGODE Estimate drag coefficient and model trajectory using RK4
%   [k_est, t_model, y_model] = solveDragODE(time, altitude, velocity, mass, g, t_start, t_end)
%
%   time       : time vector from flight data
%   altitude   : altitude vector from flight data
%   velocity   : velocity vector from flight data
%   mass       : rocket mass (kg)
%   g          : gravity (m/s^2)
%   t_start    : start time for fitting (burnout)
%   t_end      : end time for fitting (apogee)
%
%   k_est      : estimated drag coefficient
%   t_model    : modeled time vector
%   y_model    : modeled altitude vector
%
%   Model: m*v' = -mg - k*v*|v| (Quadratic Drag)
%   Only fit the coast phase since the parachute deployment messes
%   up the model, cause its drag characteristics are completely different.

% Find indices corresponding to t_start and t_end
idx_start = find(time >= t_start, 1);
idx_end = find(time >= t_end, 1);

if isempty(idx_end)
    idx_end = length(time);
end

% Get only the coast phase data
time_fit = time(idx_start:idx_end);
alt_fit = altitude(idx_start:idx_end);
vel_fit = velocity(idx_start:idx_end);

% Initial conditions
y0 = alt_fit(1);
v0 = vel_fit(1);

t_span_model = [min(time_fit), max(time)];

% Find optimal k by doing bisection
cost_fun = @(k_val) calculateError(k_val, time_fit, y0, v0, alt_fit, mass, g);
k_est = fminbnd(cost_fun, 0, 0.1);

% Generate full trajectory model with best k using 4th order Runge-Kutta
h = 0.01;
[t_model, y_model, ~] = rungeKutta4(t_span_model, y0, v0, k_est, mass, g, h);

end


function err = calculateError(k_val, time_fit, y0, v0, alt_fit, mass, g)
% CALCULATEERROR Compute RMSE between model and data for a given k
%   err = calculateError(k_val, time_fit, y0, v0, alt_fit, mass, g)

h = 0.01;
t_span = [time_fit(1), time_fit(end)];

[t_sol, y_sol, ~] = rungeKutta4(t_span, y0, v0, k_val, mass, g, h);

% Handle solver failures
if length(t_sol) < 2
    err = 1e9;
    return;
end

% Interpolate solution to match data points
y_sol_interp = interp1(t_sol, y_sol, time_fit, 'linear', 'extrap');
err = sqrt(mean((y_sol_interp - alt_fit).^2));
end
