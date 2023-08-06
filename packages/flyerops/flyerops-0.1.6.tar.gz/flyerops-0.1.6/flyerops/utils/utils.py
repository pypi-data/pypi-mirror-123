import awswrangler as wr
from typing import Dict, Any, List
import time
import psycopg2
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pandas as pd
import io
import teradatasql


class AthenaHelper:
    def __init__(
        self, bucket: str, boto_sess: str, database: str, output_prefix: str,
    ):

        """Instantiates an athena class that extends aws wrangler

        Args:
            bucket: S3 bucket where data will be stored
            boto_sess: Boto session
            database: Athena database
            output_prefix: Where to save temporary athena query data

        """
        self.bucket = bucket
        self.database = database
        self.output_prefix = output_prefix
        self.boto_sess = boto_sess
        self.athena_client = boto_sess.client("athena")
        self.s3_client = boto_sess.resource("s3")
        self.glue_client = boto_sess.client("glue")

    def read_table(self, table: str) -> pd.DataFrame:

        """Reads athena table name and returns dataframe 

        Args:
            table: Athena table name

        Returns:
            Pandas dataframe
        """

        df = wr.athena.read_sql_table(
            table=table,
            database=self.database,
            ctas_approach=True,
            s3_output=self.s3_output,
            boto3_session=self.boto_sess,
            use_threads=True,
        )
        return df

    def _wait_for_query_completion(self, query_id):
        _QUERY_FINAL_STATES: List[str] = ["FAILED", "SUCCEEDED", "CANCELLED"]
        response = self.athena_client.get_query_execution(QueryExecutionId=query_id)
        state = response["QueryExecution"]["Status"]["State"]
        while state not in _QUERY_FINAL_STATES:
            time.sleep(1)
            response = self.athena_client.get_query_execution(QueryExecutionId=query_id)
            state = response["QueryExecution"]["Status"]["State"]
        if state == "FAILED":
            print(response["QueryExecution"]["Status"]["StateChangeReason"])
        if state == "CANCELLED":
            print(response["QueryExecution"]["Status"]["StateChangeReason"])
        if state == "SUCCEEDED":
            return state

    def create_table(
        self,
        query: str,
        table_name: str,
        bucket_path: str,
        column_comments: str = None,
    ):

        """Creates table from query

        Args:
            query: query. Must be a create statement query
            table_name: Name of table to be created
            bucket_path: S3 prefix where data will be stored
            column_comments: Optional argument to specify column descriptions that will be stored in aws glue

        """

        # drop table
        wr.catalog.delete_table_if_exists(
            database=self.database, table=table_name, boto3_session=self.boto_sess,
        )

        # delete objects
        _bucket = self.s3_client.Bucket(name=self.bucket)
        _bucket.objects.filter(Prefix=bucket_path).delete()

        # Execute query
        response = self.athena_client.start_query_execution(
            QueryString=query,
            QueryExecutionContext={"Database": self.database},
            ResultConfiguration={
                "OutputLocation": f"s3://{self.bucket}/{self.output_prefix}"
            },
        )

        query_execution_id = response["QueryExecutionId"]
        state = self._wait_for_query_completion(query_execution_id)
        print(f"Query ID {query_execution_id} status: {state}")

        # Update column comments
        if column_comments:
            try:
                response = self.glue_client.get_table(
                    DatabaseName=self.database, Name=table_name,
                )

                table_input: Dict[str, Any] = {}
                for k, v in response["Table"].items():
                    if k in [
                        "Name",
                        "Description",
                        "Owner",
                        "LastAccessTime",
                        "LastAnalyzedTime",
                        "Retention",
                        "StorageDescriptor",
                        "PartitionKeys",
                        "ViewOriginalText",
                        "ViewExpandedText",
                        "TableType",
                        "Parameters",
                        "TargetTable",
                    ]:
                        table_input[k] = v

                for col in table_input["StorageDescriptor"]["Columns"]:
                    if col["Name"] in column_comments.keys():
                        col["Comment"] = column_comments[col["Name"]]

                self.glue_client.update_table(
                    DatabaseName=self.database, TableInput=table_input,
                )
            except Exception as e:
                raise e

        _bucket.objects.filter(Prefix=self.output_prefix).delete()

    def read_sql(self, query: str):
        """Reads athena SQL query and returns results

        Args:
            query: query

        Returns:
            Pandas dataframe
        """
        df = wr.athena.read_sql_query(
            query,
            database=self.database,
            s3_output=f"s3://{self.bucket}/{self.output_prefix}",
            keep_files=False,
            max_cache_seconds=0,
            boto3_session=self.boto_sess,
        )

        return df

    def to_parquet(
        self,
        data: pd.DataFrame,
        bucket_path: str,
        table_name: str,
        partition_cols: List[str] = None,
        columns_comments: Dict[str, str] = None,
    ):

        """Saves pandas dataframe as athena table

        Args:
            data: Pandas dataframe
            bucket_path: Qhere data will be stored in S3
            table_name: Name of table
            parition_cols: List of columns to create partitions on
            columns_comments: Argument to specify column descriptions that will be stored in aws glue

        """

        # Write to Athena
        wr.s3.to_parquet(
            df=data,
            path=f"s3://{self.bucket}/{bucket_path}/",  # where data will be stored in S3
            dataset=True,  # enables partitioning and table creation
            database=self.database,  # database to use; database must already exist
            table=table_name,
            partition_cols=partition_cols,  # table to be created
            mode="overwrite",  # overwrite (default is append)
            compression="snappy",
            concurrent_partitioning=True,  # compression saves cost for S3 and Athena
            use_threads=True,  # enable concurrent requests
            sanitize_columns=True,
            boto3_session=self.boto_sess,  # specify boto3 session with region
            columns_comments=columns_comments,
        )

        print(f"Created {self.database}.{table_name} in Athena")


