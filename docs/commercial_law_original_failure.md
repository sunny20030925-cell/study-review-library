# Original commercial law deployment failure

gh_log_exit=0

```text
deploy	UNKNOWN STEP	﻿2026-07-28T08:58:03.1052966Z Current runner version: '2.336.0'
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1071637Z ##[group]Runner Image Provisioner
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1072381Z Hosted Compute Agent
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1072839Z Version: 20260707.563
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1073391Z Commit: 02667638d2b423fbc733a8e32a88b44996a3ba6e
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1073970Z Build Date: 2026-07-07T19:33:50Z
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1075007Z Worker ID: {fc0f3a7f-c08d-4342-9bd0-547297b5fd93}
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1075629Z Azure Region: westus3
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1076094Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1077500Z ##[group]Operating System
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1078006Z Ubuntu
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1078415Z 24.04.4
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1078887Z LTS
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1079302Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1079743Z ##[group]Runner Image
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1080234Z Image: ubuntu-24.04
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1080691Z Version: 20260720.247.2
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1081746Z Included Software: https://github.com/actions/runner-images/blob/ubuntu24/20260720.247/images/ubuntu/Ubuntu2404-Readme.md
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1082948Z Image Release: https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20260720.247
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1083710Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1084734Z ##[group]GITHUB_TOKEN Permissions
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1086679Z Contents: read
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1087136Z Metadata: read
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1087598Z Pages: write
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1088036Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1089701Z Secret source: Actions
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1090566Z Prepare workflow directory
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1356280Z Prepare all required actions
deploy	UNKNOWN STEP	2026-07-28T08:58:03.1397914Z Getting action download info
deploy	UNKNOWN STEP	2026-07-28T08:58:03.4836451Z Download action repository 'actions/checkout@v4' (SHA:11d5960a326750d5838078e36cf38b85af677262)
deploy	UNKNOWN STEP	2026-07-28T08:58:04.3727736Z Download action repository 'actions/configure-pages@v5' (SHA:983d7736d9b0ae728b81ab479565c72886d7745b)
deploy	UNKNOWN STEP	2026-07-28T08:58:05.0349043Z Download action repository 'actions/upload-pages-artifact@v3' (SHA:56afc609e74202658d3ffba0e8f6dda462b719fa)
deploy	UNKNOWN STEP	2026-07-28T08:58:05.2762656Z Download action repository 'actions/deploy-pages@v4' (SHA:d6db90164ac5ed86f2b6aed7e0febac5b3c0c03e)
deploy	UNKNOWN STEP	2026-07-28T08:58:06.1094646Z Getting action download info
deploy	UNKNOWN STEP	2026-07-28T08:58:06.2360304Z Download action repository 'actions/upload-artifact@v4' (SHA:ea165f8d65b6e75b540449e92b4886f43607fa02)
deploy	UNKNOWN STEP	2026-07-28T08:58:06.4890781Z Complete job name: deploy
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5468111Z Node 20 is being deprecated. This workflow is running with Node 24 by default. If you need to temporarily use Node 20, you can set the ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true environment variable. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5473930Z ##[group]Run actions/checkout@v4
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5474532Z with:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5474775Z   ref: main
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5475117Z   repository: sunny20030925-cell/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5477239Z   token: ***
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5477525Z   ssh-strict: true
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5477813Z   ssh-user: git
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5478089Z   persist-credentials: true
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5478394Z   clean: true
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5478663Z   sparse-checkout-cone-mode: true
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5478962Z   fetch-depth: 1
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5479242Z   fetch-tags: false
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5479503Z   show-progress: true
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5479864Z   lfs: false
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5480103Z   submodules: false
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5480389Z   set-safe-directory: true
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5480682Z   allow-unsafe-pr-checkout: false
deploy	UNKNOWN STEP	2026-07-28T08:58:06.5481072Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:06.6345506Z Syncing repository: sunny20030925-cell/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:06.6347695Z ##[group]Getting Git version info
deploy	UNKNOWN STEP	2026-07-28T08:58:06.6348447Z Working directory is '/home/runner/work/study-review-library/study-review-library'
deploy	UNKNOWN STEP	2026-07-28T08:58:06.6349496Z [command]/usr/bin/git version
deploy	UNKNOWN STEP	2026-07-28T08:58:06.6999466Z git version 2.54.0
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7014484Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7027083Z Temporarily overriding HOME='/home/runner/work/_temp/c00c0996-0b2d-4b4c-a7e2-99df64973c1c' before making global git config changes
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7028414Z Adding repository directory to the temporary git global config as a safe directory
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7032035Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/study-review-library/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7059295Z Deleting the contents of '/home/runner/work/study-review-library/study-review-library'
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7062149Z ##[group]Initializing the repository
deploy	UNKNOWN STEP	2026-07-28T08:58:06.7065465Z [command]/usr/bin/git init /home/runner/work/study-review-library/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8025275Z hint: Using 'master' as the name for the initial branch. This default branch name
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8026294Z hint: will change to "main" in Git 3.0. To configure the initial branch name
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8027155Z hint: to use in all of your new repositories, which will suppress this warning,
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8027952Z hint: call:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8028439Z hint:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8028897Z hint: 	git config --global init.defaultBranch <name>
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8029303Z hint:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8030262Z hint: Names commonly chosen instead of 'master' are 'main', 'trunk' and
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8031056Z hint: 'development'. The just-created branch can be renamed via this command:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8031629Z hint:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8032019Z hint: 	git branch -m <name>
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8032426Z hint:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8032970Z hint: Disable this message with "git config set advice.defaultBranchName false"
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8033994Z Initialized empty Git repository in /home/runner/work/study-review-library/study-review-library/.git/
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8038055Z [command]/usr/bin/git remote add origin https://github.com/sunny20030925-cell/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8062261Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8062952Z ##[group]Disabling automatic garbage collection
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8066553Z [command]/usr/bin/git config --local gc.auto 0
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8088894Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8089632Z ##[group]Setting up auth
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8095037Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8119573Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8401105Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8426375Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8584553Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8609259Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8771715Z [command]/usr/bin/git config --local http.https://github.com/.extraheader AUTHORIZATION: basic ***
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8796595Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8797347Z ##[group]Fetching the repository
deploy	UNKNOWN STEP	2026-07-28T08:58:06.8804248Z [command]/usr/bin/git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6086043Z From https://github.com/sunny20030925-cell/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6086864Z  * [new branch]      main       -> origin/main
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6107039Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6107667Z ##[group]Determining the checkout info
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6115371Z [command]/usr/bin/git branch --list --remote origin/main
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6141487Z   origin/main
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6144752Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6149286Z [command]/usr/bin/git sparse-checkout disable
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6226543Z [command]/usr/bin/git config --local --unset-all extensions.worktreeConfig
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6329593Z ##[group]Checking out the ref
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6333413Z [command]/usr/bin/git checkout --progress --force -B main refs/remotes/origin/main
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6698649Z Switched to a new branch 'main'
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6699344Z branch 'main' set up to track 'origin/main'.
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6703194Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6730227Z [command]/usr/bin/git log -1 --format=%H
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6750344Z 9cf39f6070521f1fd1eb841c428bb20638ec2d58
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6919210Z Node 20 is being deprecated. This workflow is running with Node 24 by default. If you need to temporarily use Node 20, you can set the ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true environment variable. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6920547Z ##[group]Run actions/configure-pages@v5
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6920784Z with:
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6920962Z   enablement: true
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6922811Z   token: ***
deploy	UNKNOWN STEP	2026-07-28T08:58:07.6922986Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1120557Z ##[group]Run curl -L --fail --retry 3 \
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1120943Z ^[[36;1mcurl -L --fail --retry 3 \^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1121468Z ^[[36;1m  'https://drive.usercontent.google.com/download?id=1rgPS62bIZOWC8H3zSrw-RBZ3jkg9SDcs&export=download&confirm=t' \^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1121941Z ^[[36;1m  -o site.zip^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1122349Z ^[[36;1mecho '12b9e8f2639ac8b27157e456a985c905d91e590f88465ebf8c4b5786846f3774  site.zip' | sha256sum --check -^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1122770Z ^[[36;1mmkdir _site^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1122991Z ^[[36;1mpython -m zipfile -e site.zip _site^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1123236Z ^[[36;1mrm -rf _site/.github^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1150958Z shell: /usr/bin/bash -e {0}
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1151227Z env:
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1151430Z   GITHUB_PAGES: true
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1151628Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1251972Z   % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1254625Z                                  Dload  Upload   Total   Spent    Left  Speed
deploy	UNKNOWN STEP	2026-07-28T08:58:08.1255016Z 
deploy	UNKNOWN STEP	2026-07-28T08:58:09.1145080Z   0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
deploy	UNKNOWN STEP	2026-07-28T08:58:09.1676265Z   4 1263k    4 59490    0     0  60138      0  0:00:21 --:--:--  0:00:21 60090
deploy	UNKNOWN STEP	2026-07-28T08:58:09.1676975Z 100 1263k  100 1263k    0     0  1212k      0  0:00:01  0:00:01 --:--:-- 1212k
deploy	UNKNOWN STEP	2026-07-28T08:58:09.1723300Z site.zip: OK
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2319615Z ##[group]Run python -m pip install --disable-pip-version-check beautifulsoup4
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2320113Z ^[[36;1mpython -m pip install --disable-pip-version-check beautifulsoup4^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2320479Z ^[[36;1mpython deploy/patch_accounting_v2.py _site^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2320912Z ^[[36;1mcat deploy/patch-economics-v2.py.gz.b64.part* | base64 --decode > /tmp/patch-economics-v2.py.gz^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2321610Z ^[[36;1mecho 'b675b23d8711c75b2d736315b3161d5c2afc608d11e55249ec9ea5bd1e4d97fa  /tmp/patch-economics-v2.py.gz' | sha256sum --check -^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2322245Z ^[[36;1mgzip --decompress --stdout /tmp/patch-economics-v2.py.gz > /tmp/patch-economics-v2.py^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2322711Z ^[[36;1mSITE_ROOT="$GITHUB_WORKSPACE/_site" python /tmp/patch-economics-v2.py^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2346584Z shell: /usr/bin/bash -e {0}
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2346839Z env:
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2347020Z   GITHUB_PAGES: true
deploy	UNKNOWN STEP	2026-07-28T08:58:09.2347232Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:10.2842471Z Defaulting to user installation because normal site-packages is not writeable
deploy	UNKNOWN STEP	2026-07-28T08:58:11.5835685Z Collecting beautifulsoup4
deploy	UNKNOWN STEP	2026-07-28T08:58:11.6349462Z   Downloading beautifulsoup4-4.15.0-py3-none-any.whl.metadata (3.8 kB)
deploy	UNKNOWN STEP	2026-07-28T08:58:11.9548095Z Collecting soupsieve>=1.6.1 (from beautifulsoup4)
deploy	UNKNOWN STEP	2026-07-28T08:58:11.9646368Z   Downloading soupsieve-2.9.1-py3-none-any.whl.metadata (4.6 kB)
deploy	UNKNOWN STEP	2026-07-28T08:58:11.9686577Z Requirement already satisfied: typing-extensions>=4.0.0 in /usr/lib/python3/dist-packages (from beautifulsoup4) (4.10.0)
deploy	UNKNOWN STEP	2026-07-28T08:58:11.9793237Z Downloading beautifulsoup4-4.15.0-py3-none-any.whl (109 kB)
deploy	UNKNOWN STEP	2026-07-28T08:58:11.9966139Z    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 109.9/109.9 kB 7.1 MB/s eta 0:00:00
deploy	UNKNOWN STEP	2026-07-28T08:58:12.0061179Z Downloading soupsieve-2.9.1-py3-none-any.whl (37 kB)
deploy	UNKNOWN STEP	2026-07-28T08:58:12.4909049Z Installing collected packages: soupsieve, beautifulsoup4
deploy	UNKNOWN STEP	2026-07-28T08:58:12.5575237Z Successfully installed beautifulsoup4-4.15.0 soupsieve-2.9.1
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9814044Z {
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9814679Z   "changes": 29,
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9815021Z   "search_entries": 111,
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9815450Z   "questions": 70,
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9815808Z   "library_version": "2026.07.27-7",
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9816223Z   "accounting_version": "2026.07.27-2"
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9816625Z }
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9817265Z ('books/accounting/chapters/ch00.html', '修正五大要素定義')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9845830Z ('books/accounting/chapters/ch00.html', '五大分類措辭')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9856121Z ('books/accounting/chapters/ch06.html', '報表名稱')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9856910Z ('books/accounting/chapters/ch06.html', '損益表定義')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9857599Z ('books/accounting/chapters/ch06.html', '資產負債表名稱與分類')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9858332Z ('books/accounting/chapters/ch07.html', '進貨折扣方法前提')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9859049Z ('books/accounting/chapters/ch08.html', '存貨成本公式')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9859733Z ('books/accounting/chapters/ch08.html', '加權平均與移動平均')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9860438Z ('books/accounting/chapters/ch08.html', '存貨練習題措辭')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9861094Z ('books/accounting/chapters/ch08.html', '加權平均題目條件')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9862105Z ('books/accounting/chapters/ch09.html', '約當現金定義')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9961825Z ('books/accounting/chapters/ch09.html', '零用金短溢')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9962220Z ('books/accounting/chapters/ch10.html', '備抵方法目的')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9962594Z ('books/accounting/chapters/ch11.html', '折舊開始時點')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9962929Z ('books/accounting/chapters/ch11.html', '資產可供使用措辭')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9963256Z ('books/accounting/chapters/ch11.html', '土地折舊提醒')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9963576Z ('books/accounting/chapters/ch12.html', '流動負債定義')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9963905Z ('books/accounting/chapters/ch12.html', '股利宣告完整效果')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9964447Z ('books/accounting/chapters/ch13.html', '現金流量三分類')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9964883Z ('books/accounting/chapters/ch13.html', '間接法完整邏輯')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9965325Z ('books/accounting/chapters/ch13.html', '非現金交易提醒')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9966085Z ('books/accounting/chapters/appendix-a.html', '附錄存貨公式')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9966638Z ('books/accounting/chapters/appendix-c.html', '附錄報表中英對照')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9967143Z ('assets/accounting-svg/statements.svg', '報表圖名稱')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9967624Z ('assets/accounting-svg/inventory.svg', '存貨圖公式')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9968090Z ('assets/accounting-svg/cashflow.svg', '營業現金圖')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9968580Z ('assets/accounting-svg/cashflow.svg', '籌資現金圖')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9969079Z ('books/accounting/questions.json', '題庫精確化與版本')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9969475Z ('sw.js', 'service worker version')
deploy	UNKNOWN STEP	2026-07-28T08:58:12.9969852Z /tmp/patch-economics-v2.py.gz: OK
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1350029Z ECONOMICS_PATCH_OK version=2026.07.27-2 questions=100 search=144 corrections=14
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1473632Z ##[group]Run cat deploy/generate-commercial-law.py.gz.b64.part* | base64 --decode > /tmp/generate-commercial-law.py.gz
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1474516Z ^[[36;1mcat deploy/generate-commercial-law.py.gz.b64.part* | base64 --decode > /tmp/generate-commercial-law.py.gz^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1475229Z ^[[36;1mecho '85843044d6fee2f0c5d11208754a4d6b103402392d3a44511745a146874dcdfc  /tmp/generate-commercial-law.py.gz' | sha256sum --check -^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1475904Z ^[[36;1mgzip --decompress --stdout /tmp/generate-commercial-law.py.gz > /tmp/generate-commercial-law.py^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1476450Z ^[[36;1mpython /tmp/generate-commercial-law.py _site^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1500221Z shell: /usr/bin/bash -e {0}
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1500451Z env:
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1500634Z   GITHUB_PAGES: true
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1500819Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:13.1557564Z /tmp/generate-commercial-law.py.gz: OK
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3693776Z COMMERCIAL_LAW_GENERATED chapters=18 appendices=3 questions=90 search=111 figures=18
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3769202Z ##[group]Run python - <<'PY'
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3769548Z ^[[36;1mpython - <<'PY'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3769765Z ^[[36;1mfrom pathlib import Path^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3769991Z ^[[36;1mimport json, re^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3770190Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3770368Z ^[[36;1msite = Path('_site')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3770576Z ^[[36;1mrelease_data = {^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3770777Z ^[[36;1m    'calculus': {^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3770995Z ^[[36;1m        'updatedAt': '2026-07-27',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3771240Z ^[[36;1m        'releaseNotes': [{^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3771489Z ^[[36;1m            'version': '2026.07.27-3',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3771736Z ^[[36;1m            'date': '2026-07-27',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3771979Z ^[[36;1m            'title': '改回標準大一微積分本位',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3772208Z ^[[36;1m            'changes': [^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3772430Z ^[[36;1m                '移除經濟學取向副標題與經濟專屬核心題型',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3772718Z ^[[36;1m                '新增或強化中值定理、洛必達法則、弧長、旋轉曲面與純數學限制最佳化',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3772979Z ^[[36;1m                '73 題題庫重新驗算；181 項 QA 全數通過',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3773214Z ^[[36;1m            ],^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3773451Z ^[[36;1m            'progressImpact': '章節 ID 與章節數未變，既有閱讀進度保留。',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3773712Z ^[[36;1m        }],^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3773891Z ^[[36;1m    },^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3774074Z ^[[36;1m    'accounting': {^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3774472Z ^[[36;1m        'updatedAt': '2026-07-27',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3774716Z ^[[36;1m        'releaseNotes': [{^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3774963Z ^[[36;1m            'version': '2026.07.27-2',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3775206Z ^[[36;1m            'date': '2026-07-27',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3775445Z ^[[36;1m            'title': '二次內容複核與錯誤修正',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3775686Z ^[[36;1m            'changes': [^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3775906Z ^[[36;1m                '修正損益表名稱與存貨成本公式',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3776141Z ^[[36;1m                '區分定期加權平均與永續移動平均',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3776398Z ^[[36;1m                '補強約當現金、折舊、流動負債與現金流量分類條件',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3776645Z ^[[36;1m                '70 題題庫重新驗算並同步搜尋索引與圖解',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3776875Z ^[[36;1m            ],^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3777112Z ^[[36;1m            'progressImpact': '章節與題目 ID 未變，既有閱讀進度與錯題紀錄保留。',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3777372Z ^[[36;1m        }],^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3777550Z ^[[36;1m    },^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3777733Z ^[[36;1m    'economics': {^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3777945Z ^[[36;1m        'updatedAt': '2026-07-27',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3778189Z ^[[36;1m        'releaseNotes': [{^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3778412Z ^[[36;1m            'version': '2026.07.27-2',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3778652Z ^[[36;1m            'date': '2026-07-27',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3778931Z ^[[36;1m            'title': '發布後獨立糾錯複核',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3779189Z ^[[36;1m            'changes': [^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3779409Z ^[[36;1m                '修正補貼價格楔與福利效果的敘述',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3779653Z ^[[36;1m                '區分規模經濟、規模不經濟與規模報酬',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3779894Z ^[[36;1m                '補正正消費與正生產外部性的社會曲線關係',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3780135Z ^[[36;1m                '明定儲蓄與稅乘數公式中的 T 為淨稅收',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3780367Z ^[[36;1m                '區分簡單存款乘數與現實廣義貨幣乘數',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3780605Z ^[[36;1m                '補上總合需求與國際收支恆等式的模型條件',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3780841Z ^[[36;1m                '同步修正 6 道題庫詳解與搜尋索引',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3781063Z ^[[36;1m            ],^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3781299Z ^[[36;1m            'progressImpact': '章節與題目 ID 未變，既有閱讀進度與錯題紀錄保留。',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3781681Z ^[[36;1m        }],^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3781965Z ^[[36;1m    },^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3782156Z ^[[36;1m}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3782375Z ^[[36;1mfor book_id, extra in release_data.items():^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3782681Z ^[[36;1m    path = site / f'books/{book_id}/manifest.json'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3782999Z ^[[36;1m    obj = json.loads(path.read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3783389Z ^[[36;1m    obj.update(extra)^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3783740Z ^[[36;1m    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3784107Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3784550Z ^[[36;1mlibrary_path = site / 'data/library.json'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3784881Z ^[[36;1mlibrary = json.loads(library_path.read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3785253Z ^[[36;1mlibrary['version'] = '2026.07.28-1'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3785723Z ^[[36;1mlibrary_path.write_text(json.dumps(library, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3786171Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3786403Z ^[[36;1mapp_path = site / 'app.js'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3786688Z ^[[36;1mapp = app_path.read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3787043Z ^[[36;1mhelper = '''  function renderReleaseNotes(manifest) {^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3787452Z ^[[36;1m  const notes = Array.isArray(manifest.releaseNotes) ? manifest.releaseNotes : [];^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3787844Z ^[[36;1m  if (!notes.length) return '';^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3788115Z ^[[36;1m  return `<details class="release-notes">^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3788381Z ^[[36;1m    <summary>查看版本與更新內容</summary>^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3788672Z ^[[36;1m    <div class="release-notes-body">${notes.map(note => `^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3788979Z ^[[36;1m      <section class="release-entry">^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3789590Z ^[[36;1m        <div class="release-entry-head"><strong>${escapeHtml(note.version || manifest.version || '')}</strong><span>${escapeHtml(note.date || manifest.updatedAt || '')}</span></div>^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3790198Z ^[[36;1m        <h3>${escapeHtml(note.title || '內容更新')}</h3>^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3790573Z ^[[36;1m        <ul>${(note.changes || []).map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3791108Z ^[[36;1m        ${note.progressImpact ? `<p class="progress-impact">閱讀進度：${escapeHtml(note.progressImpact)}</p>` : ''}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3791544Z ^[[36;1m      </section>`).join('')}</div>^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3791778Z ^[[36;1m  </details>`;^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3791971Z ^[[36;1m}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3792132Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3792296Z ^[[36;1m'''^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3792534Z ^[[36;1mif 'function renderReleaseNotes(manifest)' not in app:^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3792999Z ^[[36;1m    app = app.replace('  async function renderLibrary() {', helper + '  async function renderLibrary() {')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3793405Z ^[[36;1m    app = app.replace(^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3793839Z ^[[36;1m        '            <h3>${escapeHtml(book.title)}</h3>\n            <p>${escapeHtml(book.subtitle)}</p>\n            <div class="progress-track">',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3795024Z ^[[36;1m        '            <h3>${escapeHtml(book.title)}</h3>\n            <p>${escapeHtml(book.subtitle)}</p>\n            <div class="version-line">內容版本 ${escapeHtml(manifest.version || \'未標示\')}</div>\n            <div class="progress-track">',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3795686Z ^[[36;1m        1,^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3795877Z ^[[36;1m    )^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3796067Z ^[[36;1m    app = app.replace(^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3796551Z ^[[36;1m        '          <h1>${escapeHtml(manifest.title)}</h1>\n          <p class="muted">${escapeHtml(manifest.subtitle)}</p>\n          <div class="progress-track">',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3797629Z ^[[36;1m        '          <h1>${escapeHtml(manifest.title)}</h1>\n          <p class="muted">${escapeHtml(manifest.subtitle)}</p>\n          <div class="version-line version-line-strong">內容版本 ${escapeHtml(manifest.version || \'未標示\')}・最後更新 ${escapeHtml(manifest.updatedAt || \'未標示\')}</div>\n          <div class="progress-track">',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3798479Z ^[[36;1m        1,^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3798662Z ^[[36;1m    )^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3798846Z ^[[36;1m    app = app.replace(^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3799160Z ^[[36;1m        '        </div>\n      </section>\n      <div class="section-title"><h2>搜尋內容</h2></div>',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3799763Z ^[[36;1m        '        </div>\n        ${renderReleaseNotes(manifest)}\n      </section>\n      <div class="section-title"><h2>搜尋內容</h2></div>',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3800220Z ^[[36;1m        1,^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3800400Z ^[[36;1m    )^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3800612Z ^[[36;1mapp_path.write_text(app, encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3800874Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3801058Z ^[[36;1mcss_path = site / 'styles.css'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3801322Z ^[[36;1mcss = css_path.read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3801587Z ^[[36;1mif '.release-notes{' not in css:^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3801829Z ^[[36;1m    css += '''^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3802161Z ^[[36;1m.version-line{font-size:.86rem;color:var(--muted);margin:.25rem 0 .7rem;font-weight:600}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3802841Z ^[[36;1m.version-line-strong{display:inline-block;padding:.35rem .65rem;border:1px solid var(--line);border-radius:999px;background:var(--surface);color:var(--text)}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3803665Z ^[[36;1m.release-notes{grid-column:1/-1;margin-top:.75rem;border:1px solid var(--line);border-radius:14px;background:var(--surface);overflow:hidden}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3804550Z ^[[36;1m.release-notes summary{cursor:pointer;padding:12px 14px;font-weight:700;color:var(--text)}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3805031Z ^[[36;1m.release-notes-body{border-top:1px solid var(--line);padding:0 14px}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3805364Z ^[[36;1m.release-entry{padding:14px 0}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3805678Z ^[[36;1m.release-entry+.release-entry{border-top:1px solid var(--line)}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3806183Z ^[[36;1m.release-entry-head{display:flex;gap:12px;justify-content:space-between;color:var(--muted);font-size:.9rem}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3806622Z ^[[36;1m.release-entry h3{margin:.45rem 0}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3806940Z ^[[36;1m.release-entry ul{margin:.4rem 0 .6rem;padding-left:1.25rem}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3807258Z ^[[36;1m.release-entry li{margin:.3rem 0}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3807717Z ^[[36;1m.progress-impact{margin:.6rem 0 0;padding:.65rem .75rem;border-radius:10px;background:var(--soft);color:var(--text)}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3808145Z ^[[36;1m'''^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3808354Z ^[[36;1mcss_path.write_text(css, encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3808602Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3808776Z ^[[36;1msw_path = site / 'sw.js'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3809024Z ^[[36;1msw = sw_path.read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3809460Z ^[[36;1msw = re.sub(r"const VERSION = 'study-library-[^']+';", "const VERSION = 'study-library-2026-07-28-1';", sw, count=1)^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3809953Z ^[[36;1msw_path.write_text(sw, encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3810194Z ^[[36;1mPY^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3832340Z shell: /usr/bin/bash -e {0}
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3832572Z env:
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3832748Z   GITHUB_PAGES: true
deploy	UNKNOWN STEP	2026-07-28T08:58:13.3832944Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4129326Z ##[group]Run python - <<'PY'
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4129648Z ^[[36;1mpython - <<'PY'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4129848Z ^[[36;1mimport json^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4130053Z ^[[36;1mfrom collections import Counter^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4130307Z ^[[36;1mfrom pathlib import Path^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4130528Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4130696Z ^[[36;1msite = Path('_site')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4131021Z ^[[36;1mlibrary = json.loads((site / 'data/library.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4131407Z ^[[36;1massert library['version'] == '2026.07.28-1'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4131841Z ^[[36;1massert [book['id'] for book in library['books']] == ['calculus', 'accounting', 'economics', 'commercial-law']^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4132254Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4132549Z ^[[36;1mexpected = {'calculus': 73, 'accounting': 70, 'economics': 100, 'commercial-law': 90}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4132934Z ^[[36;1mfor book_id, count in expected.items():^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4133249Z ^[[36;1m    root = site / 'books' / book_id^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4133596Z ^[[36;1m    manifest = json.loads((root / 'manifest.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4134041Z ^[[36;1m    questions = json.loads((root / 'questions.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4134596Z ^[[36;1m    search = json.loads((root / 'search.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4134939Z ^[[36;1m    assert manifest['id'] == book_id^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4135249Z ^[[36;1m    assert manifest['updatedAt'] and manifest['releaseNotes']^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4135621Z ^[[36;1m    assert questions['count'] == count == len(questions['items'])^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4135934Z ^[[36;1m    assert search['entries']^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4136193Z ^[[36;1m    for chapter in manifest['chapters']:^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4136462Z ^[[36;1m        path = root / chapter['file']^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4136761Z ^[[36;1m        assert path.is_file() and path.stat().st_size > 100^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4137037Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4137242Z ^[[36;1maccounting_root = site / 'books/accounting'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4137676Z ^[[36;1massert json.loads((accounting_root / 'manifest.json').read_text(encoding='utf-8'))['version'] == '2026.07.27-2'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4138262Z ^[[36;1massert len(json.loads((accounting_root / 'search.json').read_text(encoding='utf-8'))['entries']) == 111^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4138657Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4138863Z ^[[36;1meconomics_root = site / 'books/economics'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4139273Z ^[[36;1meconomics_manifest = json.loads((economics_root / 'manifest.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4139820Z ^[[36;1meconomics_questions = json.loads((economics_root / 'questions.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4140348Z ^[[36;1massert economics_manifest['version'] == economics_questions['version'] == '2026.07.27-2'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4140880Z ^[[36;1massert len(json.loads((economics_root / 'search.json').read_text(encoding='utf-8'))['entries']) == 144^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4141252Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4141449Z ^[[36;1mlaw_root = site / 'books/commercial-law'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4141816Z ^[[36;1mlaw_manifest = json.loads((law_root / 'manifest.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4142283Z ^[[36;1mlaw_questions = json.loads((law_root / 'questions.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4142740Z ^[[36;1mlaw_search = json.loads((law_root / 'search.json').read_text(encoding='utf-8'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4143176Z ^[[36;1massert law_manifest['version'] == law_questions['version'] == '2026.07.28-1'^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4143617Z ^[[36;1massert len([x for x in law_manifest['chapters'] if x['kind'] == 'chapter']) == 18^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4144299Z ^[[36;1massert len([x for x in law_manifest['chapters'] if x['kind'] == 'appendix']) == 3^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4144662Z ^[[36;1massert len(law_search['entries']) == 111^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4145150Z ^[[36;1massert Counter(q['chapterId'] for q in law_questions['items']) == {f'ch{i:02d}': 5 for i in range(18)}^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4145529Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4145874Z ^[[36;1mlaw_text = '\n'.join((law_root / x['file']).read_text(encoding='utf-8') for x in law_manifest['chapters'])^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4146273Z ^[[36;1mfor token in (^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4146531Z ^[[36;1m    '公司法第 23 條', '300 字', '持續 6 個月以上', '第 43-6 條第一項第二款、第三款',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4146848Z ^[[36;1m    '合計不得超過 35 人', '超過 5%', '超過 10%', '公開後 18 小時內', '證交法第 62 條',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4147126Z ^[[36;1m    '至少 2 人', '不得少於董事席次五分之一',^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4147352Z ^[[36;1m):^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4147535Z ^[[36;1m    assert token in law_text^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4147804Z ^[[36;1massert '私募對象一律不得超過 35 人' not in law_text^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4148066Z ^[[36;1massert '短線交易只適用上市股票' not in law_text^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4148302Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4148571Z ^[[36;1mfigures = sorted((site / 'assets/commercial-law-svg').glob('*.svg'))^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4148890Z ^[[36;1massert len(figures) == 18^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4149119Z ^[[36;1mfor figure in figures:^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4149371Z ^[[36;1m    svg = figure.read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4149694Z ^[[36;1m    assert '<title' in svg and '<desc' in svg and 'viewBox' in svg^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4149990Z ^[[36;1m^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4150208Z ^[[36;1mapp = (site / 'app.js').read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4150536Z ^[[36;1mcss = (site / 'styles.css').read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4150850Z ^[[36;1msw = (site / 'sw.js').read_text(encoding='utf-8')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4151116Z ^[[36;1massert '查看版本與更新內容' in app^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4151399Z ^[[36;1massert '內容版本 ${escapeHtml(manifest.version' in app^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4151676Z ^[[36;1massert '法條速查' in app^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4151910Z ^[[36;1massert '.release-notes{' in css^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4152184Z ^[[36;1massert 'study-library-2026-07-28-1' in sw^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4152497Z ^[[36;1massert './books/commercial-law/manifest.json' in sw^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4152828Z ^[[36;1massert './books/commercial-law/chapters/ch17.html' in sw^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4153261Z ^[[36;1mprint('COMMERCIAL_LAW_LIBRARY_OK books=4 chapters=18 questions=90 search=111 figures=18')^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4153629Z ^[[36;1mPY^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4153817Z ^[[36;1mnode --check _site/app.js^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4154046Z ^[[36;1mnode --check _site/sw.js^[[0m
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4173507Z shell: /usr/bin/bash -e {0}
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4173788Z env:
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4173971Z   GITHUB_PAGES: true
deploy	UNKNOWN STEP	2026-07-28T08:58:13.4174242Z ##[endgroup]
deploy	UNKNOWN STEP	2026-07-28T08:58:13.5279220Z Traceback (most recent call last):
deploy	UNKNOWN STEP	2026-07-28T08:58:13.5279631Z   File "<stdin>", line 50, in <module>
deploy	UNKNOWN STEP	2026-07-28T08:58:13.5279977Z AssertionError
deploy	UNKNOWN STEP	2026-07-28T08:58:13.5408269Z ##[error]Process completed with exit code 1.
deploy	UNKNOWN STEP	2026-07-28T08:58:13.5506967Z Node 20 is being deprecated. This workflow is running with Node 24 by default. If you need to temporarily use Node 20, you can set the ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION=true environment variable. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
deploy	UNKNOWN STEP	2026-07-28T08:58:13.5507913Z Post job cleanup.
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6168504Z [command]/usr/bin/git version
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6198050Z git version 2.54.0
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6224920Z Temporarily overriding HOME='/home/runner/work/_temp/379f51be-ea91-47f3-a895-b110d4f00f6e' before making global git config changes
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6225938Z Adding repository directory to the temporary git global config as a safe directory
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6230125Z [command]/usr/bin/git config --global --add safe.directory /home/runner/work/study-review-library/study-review-library
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6259205Z [command]/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6287150Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6467091Z [command]/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6484408Z http.https://github.com/.extraheader
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6492457Z [command]/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6516354Z [command]/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6683085Z [command]/usr/bin/git config --local --name-only --get-regexp ^includeIf\.gitdir:
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6709996Z [command]/usr/bin/git submodule foreach --recursive git config --local --show-origin --name-only --get-regexp remote.origin.url
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6988486Z Evaluate and set environment url
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6991845Z Evaluated environment url: 
deploy	UNKNOWN STEP	2026-07-28T08:58:13.6992397Z Cleaning up orphan processes
deploy	UNKNOWN STEP	2026-07-28T08:58:13.7189339Z ##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@v4, actions/configure-pages@v5. For more information see: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/
```
