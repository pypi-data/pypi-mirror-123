Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const getVariantStyle = ({ variant = 'small', theme, }) => {
    if (variant === 'large') {
        return `
      height: 24px;
      border-radius: 24px;
      border: 1px solid ${theme.border};
      box-shadow: inset 0px 1px 3px rgba(0, 0, 0, 0.06);
      :before {
        left: 6px;
        right: 6px;
        height: 14px;
        top: calc(50% - 14px/2);
        border-radius: 20px;
        max-width: calc(100% - 12px);
      }
    `;
    }
    return `
    height: 6px;
    border-radius: 100px;
    background: ${theme.progressBackground};
    :before {
      top: 0;
      left: 0;
      height: 100%;
    }
  `;
};
const ProgressBar = (0, styled_1.default)(({ className, value }) => (<div role="progressbar" aria-valuenow={value} aria-valuemin={0} aria-valuemax={100} className={className}/>)) `
  width: 100%;
  overflow: hidden;
  position: relative;
  :before {
    content: ' ';
    width: ${p => p.value}%;
    background-color: ${p => p.theme.progressBar};
    position: absolute;
  }

  ${getVariantStyle};
`;
exports.default = ProgressBar;
//# sourceMappingURL=progressBar.jsx.map