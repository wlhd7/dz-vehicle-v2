# 实施计划: 增强 CLI 批量导入工具的健壮性

## Phase 1: 准备与基础验证
- [ ] Task: 建立导入数据的 Pydantic 模型
    - [ ] 定义 `WhitelistUserImport` 模型（含字段校验）。
    - [ ] 定义 `AssetImport` 模型。
- [ ] Task: 为导入逻辑编写测试用例 (TDD)
    - [ ] 编写针对非法数据的失败测试。
    - [ ] 编写针对重复数据的失败测试。

## Phase 2: 逻辑实现
- [ ] Task: 集成验证逻辑到 CLI 命令
    - [ ] 修改 `vehicle-asset` 中的导入逻辑，使用模型进行实例化检查。
    - [ ] 实现重复数据检测逻辑。
- [ ] Task: 优化错误报告输出
    - [ ] 捕获验证异常并转换为带行号的友好提示。

## Phase 3: 验证与交付
- [ ] Task: 运行所有测试并验证修复
    - [ ] 确保 `pytest` 所有测试通过。
- [ ] Task: Conductor - User Manual Verification '验证与交付' (Protocol in workflow.md)
