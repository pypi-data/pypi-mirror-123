Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const inlineStyle = (p) => p.inline
    ? (0, react_1.css) `
        align-items: center;
      `
    : (0, react_1.css) `
        flex-direction: column;
        align-items: stretch;
      `;
const getPadding = (p) => p.stacked && !p.inline
    ? (0, react_1.css) `
        padding: 0 ${p.hasControlState ? 0 : (0, space_1.default)(2)} ${(0, space_1.default)(2)} 0;
      `
    : (0, react_1.css) `
        padding: ${(0, space_1.default)(2)} ${p.hasControlState ? 0 : (0, space_1.default)(2)} ${(0, space_1.default)(2)} ${(0, space_1.default)(2)};
      `;
const FieldWrapper = (0, styled_1.default)('div') `
  ${getPadding}
  ${inlineStyle}
  display: flex;
  transition: background 0.15s;

  ${p => !p.stacked &&
    (0, react_1.css) `
      border-bottom: 1px solid ${p.theme.innerBorder};
    `}

  ${p => p.highlighted &&
    (0, react_1.css) `
      position: relative;

      &:after {
        content: '';
        display: block;
        position: absolute;
        top: -1px;
        left: -1px;
        right: -1px;
        bottom: -1px;
        border: 1px solid ${p.theme.purple300};
        pointer-events: none;
      }
    `}


  /* Better padding with form inside of a modal */
  ${p => !p.hasControlState &&
    (0, react_1.css) `
      [role='document'] & {
        padding-right: 0;
      }
    `}

  &:last-child {
    border-bottom: none;
    ${p => (p.stacked ? 'padding-bottom: 0' : '')};
  }
`;
exports.default = FieldWrapper;
//# sourceMappingURL=fieldWrapper.jsx.map