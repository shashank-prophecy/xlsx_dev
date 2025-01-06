from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import *

from prophecy.cb.server.base.ComponentBuilderBase import ComponentCode, Diagnostic, SeverityLevelEnum
from prophecy.cb.server.base.DatasetBuilderBase import DatasetSpec, DatasetProperties, Component
from prophecy.cb.ui.uispec import *
from prophecy.cb.server.base import WorkflowContext
import dataclasses
from prophecy.cb.migration import PropertyMigrationObj


class xlsx(DatasetSpec):
    name: str = "xlsx"
    datasetType: str = "File"
    docUrl: str = "https://docs.prophecy.io/low-code-spark/gems/source-target/file/xlsx"

    def optimizeCode(self) -> bool:
        return True

    @dataclass(frozen=True)
    class XLSXProperties(DatasetProperties):
        schema: Optional[StructType] = None
        description: Optional[str] = ""
        useSchema: bool = False
        path: str = ""
        columnNameOfCorruptRecord: Optional[str] = None
        columnNameOfRowNumber: Optional[str] = None
        dataAddress: str = "A1"
        dateFormat: Optional[str] = None
        excerptSize: Optional[str] = None
        fileExtension: Optional[str] = None
        header: bool = True
        ignoreAfterHeader: Optional[int] = None
        ignoreLeadingWhiteSpace: Optional[bool] = None
        ignoreTrailingWhiteSpace: Optional[bool] = None
        inferSchema: Optional[bool] = None
        keepUndefinedRows: Optional[bool] = None
        locale: Optional[str] = None
        nanValue: Optional[str] = None
        nullValue: Optional[str] = None
        parseMode: Optional[str] = None
        positiveInf: Optional[str] = None
        samplingRatio: Optional[str] = None
        timestampFormat: Optional[str] = None
        useNullForErrorCells: Optional[bool] = None
        usePlainNumberFormat: Optional[bool] = False
        workbookPassword: Optional[str] = None
        zoneId: Optional[str] = None
        tempFileThreshold: Optional[str] = None
        maxRowsInMemory: Optional[str] = None
        maxByteArraySize: Optional[str] = None
        writeMode: Optional[str] = None
        partitionColumns: Optional[List[str]] = None
        createSingleOutputFile: Optional[bool] = None
        libraryType: Optional[str] = "crealytics"
        skipRows: Optional[str] = None
        sheetName: Optional[str] = None
        trueValues: List[str] = field(default_factory=list)
        falseValues: List[str] = field(default_factory=list)
        nRows: Optional[str] = None
        naValues: List[str] = field(default_factory=list)
        keepDefaultNAValues: Optional[bool] = None
        naFilter: Optional[bool] = None
        charForThousands: Optional[str] = None
        charForDecimal: Optional[str] = None
        charForComment: Optional[str] = None
        skipFooter: Optional[str] = None
        naRep: Optional[str] = None
        floatFormat: Optional[str] = None
        index: Optional[bool] = False
        indexLable: Optional[str] = None
        startRow: Optional[str] = None
        startColumn: Optional[str] = None
        pandasExcelDataAddress: Optional[str] = None
        pandasWriteMode: Optional[str] = None

    def sourceDialog(self) -> DatasetDialog:
        locationPath = StackLayout(height=("100%")) \
                        .addElement(
                            SelectBox("Library Type")
                                .addOption("Excel Crealytics", "crealytics")
                                .addOption("Pandas", "pandas")
                                .bindProperty("libraryType")
                        ) \
                        .addElement(
                            Condition()
                                .ifEqual(
                                PropExpr("component.properties.libraryType"),
                                StringExpr("crealytics"),
                            ).then(
                                AlertBox(
                                    variant="info",
                                    _children=[
                                        Markdown(
                                            "This Gem has the following requirement(s): Configure the [spark-excel](https://mvnrepository.com/artifact/com.crealytics/spark-excel) Maven dependency on the Spark cluster."
                                        )
                                    ]
                                )      
                            ).otherwise(
                                AlertBox(
                                    variant="info",
                                    _children=[
                                        Markdown(
                                            "This Gem has the following requirement(s): (1) Configure the [pandas](https://pypi.org/project/pandas/) and [openpyxl](https://pypi.org/project/openpyxl/) PyPi dependency on the Spark cluster, (2) Currently read in XLSX gem using Pandas is **supported on Databricks** only."
                                        )
                                    ]
                                )                                  
                            )

                        )\
                        .addElement(TargetLocation("path"))

        excelSection = (ColumnsLayout(gap=("1rem"), height=("100%"))
                        .addColumn(
                        ScrollBox().addElement(
                            StackLayout(height=("100%"))
                                .addElement(Checkbox("Enforce schema").bindProperty("useSchema"))
                                .addElement(Checkbox("Header").bindProperty("header"))
                                .addElement(StackItem(grow=(1)).addElement(
                                FieldPicker(height=("100%"))
                                    .addField(TextBox("Data Address").bindPlaceholder("A1"), "dataAddress")
                                    .addField(TextBox("Column Name of Corrupt Record"), "columnNameOfCorruptRecord")
                                    .addField(TextBox("Column Name of Row Number"), "columnNameOfRowNumber")
                                    .addField(TextBox("Date Format"), "dateFormat")
                                    .addField(TextBox("Excerpt Size"), "excerptSize")
                                    .addField(TextBox("File Extension"), "fileExtension")
                                    .addField(TextBox("Ignore after header"), "ignoreAfterHeader")
                                    .addField(Checkbox("Ignore leading whitespace"), "ignoreLeadingWhiteSpace")
                                    .addField(Checkbox("Ignore trailing whitespace"), "ignoreTrailingWhiteSpace")
                                    .addField(Checkbox("Infer Schema"), "inferSchema")
                                    .addField(TextBox("Locale"), "locale")
                                    .addField(TextBox("NaN Value"), "nanValue")
                                    .addField(TextBox("Negative Infinite value"), "negativeInf")
                                    .addField(TextBox("Null value"), "nullValue")
                                    .addField(SelectBox("Parse Mode")
                                            .addOption("Permissive", "PERMISSIVE")
                                            .addOption("Drop Malformed", "DROPMALFORMED")
                                            .addOption("Fail Fast", "FAILFAST"),
                                            "parseMode"
                                            )
                                    .addField(TextBox("Positive Infinite value"), "positiveInf")
                                    .addField(TextBox("Sampling Ratio"), "samplingRatio")
                                    .addField(TextBox("Timestamp Format"), "timestampFormat")
                                    .addField(Checkbox("Use Null for Error Cells"), "useNullForErrorCells")
                                    .addField(TextBox("Workbook Password"), "workbookPassword")
                                    .addField(TextBox("Time Zone ID"), "zoneId")
                                    .addField(TextBox("Temporary file threshold"), "tempFileThreshold")
                                    .addField(TextBox("Maximum rows in memory"), "maxRowsInMemory")
                                    .addField(TextBox("Maximum byte array size"), "maxByteArraySize")
                            )
                            )
                        ),
                        "400px"
                    ) \
                    .addColumn(SchemaTable("").bindProperty("schema"), "5fr"))

        pandasSection = (ColumnsLayout(gap=("1rem"), height=("100%"))
                        .addColumn(
                        ScrollBox().addElement(
                            StackLayout(height=("100%"))
                                .addElement(Checkbox("Enforce schema").bindProperty("useSchema"))
                                .addElement(Checkbox("Header").bindProperty("header"))
                                .addElement(StackItem(grow=(1))
                                .addElement(
                                    FieldPicker(height=("100%"))
                                        .addField(TextBox("Data Address").bindPlaceholder("A:C"), "pandasExcelDataAddress")
                                        .addField(TextBox("Skip Rows").bindPlaceholder("0"), "skipRows")
                                        .addField(TextBox("Load Specific Sheet").bindPlaceholder("Sheet2"), "sheetName")
                                        .addField(SelectBox("True Values", mode="tags"),"trueValues")
                                        .addField(SelectBox("False Values", mode="tags"),"falseValues")
                                        .addField(TextBox("Read N Rows From Start").bindPlaceholder("10"), "nRows")
                                        .addField(SelectBox("NA Values", mode="tags"),"naValues")
                                        .addField(Checkbox("Keep Default NA Values"), "keepDefaultNAValues")
                                        .addField(Checkbox("Set Missing Values as NaN"), "naFilter")
                                        .addField(TextBox("Specific Character For Thousands").bindPlaceholder("."), "charForThousands")
                                        .addField(TextBox("Specific Character For Decimal").bindPlaceholder(","), "charForDecimal")
                                        .addField(TextBox("Specific Character For Comment").bindPlaceholder("#"), "charForComment")
                                        .addField(TextBox("Skip N Rows From Bottom").bindPlaceholder("10"), "skipFooter")
                                )
                            )
                        ),
                        "400px"
                    ) \
                    .addColumn(SchemaTable("").bindProperty("schema"), "5fr"))
               
        return DatasetDialog("xlsx") \
                .addSection("LOCATION", locationPath) \
                .addSection(
                    "PROPERTIES", Condition()
                                    .ifEqual(PropExpr("component.properties.libraryType"), StringExpr("crealytics"))
                                    .then(excelSection)
                                    .otherwise(pandasSection)
                ).addSection(
                    "PREVIEW",
                    PreviewTable("").bindProperty("schema")
                )

    def targetDialog(self) -> DatasetDialog:
        locationPath = StackLayout(height=("100%")) \
                        .addElement(
                            SelectBox("Library Type")
                                .addOption("Excel Crealytics", "crealytics")
                                .addOption("Pandas", "pandas")
                                .bindProperty("libraryType")
                        ) \
                        .addElement(
                            Condition()
                                .ifEqual(
                                PropExpr("component.properties.libraryType"),
                                StringExpr("crealytics"),
                            ).then(
                                AlertBox(
                                    variant="info",
                                    _children=[
                                        Markdown(
                                            "This Gem has the following requirement(s): Configure the [spark-excel](https://mvnrepository.com/artifact/com.crealytics/spark-excel) Maven dependency on the Spark cluster."
                                        )
                                    ]
                                )      
                            ).otherwise(
                                AlertBox(
                                    variant="info",
                                    _children=[
                                        Markdown(
                                            "This Gem has the following requirement(s): (1) Configure the [pandas](https://pypi.org/project/pandas/) and [openpyxl](https://pypi.org/project/openpyxl/) PyPi dependency on the Spark cluster, (2) Currently read in XLSX gem using Pandas is **supported on Databricks** only."
                                        )
                                    ]
                                )                                  
                            )

                        )\
                        .addElement(TargetLocation("path"))
        
        excelSection = (
            ColumnsLayout(gap=("1rem"), height=("100%"))
                .addColumn(
                ScrollBox().addElement(
                    StackLayout(height=("100%"))
                        .addElement(StackItem(grow=(1)).addElement(
                        FieldPicker(height=("100%"))
                            .addField(TextBox("Data Address").bindPlaceholder("A1"), "dataAddress")
                            .addField(TextBox("File Extension").bindPlaceholder("xlsx"), "fileExtension")
                            .addField(Checkbox("Header"), "header")
                            .addField(TextBox("Locale"), "locale")
                            .addField(TextBox("Date Format"), "dateFormat")
                            .addField(Checkbox("Use Plain Number Format"), "usePlainNumberFormat")
                            .addField(TextBox("Workbook Password"), "workbookPassword")
                            .addField(
                            SelectBox("Write Mode")
                                .addOption("error", "error")
                                .addOption("overwrite", "overwrite")
                                .addOption("append", "append")
                                .addOption("ignore", "ignore"),
                            "writeMode"
                        )
                            .addField(
                            SchemaColumnsDropdown("Partition Columns")
                                .withMultipleSelection()
                                .bindSchema("schema")
                                .showErrorsFor("partitionColumns"),
                            "partitionColumns"
                        )
                            .addField(Checkbox("Create single named XLSX file"), "createSingleOutputFile")
                    )
                    )
                ),
                "400px"
            )
            .addColumn(SchemaTable("").isReadOnly().withoutInferSchema().bindProperty("schema"), "5fr")
        )

        pandasSection = (
            ColumnsLayout(gap=("1rem"), height=("100%"))
                .addColumn(
                    ScrollBox().addElement(
                            StackLayout(height=("100%"))
                                .addElement(StackItem(grow=(1))
                                .addElement(
                                    FieldPicker(height=("100%"))
                                        .addField(
                                            SelectBox("Write Mode")
                                            .addOption("overwrite", "overwrite")
                                            .addOption("append", "append"),
                                            "pandasWriteMode"
                                        )
                                        .addField(TextBox("Sheet Name").bindPlaceholder("Sheet2"), "sheetName")
                                        .addField(TextBox("NA Representation").bindPlaceholder("N/A"), "naRep")
                                        .addField(TextBox("Float Format").bindPlaceholder("%.2f"), "floatFormat")
                                        .addField(Checkbox("Header"), "header")
                                        .addField(Checkbox("Index"), "index")
                                        .addField(TextBox("Index Label").bindPlaceholder("ColumnName"), "indexLable")
                                        .addField(TextBox("Start Row").bindPlaceholder("0"), "startRow")
                                        .addField(TextBox("Start Column").bindPlaceholder("0"), "startColumn")
                                )
                        )
                    ),
                "400px"
            )
            .addColumn(SchemaTable("").isReadOnly().withoutInferSchema().bindProperty("schema"), "5fr")
        )
                
        return DatasetDialog("xlsx") \
            .addSection("LOCATION", locationPath) \
            .addSection(
            "PROPERTIES",
                            Condition()
                                .ifEqual(PropExpr("component.properties.libraryType"), StringExpr("crealytics"))
                                .then(excelSection)
                                .otherwise(pandasSection)
            )

    def validate(self, context: WorkflowContext, component: Component) -> list:
        diagnostics = super(xlsx, self).validate(context, component)
        if len(component.properties.path) == 0:
            diagnostics.append(
                Diagnostic("properties.path", "path variable cannot be empty [Location]", SeverityLevelEnum.Error))

        if component.properties.createSingleOutputFile is not None and component.properties.createSingleOutputFile:
            if component.properties.writeMode == "append":
                diagnostics.append(
                    Diagnostic("properties.writeMode",
                               "Append write mode cannot be used with create single excel file option",
                               SeverityLevelEnum.Error))

        return diagnostics

    def onChange(self, context: WorkflowContext, oldState: Component, newState: Component) -> Component:
        return newState

    class XLSXFormatCode(ComponentCode):
        def __init__(self, props):
            self.props: xlsx.XLSXProperties = props

        def sourceApply(self, spark: SparkSession) -> DataFrame:
            if self.props.libraryType == "crealytics":
                reader = spark.read.format("excel").option("header", self.props.header)

                if self.props.schema is not None and self.props.useSchema:
                    reader = reader.schema(self.props.schema)
                if self.props.dataAddress is not None:
                    reader = reader.option("dataAddress", self.props.dataAddress)
                if self.props.fileExtension is not None:
                    reader = reader.option("fileExtension", self.props.fileExtension)
                if self.props.ignoreLeadingWhiteSpace is not None:
                    reader = reader.option("ignoreLeadingWhiteSpace", self.props.ignoreLeadingWhiteSpace)
                if self.props.ignoreTrailingWhiteSpace is not None:
                    reader = reader.option("ignoreTrailingWhiteSpace", self.props.ignoreTrailingWhiteSpace)
                if self.props.inferSchema is not None:
                    reader = reader.option("inferSchema", self.props.inferSchema)
                if self.props.keepUndefinedRows is not None:
                    reader = reader.option("keepUndefinedRows", self.props.keepUndefinedRows)
                if self.props.parseMode is not None:
                    reader = reader.option("parseMode", self.props.parseMode)
                if self.props.useNullForErrorCells is not None:
                    reader = reader.option("useNullForErrorCells", self.props.useNullForErrorCells)
                if self.props.columnNameOfCorruptRecord is not None:
                    reader = reader.option("columnNameOfCorruptRecord", self.props.columnNameOfCorruptRecord)
                if self.props.columnNameOfRowNumber is not None:
                    reader = reader.option("columnNameOfRowNumber", self.props.columnNameOfRowNumber)
                if self.props.dateFormat is not None:
                    reader = reader.option("dateFormat", self.props.dateFormat)
                if self.props.excerptSize is not None:
                    reader = reader.option("excerptSize", self.props.excerptSize)
                if self.props.ignoreAfterHeader is not None:
                    reader = reader.option("ignoreAfterHeader", self.props.ignoreAfterHeader)
                if self.props.locale is not None:
                    reader = reader.option("locale", self.props.locale)
                if self.props.nanValue is not None:
                    reader = reader.option("nanValue", self.props.nanValue)
                if self.props.nullValue is not None:
                    reader = reader.option("nullValue", self.props.nullValue)
                if self.props.positiveInf is not None:
                    reader = reader.option("positiveInf", self.props.positiveInf)
                if self.props.samplingRatio is not None:
                    reader = reader.option("samplingRatio", self.props.samplingRatio)
                if self.props.timestampFormat is not None:
                    reader = reader.option("timestampFormat", self.props.timestampFormat)
                if self.props.workbookPassword is not None:
                    reader = reader.option("workbookPassword", self.props.workbookPassword)
                if self.props.zoneId is not None:
                    reader = reader.option("zoneId", self.props.zoneId)
                if self.props.tempFileThreshold is not None:
                    reader = reader.option("tempFileThreshold", self.props.tempFileThreshold)
                if self.props.maxRowsInMemory is not None:
                    reader = reader.option("maxRowsInMemory", self.props.maxRowsInMemory)
                if self.props.maxByteArraySize is not None:
                    reader = reader.option("maxByteArraySize", self.props.maxByteArraySize)

                return reader.load(self.props.path)
            else:
                import pandas as pd               
             
                kwargs: SubstituteDisabled = {}
                
                if not self.props.header:
                    kwargs["header"] = None
                if self.props.pandasExcelDataAddress is not None and self.props.pandasExcelDataAddress != "":
                    kwargs["usecols"] = self.props.pandasExcelDataAddress
                if self.props.skipRows is not None and self.props.skipRows != "":
                    kwargs["skiprows"] = int(self.props.skipRows)
                if self.props.sheetName is not None and self.props.sheetName != "":
                    kwargs["sheet_name"] = self.props.sheetName
                if self.props.trueValues:
                    kwargs["true_values"] = self.props.trueValues
                if self.props.falseValues:
                    kwargs["false_values"] = self.props.falseValues
                if self.props.nRows is not None and self.props.nRows != "":
                    kwargs["nrows"] = int(self.props.nRows)
                if self.props.naValues:
                    kwargs["na_values"] = self.props.naValues
                if self.props.keepDefaultNAValues is not None:
                    kwargs["keep_default_na"] = self.props.keepDefaultNAValues
                if self.props.naFilter is not None:
                    kwargs["na_filter"] = self.props.naFilter
                if self.props.skipFooter is not None and self.props.skipFooter != "":
                    kwargs["skipfooter"] = int(self.props.skipFooter)
                if self.props.charForThousands is not None and self.props.charForThousands != "":
                    kwargs["thousands"] = self.props.charForThousands
                if self.props.charForDecimal is not None and self.props.charForDecimal != "":
                    kwargs["decimal"] = self.props.charForDecimal
                if self.props.charForComment is not None and self.props.charForComment != "":
                    kwargs["comment"] = self.props.charForComment
                
                pandasDf: SubstituteDisabled = pd.read_excel(self.props.path, **kwargs)
                if self.props.useSchema and self.props.schema is not None:
                    spark_df = spark.createDataFrame(pandasDf, schema=self.props.schema)
                else:
                    spark_df = spark.createDataFrame(pandasDf)
                
                return spark_df

        def targetApply(self, spark: SparkSession, in0: DataFrame):

            if self.props.libraryType == "crealytics":
                if self.props.createSingleOutputFile is not None and self.props.createSingleOutputFile:
                    writer = in0.coalesce(1).write.format("excel").option("header", self.props.header)
                else:
                    writer = in0.write.format("excel").option("header", self.props.header)

                if self.props.dataAddress is not None:
                    writer = writer.option("dataAddress", self.props.dataAddress)
                if self.props.fileExtension is not None:
                    writer = writer.option("fileExtension", self.props.fileExtension)
                if self.props.locale is not None:
                    writer = writer.option("locale", self.props.locale)
                if self.props.dateFormat is not None:
                    writer = writer.option("dateFormat", self.props.dateFormat)
                if self.props.usePlainNumberFormat is not None:
                    writer = writer.option("usePlainNumberFormat", self.props.usePlainNumberFormat)
                if self.props.workbookPassword is not None:
                    writer = writer.option("workbookPassword", self.props.workbookPassword)
                if self.props.writeMode is not None:
                    writer = writer.mode(self.props.writeMode)

                if self.props.partitionColumns is not None and len(self.props.partitionColumns) > 0:
                    writer = writer.partitionBy(*self.props.partitionColumns)

                if self.props.createSingleOutputFile is not None and self.props.createSingleOutputFile:
                    writer.save(self.props.path + "_temp")
                else:
                    writer.save(self.props.path)

                if self.props.createSingleOutputFile is not None:
                    if self.props.createSingleOutputFile:
                        from prophecy.utils.gems_utils import concatenateFiles
                        concatenateFiles(spark, ".xlsx", self.props.writeMode, self.props.path + "_temp", self.props.path,
                                        True, True)
            else:
                import pandas as pd
                import os
                import shutil              
             
                kwargs: SubstituteDisabled = {} 
                if self.props.sheetName is not None and self.props.sheetName != "":
                    kwargs["sheet_name"] = self.props.sheetName
                if self.props.naRep is not None and self.props.naRep != "":
                    kwargs["na_rep"] = self.props.naRep
                if self.props.floatFormat is not None and self.props.floatFormat != "":
                    kwargs["float_format"] = self.props.floatFormat
                if self.props.header:
                    kwargs["header"] = True
                else:
                    kwargs["header"] = False
                if self.props.index:
                    kwargs["index"] = True
                else:
                    kwargs["index"] = False
                if self.props.indexLable is not None and self.props.indexLable != "":
                    kwargs["index_label"] = self.props.indexLable
                if self.props.startRow is not None and self.props.startRow != "":
                    kwargs["startrow"] = int(self.props.startRow)
                if self.props.startColumn is not None and self.props.startColumn != "":
                    kwargs["startcol"] = int(self.props.startColumn)
                
                fileName: SubstituteDisabled = self.props.path.split("/")[-1]
                localPath: SubstituteDisabled = "/tmp/"+fileName
                pandas_df: SubstituteDisabled = in0.toPandas()
                writePath = self.props.path
                
                if os.path.exists(writePath):
                    shutil.copy(writePath, localPath)
                    if self.props.pandasWriteMode == "append":
                        with pd.ExcelWriter(localPath, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                            try:
                                target_sheet = kwargs["sheet_name"] if "sheet_name" in kwargs.keys() else "Sheet1"
                                existing_data_rows = pd.read_excel(localPath, sheet_name=target_sheet,usecols=[0]).shape[0]
                                kwargs["index"] = False
                                kwargs["startrow"] = existing_data_rows + 1
                                kwargs["header"] = False
                                pandas_df.to_excel(writer, **kwargs)
                            except ValueError:
                                pandas_df.to_excel(writer, **kwargs)
                    elif self.props.pandasWriteMode == "overwrite":
                        with pd.ExcelWriter(localPath, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
                            pandas_df.to_excel(writer, **kwargs)
                else:
                    pandas_df.to_excel(localPath, **kwargs)
                
                shutil.copy(localPath, writePath)
                
                if os.path.exists(localPath):
                    os.remove(localPath)
        
    def __init__(self):
        super().__init__()
        self.registerPropertyEvolution(XLSXPropertyMigration())
                    
class XLSXPropertyMigration(PropertyMigrationObj):

    def migrationNumber(self) -> int:
        return 1

    def up(self, old_properties: xlsx.XLSXProperties) -> xlsx.XLSXProperties:
        return dataclasses.replace(
            old_properties,
            libraryType="crealytics"
        )

    def down(self, new_properties: xlsx.XLSXProperties) -> xlsx.XLSXProperties:
        raise Exception("Downgrade is not implemented for this XLSX version")