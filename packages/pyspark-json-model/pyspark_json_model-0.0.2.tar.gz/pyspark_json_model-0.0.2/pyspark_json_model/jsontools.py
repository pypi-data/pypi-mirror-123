#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyspark.sql.types import *
from pyspark.sql.functions import *
import copy
from collections import OrderedDict
from functools import reduce
from pyspark.sql import DataFrame
import json


class JSONParserPyspark:
    def __init__(self, file_path, identifier, is_normalize_df):
        """
        Constructor for JSON parser
        :param file_path: <class, 'str'>
        :param identifier: <class, 'str'>
        :param is_normalize_df: <class, 'bool'>
        """

        self.file_path = file_path
        self.identifier = identifier
        self.is_normalize_df = is_normalize_df
        self.dataframe_dict = {}
        self.final_dict = {}
        self.level = 1
        self.drop_in_col = ["root_metric", "child_metric", "level"]

    def array_identification(self, dataframe):
        """
        Function to identify the array type columns from dataframe
        :param dataframe: <class, 'pyspark.DataFrame'>
        :return: <class, 'list'>
        """

        columns = []
        for field in dataframe.schema.fields:
            if isinstance(field.dataType, ArrayType):
                columns.append(field.name)
        return columns

    def check_all_done(self, df):
        """
        Function to check whether all Struct & Array field are processed
        :param df: <class, 'pyspark.DataFrame'>
        :return: <class, 'dict'>
        """

        nested_fields = dict(
            [
                (field.name, field.dataType)
                for field in df.schema.fields
                if isinstance(field.dataType, StructType)
                or isinstance(field.dataType, ArrayType)
            ]
        )
        return nested_fields

    def get_nested_field(self, df):
        """
        Function to identify the struct type columns from dataframe
        :param df: <class, 'pyspark.DataFrame'>
        :return: <class, 'dict'>
        """

        nested_fields = dict(
            [
                (field.name, field.dataType)
                for field in df.schema.fields
                if isinstance(field.dataType, StructType)
            ]
        )
        return nested_fields

    def explode_struct_field(self, nested_fields):
        """
        Function to generate aliased list of columns to be select from nested dataframe
        :param nested_fields: <class, 'dict'>
        :return: <class, 'list'>
        """

        expanded = []
        for col_name in nested_fields.keys():
            expanded.extend(
                [
                    col(col_name + "." + k).alias(col_name + "_" + k)
                    for k in [n.name for n in nested_fields[col_name]]
                ]
            )
        return expanded

    def explode_array_df(self):
        """
        Function to itteratively create new dataframe wherever datatype is array to generate proper data model
        :param :
        :return:
        """

        keys = self.dataframe_dict.keys()
        for key in list(keys):
            id_available = False
            columns = self.array_identification(self.dataframe_dict[key])
            select_columns = copy.deepcopy(columns)
            if (
                self.root_node + "_" + self.identifier
                in self.dataframe_dict[key].columns
            ):
                id_available = True
                select_columns.append(self.root_node + "_" + self.identifier)
            if key + "_child_id" in self.dataframe_dict[key].columns:
                select_columns.append(key + "_child_id")
                select_columns.append("child_metric")
            if len(columns) > 0:
                for col_ in columns:
                    if id_available:
                        self.dataframe_dict[col_] = (
                            self.dataframe_dict[key]
                            .select(select_columns)
                            .select(
                                col(key + "_child_id").alias(key + "_root_id"),
                                col("child_metric").alias("root_metric"),
                                self.root_node + "_" + self.identifier,
                                explode_outer(col(col_)).alias(col_),
                            )
                        )
                    else:
                        self.dataframe_dict[col_] = (
                            self.dataframe_dict[key]
                            .select(select_columns)
                            .select(explode_outer(col(col_)).alias(col_))
                        )
                    self.dataframe_dict[col_] = self.add_random_id(
                        self.dataframe_dict[col_], col_
                    ).withColumn("level", lit(self.level))
                self.dataframe_dict[key] = self.dataframe_dict[key].drop(*columns)
            self.level = self.level + 1

    def add_random_id(self, df, col_):
        """
        Function to add random id to dataframe which can be used to join parent child relation in data model format
        :param df: <class, 'pyspark.DataFrame'>
        :param col_: <class, 'string'>
        :return: <class, 'pyspark.DataFrame'>
        """

        df = df.withColumn(
            col_ + "_child_id", monotonically_increasing_id()
        ).withColumn("child_metric", lit(col_))
        return df

    def main(self):
        """
        Main function to iterate over all the fileds which has datatype as array/struct
        :param :
        :return:
        """

        self.explode_array_df()
        for key in self.dataframe_dict.keys():
            nested_field = self.get_nested_field(self.dataframe_dict[key])
            if len(nested_field) > 0:
                select_clause = self.explode_struct_field(nested_field)
                self.dataframe_dict[key] = (
                    self.dataframe_dict[key]
                    .select("*", *select_clause)
                    .drop(*nested_field)
                )

    def drop_columns(self, drop_col):
        """
        Function to drop the unnecessary columns
        :param drop_col: <class, 'list'>
        :return:
        """

        for key in self.dataframe_dict.keys():
            self.dataframe_dict[key] = self.dataframe_dict[key].drop(*drop_col)

    def drop_all_duplicates(self):
        """
        Function to drop duplicate values
        :param :
        :return:
        """

        for key in self.dataframe_dict.keys():
            self.dataframe_dict[key] = self.dataframe_dict[key].dropDuplicates()

    def remove_df(self, union_df):
        """
        Function to remove the dataframe which don't have any major columns
        :param union_df: <class, 'pyspark.DataFrame'>
        :return filan_dict: <class, 'dict'>
        """

        for key in union_df.collect():
            if (
                len(self.dataframe_dict[key["root_metric"]].columns) > 6
                and len(self.dataframe_dict[key["child_metric"]].columns) > 6
            ):
                self.final_dict[key["root_metric"]] = self.dataframe_dict[
                    key["root_metric"]
                ]
                self.final_dict[key["child_metric"]] = self.dataframe_dict[
                    key["child_metric"]
                ]
            elif (
                len(self.dataframe_dict[key["root_metric"]].columns) <= 6
                and len(self.dataframe_dict[key["child_metric"]].columns) > 6
            ):
                self.final_dict[key["root_metric"]] = self.dataframe_dict[
                    key["root_metric"]
                ]
                self.final_dict[key["child_metric"]] = self.dataframe_dict[
                    key["child_metric"]
                ]
            elif (
                len(self.dataframe_dict[key["root_metric"]].columns) > 6
                and len(self.dataframe_dict[key["child_metric"]].columns) <= 6
            ):
                self.final_dict[key["root_metric"]] = self.dataframe_dict[
                    key["root_metric"]
                ]
            else:
                continue
        return self.final_dict

    def check_relationship(self, dataframe_dict):
        """
        Function to find out the parent-child  relationship from multiple segregated dataframes
        :param dataframe_dict: <class, 'dict'>
        :return union_df: <class, 'pyspark.DataFrame'>
        """

        relation_df_list = []
        parent_name = ""
        for metric in list(dataframe_dict.keys()):
            if metric != "main":
                if "root_id" not in "_".join(
                    dataframe_dict[metric].columns
                ) and "child_id" in "_".join(dataframe_dict[metric].columns):
                    parent_name = parent_name + metric
                else:
                    df = (
                        dataframe_dict[metric]
                        .select("root_metric", "child_metric", "level")
                        .dropDuplicates()
                    )
                    relation_df_list.append(df)

        union_df = reduce(DataFrame.unionAll, relation_df_list).orderBy(
            col("level").desc()
        )
        return union_df

    def join_multiple_df(self, df_left, df_right):
        """
        Function to join parent-child  relationship dataframes
        :param df_left: <class, 'pyspark.DataFrame'>
        :param df_right: <class, 'pyspark.DataFrame'>
        :return df: <class, 'pyspark.DataFrame'>
        """

        df = (
            self.final_dict[df_left]
            .join(
                self.final_dict[df_right],
                self.final_dict[df_left][df_left + "_child_id"]
                == self.final_dict[df_right][df_left + "_root_id"],
                how="inner",
            )
            .drop(*self.drop_in_col)
            .drop(self.final_dict[df_right][self.root_node + "_" + self.identifier])
        )
        return df

    def normalized_json(self, union_df, normalized_json_model):
        """
        Function to normalize
        :param union_df: <class, 'pyspark.DataFrame'>
        :param normalized_json_model: <class, 'dict'>
        :return normalized_json_model: <class, 'dict'>
        """

        for record in union_df.collect():
            self.final_dict[record["root_metric"]] = self.join_multiple_df(
                record["root_metric"], record["child_metric"]
            )

        drop_column_list = []
        for col__ in self.final_dict[self.root_node].columns:
            if "child_id" in col__ or "root_id" in col__:
                drop_column_list.append(col__)

        normalized_json_model[self.root_node + "_normalized"] = (
            self.final_dict[self.root_node].drop(*drop_column_list).dropDuplicates()
        )
        return normalized_json_model

    def process(self, sc, spark, drop_col=[]):
        """
        Function to parse JSON in fromatted manner to build structured data model
        :param drop_col<Optional>: <class, 'list'>
        :return normalized_json_model: <class, 'dict'>
        """

        sourcePath = self.file_path

        processed_json = {}
        processed_list = []

        if isinstance(
            json.loads(sc.wholeTextFiles(self.file_path).collect()[0][1]), dict
        ):
            if (
                len(
                    json.loads(sc.wholeTextFiles(self.file_path).collect()[0][1]).keys()
                )
                > 1
            ):
                processed_list.append(
                    json.loads(sc.wholeTextFiles(self.file_path).collect()[0][1])
                )
                processed_json["items"] = processed_list
                a_file = open("/normalization_json_data_model.json", "w")
                json.dump(processed_json, a_file)
                a_file.close()
                sourcePath = "file:///normalization_json_data_model.json"
                self.root_node = "items"
            elif (
                len(
                    json.loads(sc.wholeTextFiles(self.file_path).collect()[0][1]).keys()
                )
                == 1
            ):
                self.root_node = list(
                    json.loads(sc.wholeTextFiles(self.file_path).collect()[0][1]).keys()
                )[0]

        elif isinstance(
            json.loads(sc.wholeTextFiles(self.file_path).collect()[0][1]), list
        ):
            processed_json["items"] = json.loads(
                sc.wholeTextFiles(self.file_path).collect()[0][1]
            )
            a_file = open("/normalization_json_data_model.json", "w")
            json.dump(processed_json, a_file)
            a_file.close()
            sourcePath = "file:///normalization_json_data_model.json"
            self.root_node = "items"

        dataframe = spark.read.json(sourcePath)
        self.dataframe_dict["main"] = dataframe
        identifier = self.identifier
        record_count_dict = {}
        self.main()
        flag_check = True
        is_normalize_df = self.is_normalize_df

        while flag_check:
            self.main()
            len_table = len(list(self.dataframe_dict.keys()))
            check_list = []
            for table in list(self.dataframe_dict.keys()):
                if len(self.check_all_done(self.dataframe_dict[table])) > 0:
                    continue
                else:
                    check_list.append(table)

            if len(check_list) == len_table:
                flag_check = False

        self.drop_columns(drop_col)
        self.drop_all_duplicates()

        union_df = self.check_relationship(self.dataframe_dict)

        normalized_json_model = self.remove_df(union_df)

        root_metric_df = normalized_json_model[self.root_node]

        for key in list(self.final_dict.keys()):
            if (
                self.root_node + "_" + self.identifier in self.final_dict[key].columns
                and key != "main"
            ):
                record_count_dict[key] = self.final_dict[key].count()

        record_count_dict = OrderedDict(
            sorted(record_count_dict.items(), key=lambda x: x[1])
        )

        union_df = self.check_relationship(self.final_dict)

        if is_normalize_df:
            normalized_json_model = self.normalized_json(
                union_df, normalized_json_model
            )

        normalized_json_model[self.root_node] = root_metric_df

        return normalized_json_model
