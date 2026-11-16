跨区域智慧教育应用成效与公平评估平台

scale_reviews.open 使用一张已发布评分卡及固定评分门槛建立学校扩容评议，评分不足的学校不进入待审队列。
每轮评议固定比较人口、证据指纹和总名额；decide 确认或暂缓单校申请，安全门禁仍为 hold/reject 时不能批准。
多校共享本轮名额，完成结论不可覆盖。scale_reviews.inspect 可重开数据库核对候选、名额和历史依据。

同批评分卡：run 将同一次比较中的学校决策、记录版本、证据指纹
和评分固化到 cohort_card；在同一数据库内可通过 repository.cohort_card(run_id)
重读已发布评分卡。清单重放幂等，新证据不得静默覆盖旧卡。

批次人口口径：同一比较批次先按学校标识规范化并整批固定人口证据，所有学校共用
同一份群体权重，评分与推进判断不受导入顺序影响。晚到学校或历史更正会生成新的
比较人口和新评分卡，旧卡保持可复核；评分卡拒绝混用不同人口口径的决策。
中途退出后重跑同一清单会重算整批学校并得到同一份证据，不重复推进工作流状态。
单校追踪（Application.process）仍按单校自身证据给出结论，并记录其所用的比较人口。

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
