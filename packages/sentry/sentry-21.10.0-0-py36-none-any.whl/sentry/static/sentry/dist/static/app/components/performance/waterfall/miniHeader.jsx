Object.defineProperty(exports, "__esModule", { value: true });
exports.VirtualScrollbarGrip = exports.VirtualScrollbar = exports.ScrollbarContainer = exports.DividerSpacer = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
exports.DividerSpacer = (0, styled_1.default)('div') `
  width: 1px;
  background-color: ${p => p.theme.border};
`;
const MINI_HEADER_HEIGHT = 20;
exports.ScrollbarContainer = (0, styled_1.default)('div') `
  display: block;
  width: 100%;
  height: ${MINI_HEADER_HEIGHT + 50}px;
  & > div[data-type='virtual-scrollbar'].dragging > div {
    background-color: ${p => p.theme.textColor};
    opacity: 0.8;
    cursor: grabbing;
  }
  overflow-x: scroll;
`;
exports.VirtualScrollbar = (0, styled_1.default)('div') `
  height: 8px;
  width: 0;
  padding-left: 4px;
  padding-right: 4px;
  position: sticky;
  top: ${(MINI_HEADER_HEIGHT - 8) / 2}px;
  left: 0;
  cursor: grab;
`;
exports.VirtualScrollbarGrip = (0, styled_1.default)('div') `
  height: 8px;
  width: 100%;
  border-radius: 20px;
  transition: background-color 150ms ease;
  background-color: ${p => p.theme.textColor};
  opacity: 0.5;
`;
//# sourceMappingURL=miniHeader.jsx.map