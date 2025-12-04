function dydx = my_diff_ctr(x, y)
% MY_DIFF_CTR return the derivitive for the function at x with a centered estimation.
%
%   y : the y values of the function we want to differentiate
%   x : the x values of the function we want to differentiate

% Pretty sure I'm using this right: https://www.mathworks.com/help/matlab/ref/circshift.html
dydx = (circshift(y, 1) - circshift(y, -1)) ./ (circshift(x, 1) - circshift(x, -1));

% Use forward difference for the first point and backward difference for the last point
dydx(1) = (y(2) - y(1)) / (x(2) - x(1));
dydx(end) = (y(end) - y(end-1)) / (x(end) - x(end-1));
end
