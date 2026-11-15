% bemio_futi_19body.m — W6: BEMIO generation of futi_19body.h5 (19-body, GATE-B)
%
% STATUS: REV 1 (2026-11-15). First run on Saber's MATLAB R2025a Update 1
% (25.1.0.2973910): readAQWA SUCCEEDED in 252.8 s; frequency grid (47 pts,
% 0.02–2.10 rad/s) and headings (25) checks passed; the run then stopped at
% this script's own filename assert BEFORE any IRF work. Root cause was a
% wrong assumption in the original draft: in the local BEMIO, hydro.file is
% the BASE name without extension (readAQWA set it to 'futi_19body') and
% writeBEMIOH5 writes to [hydro.file '.h5'] — verified against the WEC-Sim
% source of writeBEMIOH5.m (filename = [hydro.file '.h5']; body-count field
% is hydro.Nb, not hydro.Nbodies). REV 1 fixes the filename handling and
% the body-count check (hydro.Nb), and adds an after-read checkpoint save.
% The IRF and write stages are still UNRUN. This environment has no MATLAB,
% so the script must be run on Saber's local MATLAB and its console log +
% .h5 returned for GATE-B review.
%
% INPUTS (put this script in the same folder as the two files, or edit §0):
%   futi_19body.AH1   (21,146,564 B, AQWA-Line 2022 R1, run 2026-11-11)
%   FUTI_19BODY.LIS   (89,926,233 B, same run; in the repo it lives only as a
%                      Release asset — the local original is the BEMIO input)
% OUTPUTS:
%   futi_19body.h5        (the WEC-Sim hydro file; filename is the 19-body
%                         口径 — the plan book's `futi_22body.h5` is 22-body
%                         口径 and must NOT be used)
%   futi_19body_hydro.mat (the `hydro` struct, saved before writing the .h5,
%                          so GATE-B review can re-run without re-doing IRFs)
%   futi_19body_hydro_after_read.mat (checkpoint right after readAQWA, so a
%                          later failure does not force a blind re-read)
%   bemio_futi_19body_log.txt (diary of the console output)
%
% CHAIN (plan book §W6, 22-body wording adapted to the executed 19-body
% scheme; WEC-Sim BEMIO docs, checked 2026-11-13,
% https://wec-sim.github.io/WEC-Sim/main/user/advanced_features.html):
%   readAQWA(hydro, ah1, lis) -> radiationIRF -> excitationIRF -> writeBEMIOH5
%   * readAQWA(hydro, ah1Filename, lisFilename) — normalisation is applied
%     inside readAQWA; no separate normalizeBEM call.
%   * radiationIRF(hydro, tEnd, nDt, nDw, wMin, wMax) and
%     excitationIRF(hydro, ...) — all five trailing arguments are passed as
%     [] here, i.e. BEMIO defaults (tEnd 100 s, nDt/nDw 1001, wMin/wMax =
%     the BEM data limits). For this run that means w = 0.02–2.10 rad/s,
%     47 frequencies, 25 headings — the same grid the AH1 was verified on.
%   * radiationIRFSS is deliberately NOT called: the plan-book chain has no
%     state-space step, and WEC-Sim defaults to convolution (stateSpace = 0).
%     Add it only as a separate, recorded decision if W7 needs it.
%   * writeBEMIOH5(hydro) writes to [hydro.file '.h5'] (WEC-Sim source,
%     verified 2026-11-15). readAQWA sets hydro.file to the AH1 base name
%     ('futi_19body'); the script asserts that base name and derives the
%     final .h5 filename from it. Body count field is hydro.Nb.
%
% BODY ORDER (W1,复原版 — the single authority; do NOT reorder):
%   1 central column; then per chain 180° -> 60° -> 300°, five pontoon
%   segments inner->outer + outer column. I.e. 1 = central, 2–7 = 180° chain
%   (segments 1–5, outer column), 8–13 = 60° chain, 14–19 = 300° chain.
%   Full table (CoG / panels): design-basis-w1-w2/w1-segmentation-scheme-19body.md
%   Total: 19 bodies, 19^2 = 361 added-mass/damping coupling blocks,
%   114 DOF, DIFF panels 5,454. The script checks Nbodies == 19 after the
%   read (when the field exists) and prints the frequency/heading grid.
%
% Ainf / LHFR (known open point — see AGENTS.md §4.3 and route V2.5 §5):
%   This AQWA run was made with LHFR OFF, so the .AH1 carries no FIDD
%   (infinite-frequency added mass). Per the plan book (verified against
%   WEC-Sim source when the plan was written), readAQWA does not read FIDD
%   and Ainf is recomputed by radiationIRF. After the run, record what
%   hydro.Ainf contains and confirm it in the GATE-B record; do not assume.
%
% GATE-B REVIEW (after this script runs — not part of this script):
%   Compare the .h5 synthesised excitation against the corr+ reference in
%   gate-a-verification/excitation-full-spectrum.csv / .npz (Fsyn_corr_plus).
%   Criteria: amplitude < 1%, phase < 1°. corr+ is the adjudicated correct
%   sign (sign-adjudication-record.md, 2026-11-13: median complex error
%   0.102%, phase 0.004° vs the overall single-body LIS benchmark); a .h5
%   that disagrees with corr+ is a BEMIO-side problem, not a sign question.
%   Also re-check the ω ≤ 0.15 low-frequency moment residual band
%   (≤ ~5% of peak, variant-independent; see the adjudication record §4)
%   in the same band, for the thesis limitations section.
%
% REVIEW PASS on this draft (thesis rule: review before output, 2026-11-13):
%   - Function names/signatures re-checked against the WEC-Sim BEMIO docs
%     above (readAQWA / radiationIRF / excitationIRF / writeBEMIOH5).
%   - Body count, frequency/heading grid, file names and sizes re-checked
%     against futi_19body.AH1 / FUTI_19BODY.LIS and synthesis_results.json
%     (Mtot 17,854.06 t, 47 freqs, 25 headings).
%   - REV 1 (2026-11-15): `hydro.file` / `hydro.Nb` conventions verified
%     against the WEC-Sim source (writeBEMIOH5.m) and the first local run
%     (readAQWA 252.8 s on R2025a Update 1; grid/headings checks passed).
%     Still NOT verified by execution: the radiationIRF / excitationIRF /
%     writeBEMIOH5 stages and runtime/memory for 361 coupling blocks. The
%     script therefore uses isfield-guarded checks and fails loudly
%     instead of silently assuming. Record the actual runtime.
%   - Filename uses underscores because a MATLAB script file with hyphens
%     cannot be run by name; this is the one exception to the repo's
%     kebab-case naming rule (AGENTS.md §6).

%% 0. Paths — edit only these three lines if the files live elsewhere
ah1File = 'futi_19body.AH1';
lisFile = 'FUTI_19BODY.LIS';
h5Base  = 'futi_19body';        % hydro.file base name (no extension)
h5File  = 'futi_19body.h5';     % final file written by writeBEMIOH5

diary('bemio_futi_19body_log.txt');
fprintf('=== W6 BEMIO: futi_19body.h5 — 19-body, GATE-B ===\n');
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
    fprintf('Nb = %d (expected 19)\n', hydro.Nb);
    assert(hydro.Nb == 19, 'Nb is %d, expected 19 — body order/count mismatch. STOP.', hydro.Nb);
elseif isfield(hydro, 'Nbodies')
    fprintf('Nbodies = %d (expected 19)\n', hydro.Nbodies);
    assert(hydro.Nbodies == 19, 'Nbodies is %d, expected 19 — body order/count mismatch. STOP.', hydro.Nbodies);
elseif isfield(hydro, 'body')
    fprintf('hydro.body count = %d (expected 19)\n', numel(hydro.body));
    assert(numel(hydro.body) == 19, 'hydro.body count is %d, expected 19. STOP.', numel(hydro.body));
else
    warning('No Nb/Nbodies/body field found — verify body count (19) manually from the printed struct.');
    disp(fieldnames(hydro));
end
if isfield(hydro, 'dof')
    fprintf('Total DOF = %d (expected 114 = 19 x 6)\n', sum(hydro.dof));
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
save('futi_19body_hydro_after_read.mat', 'hydro', '-v7.3');
fprintf('Checkpoint saved: futi_19body_hydro_after_read.mat\n');

%% 2. Radiation + excitation IRFs (BEMIO defaults: [] = 100 s / 1001 / 1001 / data limits)
% 19 bodies = 361 coupling blocks; this step is the long one — record the time.
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
save('futi_19body_hydro.mat', 'hydro', '-v7.3');
fprintf('Saved hydro struct to futi_19body_hydro.mat\n');

fprintf('Writing .h5 to: %s\n', h5File);
tWrite = tic;
writeBEMIOH5(hydro);
fprintf('writeBEMIOH5 done in %.1f s.\n', toc(tWrite));
assert(exist(h5File, 'file') == 2, '.h5 file was not created: %s', h5File);
fprintf('.h5 created: %s (%d bytes)\n', h5File, dir(h5File).bytes);

fprintf('=== DONE. Return futi_19body.h5 + this log + futi_19body_hydro.mat for GATE-B review. ===\n');
fprintf('GATE-B anchor: corr+ reference, excitation-full-spectrum.csv/.npz (Fsyn_corr_plus); criteria amplitude <1%%, phase <1%%.\n');
diary off;
