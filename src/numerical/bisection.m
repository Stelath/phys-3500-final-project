function [root, iter] = bisection(f, a, b, tol, maxIter)
% BISECTION Root-finding via bisection method
%   [root, iter] = bisection(f, a, b, tol, maxIter)

% initial guess
an = a;
bn = b;
fa = f(an);
fb = f(bn);
if fa*fb > 0
  error('No sign change in interval [%f, %f].', an, bn);
end

% iteration to narrow down the interval
for iter = 1:maxIter
  % evaluate the midpoint
  m = (an + bn)/2;
  fm = f(m);

  if abs(fm) < tol || (bn-an) < tol
    % convergence condition
    break;
  end
  if fa*fm < 0
    % choose the left half
    bn = m;
    fb = fm;
  else
    % choose the right half
    an = m;
    fa = fm;
  end
end

root = (an+bn)/2;
end
