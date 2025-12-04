function integral = simpson(f, a, b, n)
% SIMPSON return the integral using Simpson's integration formula
%
%   NOTE: Assumes uniform spacing in x
%
%   f : function we want to integrate
%   a : lower bound of integration
%   b : upper bound of integration
%   n : number of intervals

dx = (b - a) / n;
x = a:dx:b;

integral = 0;
integral = integral + f(x(1)); % left boundary

for i = 2:2:n % 2, 4, 6, ..., n-1
    integral = integral + 4 * f(x(i));
end
for i = 3:2:n-1 % 3, 5, 7, ..., n-2
    integral = integral + 2 * f(x(i));
end

integral = integral + f(x(n + 1)); % right boundary
integral = integral * dx / 3.0;    % normalize by h/3
end
