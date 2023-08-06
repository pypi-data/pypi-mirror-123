Object.defineProperty(exports, "__esModule", { value: true });
exports.TreeToggleIcon = exports.TreeToggleContainer = exports.TreeToggle = exports.TreeConnector = exports.ConnectorBar = exports.TOGGLE_BORDER_BOX = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const constants_1 = require("app/components/performance/waterfall/constants");
const utils_1 = require("app/components/performance/waterfall/utils");
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const TOGGLE_BUTTON_MARGIN_RIGHT = 16;
const TOGGLE_BUTTON_MAX_WIDTH = 30;
exports.TOGGLE_BORDER_BOX = TOGGLE_BUTTON_MAX_WIDTH + TOGGLE_BUTTON_MARGIN_RIGHT;
const TREE_TOGGLE_CONTAINER_WIDTH = 40;
exports.ConnectorBar = (0, styled_1.default)('div') `
  height: 250%;

  border-left: 1px ${p => (p.orphanBranch ? 'dashed' : 'solid')} ${p => p.theme.border};
  top: -5px;
  position: absolute;
`;
exports.TreeConnector = (0, styled_1.default)('div') `
  height: ${p => (p.isLast ? constants_1.ROW_HEIGHT / 2 : constants_1.ROW_HEIGHT)}px;
  width: 100%;
  border-left: ${p => {
    return `1px ${p.orphanBranch ? 'dashed' : 'solid'} ${p.theme.border}`;
}};
  position: absolute;
  top: 0;

  &:before {
    content: '';
    height: 1px;
    border-bottom: ${p => `1px ${p.orphanBranch ? 'dashed' : 'solid'} ${p.theme.border};`};
    left: 0;
    width: 100%;
    position: absolute;
    bottom: ${p => (p.isLast ? '0' : '50%')};
  }

  &:after {
    content: '';
    background-color: ${p => p.theme.border};
    border-radius: 4px;
    height: 3px;
    width: 3px;
    position: absolute;
    right: 0;
    top: ${constants_1.ROW_HEIGHT / 2 - 2}px;
  }
`;
exports.TreeToggle = (0, styled_1.default)('div') `
  height: 16px;
  white-space: nowrap;
  min-width: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 99px;
  padding: 0px ${(0, space_1.default)(0.5)};
  transition: all 0.15s ease-in-out;
  font-size: 10px;
  line-height: 0;
  z-index: 1;

  ${p => (0, utils_1.getToggleTheme)(p)}
`;
exports.TreeToggleContainer = (0, styled_1.default)('div') `
  position: relative;
  height: ${constants_1.ROW_HEIGHT}px;
  width: ${TREE_TOGGLE_CONTAINER_WIDTH}px;
  min-width: ${TREE_TOGGLE_CONTAINER_WIDTH}px;
  margin-right: ${(0, space_1.default)(1)};
  z-index: ${p => p.theme.zIndex.traceView.spanTreeToggler};
  display: flex;
  justify-content: flex-end;
  align-items: center;
`;
exports.TreeToggleIcon = (0, styled_1.default)(icons_1.IconChevron) `
  width: 7px;
  margin-left: ${(0, space_1.default)(0.25)};
`;
//# sourceMappingURL=treeConnector.jsx.map