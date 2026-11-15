跨区域智慧教育应用成效与公平评估平台

运行验收：
python3 -m learning_evidence run --fixture fixtures/acceptance.json --database /tmp/learning_evidence.sqlite3 --output /tmp/learning_evidence-output

核验：
python3 -m learning_evidence verify --database /tmp/learning_evidence.sqlite3 --output /tmp/learning_evidence-output

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.programs.test_contract -v

构建检查：
python3 -m compileall -q learning_evidence tests
