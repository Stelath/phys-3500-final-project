function [t, y] = euler_modified(f, t_span, y0, h)
% EULER_MODIFIED Solve ODE using Modified Euler method (Heun's method)
%   [t, y] = euler_modified(f, t_span, y0, h)
%
%   f      : function handle for dy/dt = f(t, y)
%   t_span : [t_start, t_end]
%   y0     : initial condition
%   h      : step size

t = t_span(1):h:t_span(2);
y = zeros(length(t), length(y0));
y(1, :) = y0;

for i = 1:length(t)-1
    % Predictor step (Euler)
    k1 = f(t(i), y(i, :));
    y_predict = y(i, :) + h * k1';

    % Corrector step
    k2 = f(t(i+1), y_predict);
    y(i+1, :) = y(i, :) + (h/2) * (k1' + k2');
end
end
