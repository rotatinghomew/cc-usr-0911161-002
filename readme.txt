全球南方人工智能能力建设项目编排中心

运行验收：
python3 -m capacity_commons run --fixture fixtures/acceptance.json --database /tmp/capacity_commons.sqlite3 --output /tmp/capacity_commons-output

核验：
python3 -m capacity_commons verify --database /tmp/capacity_commons.sqlite3 --output /tmp/capacity_commons-output

分层分析（在一致观察范围内按 总体→国家→轨道→国家×轨道 比较覆盖、完成与资源投入，
标明分母与缺失程度；更正按 record_id 归并、不计入新增参与；证据不足的分组不参与排名。
结果包中的 analysis.json 与项目判断消费同一份结论，重算结果与结果包逐字节一致）：
python3 -m capacity_commons analyze --database /tmp/capacity_commons.sqlite3

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.equity_monitor.test_equity_signal -v

构建检查：
python3 -m compileall -q capacity_commons tests
