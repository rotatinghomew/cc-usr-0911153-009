跨区域智慧教育应用成效与公平评估平台

scale_reviews.open 使用一张已发布评分卡及固定评分门槛建立学校扩容评议，评分不足的学校不进入待审队列。
每轮评议固定比较人口、证据指纹和总名额；decide 确认或暂缓单校申请，安全门禁仍为 hold/reject 时不能批准。
多校共享本轮名额，完成结论不可覆盖。scale_reviews.inspect 可重开数据库核对候选、名额和历史依据。

同批评分卡基线：run 将同一次比较中的学校决策、记录版本、证据指纹
和评分固化到 cohort_card；在同一数据库内可通过 repository.cohort_card(run_id)
重读已发布评分卡。清单重放幂等，新证据不得静默覆盖旧卡。
此处尚未改变逐校成效计算或群体公平性上下文，顺序导致同批评分不一致的缺陷仍存在。

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
