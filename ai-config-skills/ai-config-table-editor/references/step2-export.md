# 第 2 步：由表格生成 JSON

## 目录与工具

按项目实际替换以下占位目录：

- 配置源目录：`$CONFIG_XLSX_DIR`（维护各 xlsx）
- 导出暂存区：`$EXPORT_STAGING_DIR`（把修改后的 xlsx 复制到这里，同名直接覆盖）
- 导出器目录：`$EXPORT_GEN_DIR`（包含导出工具，例如 `ExcelToConfConsole.jar` + 配置文件）
- JSON 输出：服务端 JSON 目录（上传 Apollo 用这份），如有 client 副本目录则另行约定

运行环境：按导出工具要求（例如 Java 8）。

## 表格命名与结构规范

- 文件名不影响产物；**第一个 sheet 名决定产物**。sheet 名格式为 `中文|English`（如 `商城|Shop`），产物为 `Conf{English}.json`（如 `ConfShop.json`）。
- 表头固定 4 行，第 5 行起为数据：
  1. 类型标记（如 `cs`）
  2. 字段类型（`int`、`String`、`long` 等）
  3. 中文注释/说明
  4. 字段名（与 JSON 字段一一对应）

## 执行流程

1. 在 `$CONFIG_XLSX_DIR` 修改对应 xlsx，保存并关闭 Excel（文件被占用时复制会失败）。
2. 复制到暂存区：

   ```powershell
   Copy-Item <源表> $EXPORT_STAGING_DIR -Force
   ```

3. 运行导出器（直接调用工具，不要使用带 `pause` 的批处理，会卡住自动化）：

   ```powershell
   cd $EXPORT_GEN_DIR
   java -jar ExcelToConfConsole.jar
   ```

4. 检查生成的 `Conf*.json` 与服务端 JSON 目录；上传 Apollo 用服务端 JSON。

## 注意

- 工具通常会处理暂存区内**所有** xlsx：放入新表会连带重新生成其它 `Conf*.json`（输入未变则内容不变）。
- 运行时若提示缺少 client 子目录等可选目录，不影响服务端产物时可忽略（按工具实际情况处理）。
