#!/usr/bin/env python
import subprocess
from htcondor_dag import job, autorun

# Note: you can't set input=None because this is where htcondor_dag.py
# stores the picked arguments to call the function
@job(output=None,arguments=["one","\"two\"","spacey 'quoted' argument"],environment={"one":1,"two":'"2"',"three":"spacey 'quoted' value"})
def bash(cmd):
    subprocess.check_call(["/bin/bash","-c","set -o pipefail; " + cmd])

autorun()

j1 = bash.queue("tr 'a-z' 'A-Z' </etc/passwd >tmp1")
j2 = bash.queue("tr 'a-z' 'A-Z' </etc/hosts >tmp2")
j3 = bash.queue("cat tmp1 tmp2 >tmp.out").parent(j1, j2).var(job_files="tmp1,tmp2")