class AuroraHelper:
    def __init__(self, host, user, password, port, database):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database

    def sqlalchemy_engine(self):
        """
        Creates sqlalchemy engine for Postgres Aurora.

        Returns:
            sqlalchemy.engine.Engine
        """
        try:
            return create_engine(
                f"postgresql+psycopg2://"
                f"{quote_plus(self.user)}:{quote_plus(self.password)}@{self.host}:{self.port}/{self.database}"
            )
        except Exception as e:
            print(e)

    def psycopg2_connection(self):
        """
        Creates psycopg2 connection for Postgres Aurora.

        Returns:
            psycopg2.extensions.connection
        """
        try:
            return psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                port=self.port,
                database=self.database,
            )
        except Exception as e:
            raise e

    def query(self, query: str, return_df=False):
        """
        Executes query

        Args:
            query: Query string
        """

        con = self.psycopg2_connection()
        con.autocommit = True
        try:
            with con.cursor() as cur:
                print(f"Executing query")
                cur.execute(query)
                if return_df:
                    data = cur.fetchall()
                    col_names = [desc[0] for desc in cur.description]
                    return pd.DataFrame(data, columns=col_names)
                else:
                    print("Query status: complete")
        except Exception as e:
            raise e

    def df_to_aurora(
        self,
        df,
        table_name,
        schema_name,
        mode="fail",
        sep_val="\t",
        null_val="",
        verbose=False,
    ):
        """
        Efficiently load data into Postgres Aurora from pandas DataFrame.

        Args:
            df : pandas.DataFrame
                Query can be any valid PostgreSQL statement.
            table_name : str
                Target table name in Aurora.
            schema_name: str
                Target schema name in Aurora.
            mode: {'fail', 'replace', 'append'}, optional [default is "fail"]
                Write mode to use, if table already exists.
            sep_val: str, optional [default is "\t"]
                Sets separator value.
            null_val: str, optional [default is ""]
                Sets default value for nulls.
            verbose: bool, optional
                Prints completion message, if set to True.

        Returns:
            pandas.DataFrame
        """
        engine = self.sqlalchemy_engine()
        # raw_connection overcomes limitations imposed by DB API connection
        raw_con = engine.raw_connection()
        cur = raw_con.cursor()
        csv_like_stringio_object = io.StringIO()
        try:
            df.to_csv(
                path_or_buf=csv_like_stringio_object,
                sep=sep_val,
                header=False,
                index=False,
            )  # convert data to StringIO object
            csv_like_stringio_object.seek(0)  # set StringIO cursor
            df.head(0).to_sql(
                name=table_name,
                schema=schema_name,
                con=engine,
                if_exists=mode,
                index=False,
            )  # create table in Aurora
            cur.execute("SET search_path TO " + schema_name)  # set Aurora schema
            cur.copy_from(
                file=csv_like_stringio_object,
                table=table_name,
                sep=sep_val,
                null=null_val,
            )
            raw_con.commit()
            if verbose:
                print(f"Data successfully loaded into {schema_name}.{table_name}.")
        except Exception as e:
            print(e)
        finally:
            csv_like_stringio_object.close()
            cur.close()
            raw_con.close()
            engine.dispose()


class TeradataHelper:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def teradata_conn(self, source="prod"):
        # SQL Connection
        try:
            if source.lower() == "prod":
                conn = teradatasql.connect(
                    user=self.user,
                    password=self.password,
                    host="dwprod.delta.com",
                    logmech="ldap",
                )
                print("Database connection to prod")
                return conn

            elif source.lower() == "lake":
                conn = teradatasql.connect(
                    user=self.user,
                    password=self.password,
                    dbs_port=1433,
                    host="10.68.112.220",
                    logmech="TD2",
                )
                print("Database connection to lake")
                return conn

        except Exception as e:
            raise e

    def query(self, query, source="prod"):
        conn = self.teradata_conn(source)
        df = pd.read_sql(query, conn)
        print(f"Shape: {df.shape}")
        return df
