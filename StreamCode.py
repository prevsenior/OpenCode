def upsert(df, deltatable):
    df.createOrReplaceGlobalTempView(f"view_{tablename}")

    query = f'''
        SELECT *
        FROM global_temp.view_{tablename}
    QUALIFY ROW_NUMBER() OVER (PARTITION BY {id_field} ORDER BY {timestamp_field} DESC)=1
    '''

    df_cdc = spark.sql(query)

    (deltatable.alias("b")
                .merge(df_cdc.alias("d"), f"b.{id_field} = d.{id_field}")
                .whenMatchedDelete(condition = "d.OP = 'D'")
                .whenMatchedUpdateAll(condition = "d.OP = 'U'")
                .whenNotMatchedInsertAll(condition = "d.OP = 'I' OR d.OP = 'U'")
                .execute())

df_stream = (spark.readStream
             .format("cloudFiles")
             .option("cloudFiles.format", "parquet")
             .schema(schema)
             .load(f"/volumes/raw/upsell/cdc/{tablename}/"))

stream = (df_stream.writeStream
                    .option("checkpointLocation", f"/Volumes/raw/upsell/cdc/{tablename}_checkpoint/")
                    .trigger(availableNow=True))




#Codigo ajustado pelo ChatGPT


def upsert(df, deltatable, tablename, id_field, timestamp_field):
    df.createOrReplaceGlobalTempView(f"view_{tablename}")

    query = f'''
        SELECT *
        FROM global_temp.view_{tablename}
        QUALIFY ROW_NUMBER() OVER (PARTITION BY {id_field} ORDER BY {timestamp_field} DESC) = 1
    '''

    df_cdc = spark.sql(query)

    (deltatable.alias("b")
                .merge(df_cdc.alias("d"), f"b.{id_field} = d.{id_field}")
                .whenMatchedDelete("d.OP = 'D'")
                .whenMatchedUpdateAll("d.OP = 'U'")
                .whenNotMatchedInsertAll())
                .execute()

df_stream = (spark.readStream
             .format("cloudFiles")
             .option("cloudFiles.format", "parquet")
             .schema(schema)
             .load(f"/volumes/raw/upsell/cdc/{tablename}/"))

stream = (df_stream.writeStream
                    .option("checkpointLocation", f"/Volumes/raw/upsell/cdc/{tablename}_checkpoint/")
                    .trigger(availableNow=True)
                    .start())
