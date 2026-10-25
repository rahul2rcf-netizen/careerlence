# Scoring methodology

The displayed score is `100 × (0.60R + 0.15P + 0.25T)`, where `R` and `P` are distinct required/preferred taxonomy-skill coverage fractions, and `T` is TF-IDF cosine similarity between the complete resume and job text. Components are each in `[0,1]`; hence the total is `[0,100]`. A group with no detected requirements has zero coverage. Empty input is rejected; zero-vector text similarity is zero.

This is a transparent baseline, not a calibrated hiring score. A skill mention is only text evidence, not verification. Dictionary omissions, section parsing, synonym gaps, boilerplate, and text length can affect results. Candidates should inspect evidence and apparent gaps before acting.

