function validateResults(time, altitude, velocity, acceleration, apogee_time)
% VALIDATERESULTS Check physical constraints and error metrics

fprintf('\n--- Validation Checks ---\n');

% 1. Check Velocity at Apogee (should be approx 0)
% Find velocity at apogee time
v_apogee = interp1(time, velocity, apogee_time);
fprintf('1. Velocity at Apogee: %.4f m/s (Expected ~0)\n', v_apogee);

if abs(v_apogee) < 1.0
  fprintf('   [PASS] Velocity is close to zero.\n');
else
  fprintf('   [WARN] Velocity deviation is high.\n');
end

% 2. Check Acceleration at Apogee (should be approx -g = -9.81)
% Assuming drag is negligible at v=0
a_apogee = interp1(time, acceleration, apogee_time);
fprintf('2. Acceleration at Apogee: %.4f m/s^2 (Expected ~ -9.81)\n', a_apogee);

if abs(a_apogee + 9.81) < 2.0
  fprintf('   [PASS] Acceleration is consistent with gravity.\n');
else
  fprintf('   [WARN] Acceleration deviation is high.\n');
end

% 3. Check Initial Conditions
fprintf('3. Initial Altitude: %.2f m\n', altitude(1));
fprintf('   Initial Velocity: %.2f m/s\n', velocity(1));

end
