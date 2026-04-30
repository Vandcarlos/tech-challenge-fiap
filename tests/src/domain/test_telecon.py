import domain.telecon as sut


def test_pandera_classes_has_same_fields():
    fields_pandas = set(sut.TelecomPandas.to_schema().columns.keys())
    fields_spark = set(sut.TelecomSpark.to_schema().columns.keys())

    diff = fields_pandas.symmetric_difference(fields_spark)

    assert fields_pandas == fields_spark, (
        f"Os schemas estão diferentes! Colunas divergentes: {diff}"
    )
    assert len(fields_pandas) == len(fields_spark), "A quantidade de atributos é diferente."
