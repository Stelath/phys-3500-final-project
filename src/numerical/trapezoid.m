function integral = trapezoid(f, a, b, n)
% TRAPEZOID return the integral using the trapezoid integration formula
%
%   NOTE: Assumes uniform spacing in x
%
%   f : function we want to integrate
%   a : lower bound of integration
%   b : upper bound of integration
%   n : number of intervals

dx = (b - a) / n;

integral = 0;
for i = 1:n
  x_left = a + (i - 1) * dx;
  x_right = a + i * dx;
  integral = integral + 0.5 * (f(x_left) + f(x_right)) * dx;
end
end
