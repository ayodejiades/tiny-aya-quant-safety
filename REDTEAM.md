# Red team: standing attacks A1 to A13

Each attack from `researchops/rules/redteam_standing.md`, answered against this project. Status: fixed, limited or rejected.

### A1: What decision changes, and for whom, if this result is true?
Status: fixed
Response: Anyone shipping Tiny Aya on-device can keep the official q4_k_m file without expecting lost refusals on this test, should treat q4_0 as an over-refusal risk and Q2_K as a safety and accuracy risk, and should not assume that protecting a block of layers is a cheap repair. Stated in the Abstract and Discussion.

### A2: Where is the positive control, what number did it give, and is it in Results?
Status: fixed
Response: f16 refuses harmful dev prompts 73.3 points more often than benign ones (minimum 20). It opens Results, with the Q2_K sensitivity control beside it.

### A3: Does any comparison change more than one variable at once?
Status: limited
Response: F1 against Q3_K_S changes both bits per weight and which layers are protected; the decoy F2 has the same size as F1, so F1 against F2 isolates layer choice. q4_0 against q4_k_m differs in quantization scheme as well as bit width. Both are noted in Results and Limitations.

### A4: Could the headline be an artefact of a token cap, truncation, parser, prompt format or judge?
Status: limited
Response: Yes, partly. The 128-token cap truncated about nine in ten benign and wrapped responses, the refusal detector reads the first sentence only, and Llama Guard judged partial text; truncation rates per arm are reported and ASR is described as probably an undercount. The default system preamble is identical for every arm. The cap was frozen in the preregistration and cannot be changed without a rerun.

### A5: Does the abstract state anything that Limitations takes back or narrows?
Status: fixed
Response: The abstract states the cuts, the wide intervals and the cap. Limitations adds scope sentences ("This does not establish ...") but does not contradict the abstract.

### A6: Do the prereg URL and code URL load, and does the code reproduce the headline numbers?
Status: fixed
Response: Both load logged out. `rops-guard check` re-runs the analysis scripts in a temporary copy and reproduces the claims table. The repository has no model outputs; the logs dataset has them (unsafe ones truncated). The prereg tag was recreated after a history rewrite to remove a personal email; hashes are mapped in `DEVIATIONS.md` D7.

### A7: What was built or run before the weekend, and is it disclosed?
Status: fixed
Response: The `rops` checking tools are the author's own earlier tooling, disclosed under Reproduction. The experiment design and executor guide were written by Claude Fable before the run, disclosed in the LLM usage statement.

### A8: If an LLM judge scored anything, what is its agreement with hand labels?
Status: limited
Response: Llama Guard 3 and the keyword detector are compared with 60 blind hand labels by Cohen's kappa. The hand labels were not yet complete when this file was written, so kappa is pending. Llama Guard was also called with a corrected prompt (`DEVIATIONS.md` D6), because the default Ollama template grades the prompt, not the response.

### A9: How many seeds or samples per cell, and is variance reported?
Status: limited
Response: One seed, temperature 0, one sample per prompt, 69 to 70 prompts per cell. Wilson intervals are reported for every rate and are wide; paired exact tests are used for comparisons. More seeds would not add information at temperature 0, but more prompts would; XSTest was cut for time.

### A10: Does every reported metric have a scale a non-specialist can read?
Status: fixed
Response: Rates are percentages of a stated number of prompts; flip rate is the percentage of 139 prompts whose refusal label differs from f16; units are given in the Metrics section.

### A11: Does Methods describe exactly what ran, with settings identical to configs/?
Status: limited
Response: Server flags, seeds and the rendered prompt are exact. `configs/experiment.json` is frozen and still lists the XSTest sets, six layer blocks and wrapper W2; the speed rule removed these and the changes are logged in `DEVIATIONS.md` D5. Methods describes what ran.

### A12: Is any section a second paper that should be cut?
Status: rejected
Response: The wrapper result and the over-refusal result are short and share the arms, metrics and judge of the main question; there is no separate method.

### A13: Which three paragraphs read most like generated text, and did a human rewrite each one in their own words?
Status: limited
Response: The whole draft was written by Claude Sonnet 5.5 (disclosed). The author has not yet rewritten the three most generated-sounding paragraphs (the Discussion, the abstract's second paragraph and the Limitations opening); that edit is the author's to make before submitting.
