#!/usr/bin/env python3
from __future__ import annotations

import sys

from record_study_library_deployment import main


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: python deploy/record_econometrics_v2_deployment.py SITE_ROOT")
    main(sys.argv[1])
