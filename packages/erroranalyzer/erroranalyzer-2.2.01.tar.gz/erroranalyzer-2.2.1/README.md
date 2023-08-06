# erroranalyzer

This package is a Python wrapper to call the `ErrorAnalyzer` shared library.

---

To import the package with the necessary functions and classes write:

```
from erroranalyzer import eaAnalyzer, eaAnalyzersFinal
```


Creating your first analyzer is as easy as doing:

```
# Create the first analyzer, 8 Bit, unsigned
my_analyzer = eaAnalyzer("Analyzer 1", 8, False)
```

To add samples to your analyzer call the function:

```
my_analyzer.add_sample(data_read=1, data_expected=2, time=1000)
```

At the end print the final report:

```
eaAnalyzersFinal()
```

# Environment Variables

Set `EA_ROOT` to point to the directory containing the license file. Otherwise the trial version will be used.

Set `EA_CONFIG` to point to the directory containing the config file. Otherwise the standard configuration will be used.
