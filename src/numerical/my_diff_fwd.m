function dydx = my_diff_fwd(x, y)
% MY_DIFF_FWD return the derivitive for the function at x with a forward estimation.
%
%   y : the y values of the function we want to differentiate
%   x : the x values of the function we want to differentiate

dydx = diff(y) ./ diff(x);

% Use backward difference for the last point
dydx(end+1) = (y(end) - y(end-1)) / (x(end) - x(end-1));
end
