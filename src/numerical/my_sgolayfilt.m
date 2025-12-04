function y_smooth = my_sgolayfilt(y, order, framelen)
% MY_SGOLAYFILT Custom implementation of Savitzky-Golay filter
%   y_smooth = my_sgolayfilt(y, order, framelen)
%
%   y        : Input data vector
%   order    : Polynomial order
%   framelen : Frame length (must be odd)

if mod(framelen, 2) == 0
    error('Frame length must be odd.');
end

half_win = (framelen - 1) / 2;
n = length(y);
y_smooth = zeros(size(y));

% Compute coefficients (Gram polynomial approach simplified)
% We fit a polynomial of 'order' to 'framelen' points centered at 0
% The smoothed value is the value of the polynomial at 0

% Construct Vandermonde matrix for the window
x = (-half_win:half_win)';
V = zeros(framelen, order + 1);
for i = 0:order
    V(:, i+1) = x.^i;
end

% Projection matrix: H = V * (V'*V)^-1 * V'
% We only need the row corresponding to x=0 (center point)
% The coefficients for the center point are the middle row of H
[Q, R] = qr(V, 0);
% H = Q * Q'
% Center row index is half_win + 1
coeffs = Q(half_win + 1, :) * Q';

% Convolve with the coefficients
% Handle boundaries by shrinking window or replicating (simple approach: replicate)
% Manual padding (replicate border values)
y_col = y(:);
pad_pre = repmat(y_col(1), half_win, 1);
pad_post = repmat(y_col(end), half_win, 1);
y_pad = [pad_pre; y_col; pad_post];

% Apply filter
y_smooth_col = conv(y_pad, coeffs, 'valid');

% Reshape to match input
if isrow(y)
    y_smooth = y_smooth_col';
else
    y_smooth = y_smooth_col;
end
end
