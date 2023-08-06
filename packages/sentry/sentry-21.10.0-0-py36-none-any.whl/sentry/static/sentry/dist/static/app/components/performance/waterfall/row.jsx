Object.defineProperty(exports, "__esModule", { value: true });
exports.RowCell = exports.RowCellContainer = exports.Row = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
const utils_1 = require("app/components/performance/waterfall/utils");
exports.Row = (0, styled_1.default)('div') `
  display: ${p => (p.visible ? 'block' : 'none')};
  border-top: ${p => (p.showBorder ? `1px solid ${p.theme.border}` : null)};
  margin-top: ${p => (p.showBorder ? '-1px' : null)}; /* to prevent offset on toggle */
  position: relative;
  overflow: hidden;
  min-height: ${constants_1.ROW_HEIGHT}px;
  cursor: ${p => { var _a; return (_a = p.cursor) !== null && _a !== void 0 ? _a : 'pointer'; }};
  transition: background-color 0.15s ease-in-out;

  &:last-child {
    & > [data-component='span-detail'] {
      border-bottom: none !important;
    }
  }
`;
exports.RowCellContainer = (0, styled_1.default)('div') `
  display: flex;
  position: relative;
  height: ${constants_1.ROW_HEIGHT}px;

  /* for virtual scrollbar */
  overflow: hidden;

  user-select: none;

  &:hover > div[data-type='span-row-cell'] {
    background-color: ${p => p.showDetail ? p.theme.textColor : p.theme.backgroundSecondary};
  }
`;
exports.RowCell = (0, styled_1.default)('div') `
  position: relative;
  height: 100%;
  overflow: hidden;
  background-color: ${p => (0, utils_1.getBackgroundColor)(p)};
  transition: background-color 125ms ease-in-out;
  color: ${p => (p.showDetail ? p.theme.background : 'inherit')};
`;
//# sourceMappingURL=row.jsx.map