function yq = cubicSplineInterp(x, y, xq)
%CUBICSPLINEINTERP Natural cubic spline interpolation
%
%   yq = cubicSplineInterp(x, y, xq)
%
% Inputs:
%   x  - data point positions (must be strictly increasing)
%   y  - data point values
%   xq - query points (scalar or vector)
%
% Output:
%   yq - interpolated values at xq

n = numel(x);
if numel(y) ~= n
    error('x and y must have the same length.');
end
if n < 3
    error('At least 3 data points are required.');
end

% Step sizes
h = diff(x);

% Solve tridiagonal system for second derivatives (M)
% System: A * M = rhs
A = zeros(n);
rhs = zeros(n,1);

% Natural spline boundary conditions
A(1,1) = 1;       % M1 = 0
A(n,n) = 1;       % Mn = 0

% Fill tridiagonal matrix
for i = 2:n-1
    A(i,i-1) = h(i-1);
    A(i,i)   = 2*(h(i-1)+h(i));
    A(i,i+1) = h(i);
    rhs(i)   = 6*((y(i+1)-y(i))/h(i) - (y(i)-y(i-1))/h(i-1));
end

% Solve system
M = A\rhs;

% Evaluate spline at query points
yq = zeros(size(xq));
for k = 1:numel(xq)
    % Find interval containing xq(k)
    i = find(xq(k) >= x(1:end-1) & xq(k) <= x(2:end), 1);
    if isempty(i)
        % Extrapolation: clamp to nearest interval
        if xq(k) < x(1)
            i = 1;
        else
            i = n-1;
        end
    end
    hi = x(i+1) - x(i);

    % Cubic spline formula
    term1 = M(i)   * (x(i+1)-xq(k))^3 / (6*hi);
    term2 = M(i+1) * (xq(k)-x(i))^3 / (6*hi);
    term3 = (y(i)  - M(i)*hi^2/6) * (x(i+1)-xq(k))/hi;
    term4 = (y(i+1)- M(i+1)*hi^2/6) * (xq(k)-x(i))/hi;

    yq(k) = term1 + term2 + term3 + term4;
end
end
