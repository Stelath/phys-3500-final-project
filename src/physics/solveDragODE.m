function [k_est, t_model, y_model] = solveDragODE(time, altitude, velocity, mass, g, t_start)
% SOLVEDRAGODE Estimate drag coefficient and model trajectory
%   [k_est, t_model, y_model] = solveDragODE(time, altitude, velocity, mass, g, t_start)
%
%   Model: m*v' = -mg - kv (Linear Drag)
%   Note: Fitting is restricted to t >= t_start (coast phase)

% 1. Define the ODE function for optimization
% State vector Y = [y; v]
ode_fun = @(t, Y, k) [Y(2); -g - (k/mass)*Y(2)];

% 2. Prepare data for fitting (Coast Phase Only)
% Find index corresponding to t_start
idx_start = find(time >= t_start, 1);
time_fit = time(idx_start:end);
alt_fit = altitude(idx_start:end);
vel_fit = velocity(idx_start:end);

% Initial conditions for the fit
y0 = alt_fit(1);
v0 = vel_fit(1);
Y0 = [y0; v0];
t_span = [min(time_fit), max(time_fit)];

% Sweep k values
k_candidates = linspace(0, 3.0, 50);
errors = zeros(size(k_candidates));

for i = 1:length(k_candidates)
    k_val = k_candidates(i);
    [t_sol, Y_sol] = ode45(@(t,y) ode_fun(t,y,k_val), time_fit, Y0);

    % Interpolate solution to match data points for error calc
    y_sol_interp = interp1(t_sol, Y_sol(:,1), time_fit);
    errors(i) = sqrt(mean((y_sol_interp - alt_fit).^2));
end

[~, best_idx] = min(errors);
k_est = k_candidates(best_idx);

% 3. Generate full model with best k using Euler Modified
% We model from t_start onwards
h = 0.01; % Step size

% Define function for Euler Modified (returns column vector to match transpose in solver)
f_euler = @(t, Y) [Y(2); -g - (k_est/mass)*Y(2)];

[t_model, Y_model] = euler_modified(f_euler, t_span, Y0', h);
y_model = Y_model(:, 1);
end
