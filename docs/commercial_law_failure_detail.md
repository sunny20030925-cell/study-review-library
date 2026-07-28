# Commercial law deployment failure detail

run_id=30344547335
run_url=https://github.com/sunny20030925-cell/study-review-library/actions/runs/30344547335
gh_log_exit=0

```text
deploy	Download and verify website package	﻿2026-07-28T17:38:54.8955623Z ##[group]Run curl -L --fail --retry 3 \
deploy	Download and verify website package	2026-07-28T17:38:54.8956925Z ^[[36;1mcurl -L --fail --retry 3 \^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.8959226Z ^[[36;1m  'https://drive.usercontent.google.com/download?id=1rgPS62bIZOWC8H3zSrw-RBZ3jkg9SDcs&export=download&confirm=t' \^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.8961771Z ^[[36;1m  -o site.zip^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.8963703Z ^[[36;1mecho '12b9e8f2639ac8b27157e456a985c905d91e590f88465ebf8c4b5786846f3774  site.zip' | sha256sum --check -^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.8965816Z ^[[36;1mmkdir _site^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.8966776Z ^[[36;1mpython -m zipfile -e site.zip _site^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.8967942Z ^[[36;1mrm -rf _site/.github^[[0m
deploy	Download and verify website package	2026-07-28T17:38:54.9023620Z shell: /usr/bin/bash -e {0}
deploy	Download and verify website package	2026-07-28T17:38:54.9024606Z env:
deploy	Download and verify website package	2026-07-28T17:38:54.9025347Z   GITHUB_PAGES: true
deploy	Download and verify website package	2026-07-28T17:38:54.9026202Z ##[endgroup]
deploy	Download and verify website package	2026-07-28T17:38:54.9186268Z   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
deploy	Download and verify website package	2026-07-28T17:38:54.9188541Z                                  Dload  Upload   Total   Spent    Left  Speed
deploy	Download and verify website package	2026-07-28T17:38:54.9189740Z 
deploy	Download and verify website package	2026-07-28T17:38:56.1270845Z   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
deploy	Download and verify website package	2026-07-28T17:38:57.1283320Z   0     0    0     0    0     0      0      0 --:--:--  0:00:01 --:--:--     0
deploy	Download and verify website package	2026-07-28T17:38:58.1294038Z   0     0    0     0    0     0      0      0 --:--:--  0:00:02 --:--:--     0
deploy	Download and verify website package	2026-07-28T17:38:58.4506030Z   0     0    0     0    0     0      0      0 --:--:--  0:00:03 --:--:--     0
deploy	Download and verify website package	2026-07-28T17:38:58.4507115Z 100 1346k  100 1346k    0     0   381k      0  0:00:03  0:00:03 --:--:--  381k
deploy	Download and verify website package	2026-07-28T17:38:58.4567418Z sha256sum: WARNING: 1 computed checksum did NOT match
deploy	Download and verify website package	2026-07-28T17:38:58.4567942Z site.zip: FAILED
deploy	Download and verify website package	2026-07-28T17:38:58.4583378Z ##[error]Process completed with exit code 1.
```
