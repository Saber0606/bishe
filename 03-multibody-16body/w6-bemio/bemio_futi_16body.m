% bemio_futi_16body.m — W6: BEMIO generation of futi_16body.h5 (16-body, GATE-B)
%
% STATUS: Prepared 2026-11-16, after 16-body GATE-A closed (see
% 03-multibody-16body/gate-a-verification/gate-a-verification-record-16body.md).
% Adapted from the executed 19-body script bemio_futi_19body.m REV 1
% (03-multibody-19body/w6-bemio/), which ran to completion on Saber's
% MATLAB R2025a Update 1 (25.1.0.2973910) on 2026-11-15 and passed
% GATE-B. All REV 1 lessons are carried over: hydro.file is the BASE
% name without extension (writeBEMIOH5 writes [hydro.file '.h5'],
% verified against the WEC-Sim source), the body-count field is
% hydro.Nb, and a checkpoint .mat is saved right after readAQWA.
% This environment has no MATLAB, so the script must be run on Saber's
% local MATLAB and its console log + .h5 + hydro.mat returned for
% GATE-B review.
%
% INPUTS (put this script in the same folder as the two files, or edit §0):
%   futi_16body.AH1   (15,506,571 B, MD5 cb2d1c44..., AQWA-Line 2022 R1,
%                      run 2026-11-16 20:33; GATE-A verified)
%   futi_16body.LIS   (70,936,631 B, MD5 fb9bdf57..., same run; in the
%                      repo it lives only as a Release asset — use the
%                      local original; note the run's original name was
%                      FUTI_16BODY.LIS, rename the copy to futi_16body.LIS
%                      or edit §0)
% OUTPUTS:
%   futi_16body.h5        (the WEC-Sim hydro file)
%   futi_16body_hydro.mat (the `hydro` struct, saved before writing the
%                          .h5, so GATE-B review can re-run without
%                          re-doing IRFs)
%   futi_16body_hydro_after_read.mat (checkpoint right after readAQWA)
%   bemio_futi_16body_log.txt (diary of the console output)
%
% CHAIN (plan book §W6, adapted to the executed 16-body scheme;
% WEC-Sim BEMIO docs https://wec-sim.github.io/WEC-Sim/main/user/advanced_features.html):
%   readAQWA(hydro, ah1, lis) -> radiationIRF -> excitationIRF -> writeBEMIOH5
%   * Normalisation is applied inside readAQWA; no separate normalizeBEM.
%   * radiationIRF / excitationIRF trailing arguments are all [] here,
%     i.e. BEMIO defaults (tEnd 100 s, nDt/nDw 1001, wMin/wMax = data
%     limits): w = 0.02–2.10 rad/s, 47 frequencies, 25 headings — the
%     grid GATE-A was verified on.
%   * radiationIRFSS is deliberately NOT called (convolution default,
%     stateSpace = 0), same as the 19-body run. Add it only as a
%     separate, recorded decision if W7 needs it.
%
% BODY ORDER (W1 v2 — the single authority; do NOT reorder):
%   1 = central column; 180° chain: 2–5 = segments S1–S4 (inner->outer),
%   6 = outer column; 60° chain: 7–10 = S1–S4, 11 = outer column;
%   300° chain: 12–15 = S1–S4, 16 = outer column.
%   Total: 16 bodies, 16^2 = 256 added-mass/damping coupling blocks,
%   96 DOF, DIFF panel pieces 5,651.
%
% Ainf / LHFR: this AQWA run had LHFR OFF; the .AH1 FIDD block is
% present but all-zero. In the 19-body run readAQWA did not use FIDD
% and Ainf was recomputed by radiationIRF (confirmed by the run log
% and GATE-B review). After the run, record what hydro.Ainf contains
% and confirm it in the GATE-B record; do not assume.
%
% GATE-B REVIEW (after this script runs — not part of this script):
%   BEMIO excitation convention (19-body finding, source-verified):
%   F_h5 = conj(F_AH1) .* exp(-i*k*(x_G cos th + y_G sin th)) per body —
%   invert it BEFORE comparing with FORCERAO, otherwise a bogus ~124%
%   median error appears. Synthesised excitation is compared against
%   the GATE-A corr+ anchor (gate-a-verification/
%   excitation-full-spectrum-16body.npz, Fsyn_corr_plus).
%   Criteria (along 19-body GATE-B): synthesised vs anchor amplitude
%   max < 1%, phase max < 1°; A/B matrices vs AH1 at 1e-7 level;
%   Ainf rigid synthesis vs NREL Table 4 within ±2.5%; also re-check
%   the omega <= 0.15 low-frequency moment residual band in the
%   .h5 <-> AH1 comparison (GATE-A record §4: it is expected NOT to
%   reproduce there; 19-body band max amplitude error was 0.0018%).
%
% REVIEW PASS on this draft (thesis rule: review before output):
%   - Derived from the executed 19-body REV 1 script by mechanical
%     substitution of names/counts only; the code body is otherwise
%     byte-identical in logic (asserts updated: Nb 16, DOF 96).
%   - Input sizes/MD5s re-checked against the local run products
%     (run-products-20261116) on 2026-11-16; body order re-checked
%     against the AH1 COG block (body 2 = (-12.160, 0, -16.500) etc.).
%   - Filename uses underscores because a MATLAB script file with
%     hyphens cannot be run by name; this is the one exception to the
%     repo's kebab-case naming rule (AGENTS.md §6).

%% 0. Paths — edit only these three lines if the files live elsewhere
ah1File = 'futi_16body.AH1';
lisFile = 'futi_16body.LIS';
h5Base  = 'futi_16body';        % hydro.file base name (no extension)
h5File  = 'futi_16body.h5';     % final file written by writeBEMIOH5

diary('bemio_futi_16body_log.txt');
fprintf('=== W6 BEMIO: futi_16body.h5 — 16-body, GATE-B ===\n');
fprintf('Run started: %s\n', datestr(now, 'yyyy-mm-dd HH:MM:SS'));
fprintf('MATLAB: %s\n', version);
fprintf('Inputs: %s / %s\n', ah1File, lisFile);

assert(exist(ah1File, 'file') == 2, 'AH1 file not found: %s', ah1File);
assert(exist(lisFile, 'file') == 2, 'LIS file not found: %s', lisFile);
fprintf('Input files found. AH1 bytes: %d; LIS bytes: %d\n', ...
    dir(ah1File).bytes, dir(lisFile).bytes);

%% 1. Read AQWA output (normalisation is applied inside readAQWA)
tRead = tic;
hydro = struct();
hydro = readAQWA(hydro, ah1File, lisFile);
fprintf('readAQWA done in %.1f s.\n', toc(tRead));

% Body count / grid — the local BEMIO uses hydro.Nb (writeBEMIOH5 loops
% over 1:hydro.Nb); fall back to Nbodies, then to counting hydro.body.
if isfield(hydro, 'Nb')
    fprintf('Nb = %d (expected 16)\n', hydro.Nb);
    assert(hydro.Nb == 16, 'Nb is %d, expected 16 — body order/count mismatch. STOP.', hydro.Nb);
elseif isfield(hydro, 'Nbodies')
    fprintf('Nbodies = %d (expected 16)\n', hydro.Nbodies);
    assert(hydro.Nbodies == 16, 'Nbodies is %d, expected 16 — body order/count mismatch. STOP.', hydro.Nbodies);
elseif isfield(hydro, 'body')
    fprintf('hydro.body count = %d (expected 16)\n', numel(hydro.body));
    assert(numel(hydro.body) == 16, 'hydro.body count is %d, expected 16. STOP.', numel(hydro.body));
else
    warning('No Nb/Nbodies/body field found — verify body count (16) manually from the printed struct.');
    disp(fieldnames(hydro));
end
if isfield(hydro, 'dof')
    fprintf('Total DOF = %d (expected 96 = 16 x 6)\n', sum(hydro.dof));
end
if isfield(hydro, 'w')
    fprintf('Frequency grid: %d points, %.4g to %.4g rad/s (expected 47, 0.02–2.10)\n', ...
        numel(hydro.w), min(hydro.w), max(hydro.w));
    assert(numel(hydro.w) == 47, 'Frequency count is %d, expected 47. STOP.', numel(hydro.w));
end
if isfield(hydro, 'theta')
    fprintf('Headings: %d (expected 25)\n', numel(hydro.theta));
end
if isfield(hydro, 'Ainf')
    fprintf('Ainf present after readAQWA (size below; note its values for the GATE-B record; LHFR was OFF).\n');
    fprintf('size(hydro.Ainf) = %s\n', mat2str(size(hydro.Ainf)));
    if numel(hydro.Ainf) >= 36
        disp(hydro.Ainf(1:6, 1:6));
    else
        disp(hydro.Ainf);
    end
end

% Output filename: settle it NOW (before the long IRF steps). In this
% BEMIO version hydro.file is the BASE name and writeBEMIOH5 writes to
% [hydro.file '.h5'] (source-verified 2026-11-15). readAQWA set it from
% the AH1 name; assert the base name, not the full .h5 filename.
if ~isfield(hydro, 'file') || isempty(hydro.file)
    hydro.file = h5Base;
end
fprintf('hydro.file (base name) = %s -> output .h5 will be: %s\n', hydro.file, [hydro.file '.h5']);
assert(strcmp(hydro.file, h5Base), 'hydro.file is %s, expected base name %s — check the local BEMIO version before continuing. STOP.', hydro.file, h5Base);
assert(strcmp([hydro.file '.h5'], h5File), 'Derived output name %s ~= expected %s. STOP.', [hydro.file '.h5'], h5File);

% Checkpoint: save the post-read hydro struct so that if an IRF/write step
% fails, the 4-minute readAQWA does not have to be repeated blindly —
% keep this file and report the failure first.
save('futi_16body_hydro_after_read.mat', 'hydro', '-v7.3');
fprintf('Checkpoint saved: futi_16body_hydro_after_read.mat\n');

%% 2. Radiation + excitation IRFs (BEMIO defaults: [] = 100 s / 1001 / 1001 / data limits)
% 16 bodies = 256 coupling blocks; this step is the long one — record the time.
tIrf = tic;
hydro = radiationIRF(hydro, [], [], [], [], []);
fprintf('radiationIRF done in %.1f s.\n', toc(tIrf));
tIrf = tic;
hydro = excitationIRF(hydro, [], [], [], [], []);
fprintf('excitationIRF done in %.1f s.\n', toc(tIrf));
if isfield(hydro, 'Ainf')
    fprintf('Ainf after radiationIRF (for the GATE-B record):\n');
    fprintf('size(hydro.Ainf) = %s\n', mat2str(size(hydro.Ainf)));
    if numel(hydro.Ainf) >= 36
        disp(hydro.Ainf(1:6, 1:6));
    else
        disp(hydro.Ainf);
    end
end

%% 3. Save the hydro struct first, then write the .h5
save('futi_16body_hydro.mat', 'hydro', '-v7.3');
fprintf('Saved hydro struct to futi_16body_hydro.mat\n');

fprintf('Writing .h5 to: %s\n', h5File);
tWrite = tic;
writeBEMIOH5(hydro);
fprintf('writeBEMIOH5 done in %.1f s.\n', toc(tWrite));
assert(exist(h5File, 'file') == 2, '.h5 file was not created: %s', h5File);
fprintf('.h5 created: %s (%d bytes)\n', h5File, dir(h5File).bytes);

fprintf('=== DONE. Return futi_16body.h5 + this log + futi_16body_hydro.mat for GATE-B review. ===\n');
fprintf('GATE-B anchor: corr+ reference, excitation-full-spectrum-16body.csv/.npz (Fsyn_corr_plus); criteria amplitude <1%%, phase <1%%.\n');
diary off;
