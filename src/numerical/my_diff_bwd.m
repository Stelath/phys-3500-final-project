function dydx = my_diff_bwd(x, y)
% MY_DIFF_BWD return the derivitive for the function at x with a backward estimation.
%
%   y : the y values of the function we want to differentiate
%   x : the x values of the function we want to differentiate

dydx = (circshift(y, 1) - y) ./ (circshift(x, 1) - x);

% Use forward difference for the first point
dydx(1) = (y(2) - y(1)) / (x(2) - x(1));
end
