function [t_out, y_out, v_out] = rungeKutta4(t_span, y0, v0, k, mass, g, h)
% RUNGEKUTTA4 Solve drag ODE using 4th order Runge-Kutta method
%   [t_out, y_out, v_out] = rungeKutta4(t_span, y0, v0, k, mass, g, h)
%
%   t_span : [t_start, t_end] time interval
%   y0     : initial altitude
%   v0     : initial velocity
%   k      : drag coefficient
%   mass   : rocket mass
%   g      : gravitational acceleration
%   h      : step size
%
%   t_out  : time vector
%   y_out  : altitude vector
%   v_out  : velocity vector
%
%   ODEs:
%     y' = v
%     v' = -g - (k/mass)*v*|v|

ta = t_span(1);
tb = t_span(2);

% Number of points
npts = ceil((tb - ta) / h) + 1;
h = (tb - ta) / (npts - 1);

% Time grid
tt = linspace(ta, tb, npts);

% Initialize solution arrays
y_rk = zeros(1, npts);
v_rk = zeros(1, npts);

% Set initial conditions
y_rk(1) = y0;
v_rk(1) = v0;

% Drag coefficient ratio
k2m = k / mass;

% 4th order Runge-Kutta integration loop
for i = 1:npts-1
    % Current state
    y_i = y_rk(i);
    v_i = v_rk(i);

    % k1 = f(t_n, Y_n)
    yp_k1 = v_i;
    vp_k1 = -g - k2m * v_i * abs(v_i);

    % k2 = f(t_n + h/2, Y_n + k1*h/2)
    yp_k2 = v_i + vp_k1 * h/2;
    vp_k2 = -g - k2m * (v_i + vp_k1 * h/2) * abs(v_i + vp_k1 * h/2);

    % k3 = f(t_n + h/2, Y_n + k2*h/2)
    yp_k3 = v_i + vp_k2 * h/2;
    vp_k3 = -g - k2m * (v_i + vp_k2 * h/2) * abs(v_i + vp_k2 * h/2);

    % k4 = f(t_n + h, Y_n + k3*h)
    yp_k4 = v_i + vp_k3 * h;
    vp_k4 = -g - k2m * (v_i + vp_k3 * h) * abs(v_i + vp_k3 * h);

    % Update: Y_{n+1} = Y_n + h*(k1/6 + k2/3 + k3/3 + k4/6)
    y_rk(i+1) = y_i + h * (yp_k1/6 + yp_k2/3 + yp_k3/3 + yp_k4/6);
    v_rk(i+1) = v_i + h * (vp_k1/6 + vp_k2/3 + vp_k3/3 + vp_k4/6);
end

% Return as column vectors to match typical ODE solver output
t_out = tt';
y_out = y_rk';
v_out = v_rk';

end
