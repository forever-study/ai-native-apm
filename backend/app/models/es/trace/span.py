from datetime import datetime

from elasticsearch import dsl


class AsyncSpan(dsl.AsyncDocument):
    # Data Stream 强制要求定义时间戳字段，标准名称为 @timestamp
    timestamp: dsl.M[datetime] = dsl.mapped_field(
        dsl.Date(default_timezone="UTC"), es_name="@timestamp"
    )
    start_time: dsl.M[datetime] = dsl.mapped_field(
        dsl.Date()
    )  # 原数据纳秒级，损失精度到微秒
    end_time: dsl.M[datetime] = dsl.mapped_field(
        dsl.Date()
    )  # 原数据纳秒级，损失精度到微秒

    trace_id: dsl.M[str] = dsl.mapped_field(dsl.Keyword())
    span_id: dsl.M[str] = dsl.mapped_field(dsl.Keyword())
    parent_span_id: dsl.M[str] = dsl.mapped_field(dsl.Keyword())
    name: dsl.M[str] = dsl.mapped_field(dsl.Keyword())
    kind: dsl.M[str] = dsl.mapped_field(dsl.Keyword())
    trace_state: dsl.M[str] = dsl.mapped_field(dsl.Keyword())

    # 复合字段
    attributes: dsl.M[dict[str, object]] = dsl.mapped_field(dsl.Object(dynamic=True))
    resource: dsl.M[dict[str, object]] = dsl.mapped_field(dsl.Object(dynamic=True))
    status: dsl.M[dict[str, object]] = dsl.mapped_field(dsl.Object(dynamic=True))

    # 嵌套字段
    events: dsl.M[list[dict[str, object]]] = dsl.mapped_field(dsl.Nested(dynamic=True))
    links: dsl.M[list[dict[str, object]]] = dsl.mapped_field(dsl.Nested(dynamic=True))

    class Index:
        # 匹配模式：该模型对应的所有 Data Stream 目标名称前缀
        name: str = "ai-native-apm-span"
        data_stream: bool = True
