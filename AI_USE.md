# AI-use disclosure

- Tool/model used, or `No AI assistance`: OpenAI ChatGPT (GPT-6).
- Tasks for which help was used: reviewing the supplied lab instructions and source files; implementing and debugging the four functions; constructing notebook analysis, CSV outputs, plots, report wording and reproduction metadata.
- Material you changed or rejected: the initial parser implementation was corrected after public tests exposed a title/prose separator error; a further boundary review corrected chapter extraction so prose stops at the next chapter heading. No raw input data were changed.
- Independent checks you performed: executed all 13 public unit tests; manually checked Journey Chapter I counts against retained prose; checked final cumulative values against chapter-matrix column sums; inspected extracted chapter records and generated tables. The execution runtime was Python 3.13.5, not Python 3.12.
