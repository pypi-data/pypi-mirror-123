Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const defaultProps = {
    shape: 'rect',
    bottomGutter: 0,
    width: '100%',
    height: '60px',
    testId: 'loading-placeholder',
};
const Placeholder = (0, styled_1.default)(({ className, children, error, testId }) => {
    return (<div data-test-id={testId} className={className}>
      {error || children}
    </div>);
}) `
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  justify-content: center;
  align-items: center;

  background-color: ${p => (p.error ? p.theme.red100 : p.theme.backgroundSecondary)};
  ${p => p.error && `color: ${p.theme.red200};`}
  width: ${p => p.width};
  height: ${p => p.height};
  ${p => (p.shape === 'circle' ? 'border-radius: 100%;' : '')}
  ${p => typeof p.bottomGutter === 'number' && p.bottomGutter > 0
    ? `margin-bottom: ${(0, space_1.default)(p.bottomGutter)};`
    : ''}
`;
Placeholder.defaultProps = defaultProps;
exports.default = Placeholder;
//# sourceMappingURL=placeholder.jsx.map