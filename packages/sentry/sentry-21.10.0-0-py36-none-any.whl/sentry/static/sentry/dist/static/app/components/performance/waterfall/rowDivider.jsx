Object.defineProperty(exports, "__esModule", { value: true });
exports.EmbeddedTransactionBadge = exports.ErrorBadge = exports.DividerLineGhostContainer = exports.DividerLine = exports.DividerContainer = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.DividerContainer = (0, styled_1.default)('div') `
  position: relative;
  min-width: 1px;
`;
exports.DividerLine = (0, styled_1.default)('div') `
  background-color: ${p => (p.showDetail ? p.theme.textColor : p.theme.border)};
  position: absolute;
  height: 100%;
  width: 1px;
  transition: background-color 125ms ease-in-out;
  z-index: ${p => p.theme.zIndex.traceView.dividerLine};

  /* enhanced hit-box */
  &:after {
    content: '';
    z-index: -1;
    position: absolute;
    left: -2px;
    top: 0;
    width: 5px;
    height: 100%;
  }

  &.hovering {
    background-color: ${p => p.theme.textColor};
    width: 3px;
    transform: translateX(-1px);
    margin-right: -2px;

    cursor: ew-resize;

    &:after {
      left: -2px;
      width: 7px;
    }
  }
`;
exports.DividerLineGhostContainer = (0, styled_1.default)('div') `
  position: absolute;
  width: 100%;
  height: 100%;
`;
const BadgeBorder = (0, styled_1.default)('div') `
  position: absolute;
  margin: ${(0, space_1.default)(0.25)};
  left: -11px;
  background: ${p => p.theme.background};
  width: ${(0, space_1.default)(3)};
  height: ${(0, space_1.default)(3)};
  border: 1px solid ${p => p.theme[p.borderColor]};
  border-radius: 50%;
  z-index: ${p => p.theme.zIndex.traceView.dividerLine};
  display: flex;
  align-items: center;
  justify-content: center;
`;
function ErrorBadge() {
    return (<BadgeBorder borderColor="red300">
      <icons_1.IconFire color="red300" size="xs"/>
    </BadgeBorder>);
}
exports.ErrorBadge = ErrorBadge;
function EmbeddedTransactionBadge({ expanded, onClick, }) {
    return (<BadgeBorder borderColor="border" onClick={event => {
            event.stopPropagation();
            event.preventDefault();
            onClick();
        }}>
      {expanded ? (<icons_1.IconSubtract color="textColor" size="xs"/>) : (<icons_1.IconAdd color="textColor" size="xs"/>)}
    </BadgeBorder>);
}
exports.EmbeddedTransactionBadge = EmbeddedTransactionBadge;
//# sourceMappingURL=rowDivider.jsx.map