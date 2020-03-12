
import tag_ripper
import job_count
import subprocess
import os

def main():
    p = subprocess.Popen(tag_ripper)
    p.wait()
    p = subprocess.Popen(job_count)
    p.wait()

main()