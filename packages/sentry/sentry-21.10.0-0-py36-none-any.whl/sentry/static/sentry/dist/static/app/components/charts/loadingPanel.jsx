Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const loadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/loadingMask"));
const LoadingPanel = (0, styled_1.default)((_a) => {
    var { height: _height } = _a, props = (0, tslib_1.__rest)(_a, ["height"]);
    return (<div {...props}>
    <loadingMask_1.default />
  </div>);
}) `
  flex: 1;
  flex-shrink: 0;
  overflow: hidden;
  height: ${p => p.height};
  position: relative;
  border-color: transparent;
  margin-bottom: 0;
`;
LoadingPanel.defaultProps = {
    height: '200px',
};
exports.default = LoadingPanel;
//# sourceMappingURL=loadingPanel.jsx.map