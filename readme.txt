全球南方人工智能能力建设项目编排中心

运行验收：
python3 -m capacity_commons run --fixture fixtures/acceptance.json --database /tmp/capacity_commons.sqlite3 --output /tmp/capacity_commons-output

核验：
python3 -m capacity_commons verify --database /tmp/capacity_commons.sqlite3 --output /tmp/capacity_commons-output

全量测试：
python3 -m unittest discover -s tests -v

按模块测试：
python3 -m unittest tests.equity_monitor.test_equity_signal -v

构建检查：
python3 -m compileall -q capacity_commons tests
