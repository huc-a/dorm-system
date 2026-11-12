<template><router-view /></template>
<style>
:root {
  --el-color-primary: #2f7de1;
  --el-color-primary-light-3: #6aa9ec;
  --el-color-primary-light-5: #9cc4f4;
  --el-color-primary-light-7: #c3dbf9;
  --el-color-primary-light-9: #eaf3fd;
  --el-color-primary-dark-2: #2564b4;
  --el-border-radius-base: 8px;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  background: #eef2f7;
  color: #303133;
  -webkit-font-smoothing: antialiased;
}
/* 卡片：圆角 + 柔和阴影 + 悬停浮起 */
.el-card {
  border: none !important;
  border-radius: 14px !important;
  box-shadow: 0 2px 12px rgba(31, 68, 120, 0.06) !important;
  transition: box-shadow .25s ease, transform .25s ease;
}
.el-card.is-hover-shadow:hover {
  box-shadow: 0 10px 28px rgba(31, 68, 120, 0.14) !important;
  transform: translateY(-3px);
}
.el-card__header { border-bottom: 1px solid #eef2f7 !important; font-weight: 600; }
/* 表格：表头浅蓝底、行悬停高亮、圆角外框 */
.el-table { border-radius: 10px; overflow: hidden; }
.el-table th.el-table__cell {
  background: linear-gradient(180deg, #f2f7fd, #e8f1fb) !important;
  color: #33506e; font-weight: 600;
}
.el-table .el-table__row:hover > td.el-table__cell { background: #f2f8ff !important; }
/* 按钮与输入 */
.el-button { border-radius: 8px !important; font-weight: 500; }
.el-button--primary:not(.is-plain) {
  background: linear-gradient(135deg, #3a8dde, #2f7de1) !important;
  border-color: transparent !important;
  box-shadow: 0 4px 12px rgba(47, 125, 225, 0.28);
}
.el-button--primary:not(.is-plain):hover { filter: brightness(1.07); }
.el-button--primary.is-plain {
  background: #eaf3fd !important; color: #2f7de1 !important; border-color: #bcd8f8 !important; box-shadow: none;
}
.el-button--primary.is-plain:hover { background: #d9ebfc !important; }
.el-input__wrapper, .el-select__wrapper { border-radius: 8px !important; }
/* 对话框与分页 */
.el-dialog { border-radius: 16px !important; overflow: hidden; }
.el-dialog__header { background: linear-gradient(90deg, #f2f7fd, #ffffff); margin-right: 0 !important; padding: 18px 24px !important; }
.el-dialog__body { padding: 22px 24px 8px !important; }
.el-pagination .el-pager li { border-radius: 6px; }
.el-pagination .el-pager li.is-active { background: linear-gradient(135deg, #3a8dde, #2f7de1); }
/* 侧栏菜单：胶囊式选中态 */
.el-menu { padding: 8px 10px; }
.el-menu .el-menu-item { border-radius: 10px; margin: 3px 0; height: 46px; line-height: 46px; }
.el-menu .el-menu-item:hover { background: rgba(255, 255, 255, 0.08) !important; color: #fff !important; }
.el-menu .el-menu-item.is-active {
  background: linear-gradient(90deg, #2f7de1, #4a97e8) !important;
  color: #fff !important;
  box-shadow: 0 4px 12px rgba(47, 125, 225, 0.35);
}
/* 滚动条 */
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-thumb { background: #c3cedb; border-radius: 6px; }
::-webkit-scrollbar-thumb:hover { background: #a7b7ca; }
::-webkit-scrollbar-track { background: transparent; }
.el-main { padding: 20px 22px !important; }
.el-tag { border-radius: 6px; font-weight: 500; }
</style>
