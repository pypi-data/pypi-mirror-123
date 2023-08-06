Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_autosize_textarea_1 = (0, tslib_1.__importDefault)(require("react-autosize-textarea"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const input_1 = require("app/styles/input");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const TextAreaControl = React.forwardRef(function TextAreaControl(_a, ref) {
    var { autosize, rows, maxRows } = _a, p = (0, tslib_1.__rest)(_a, ["autosize", "rows", "maxRows"]);
    return autosize ? (<react_autosize_textarea_1.default {...p} async ref={ref} rows={rows ? rows : 2} maxRows={maxRows}/>) : (<textarea ref={ref} {...p}/>);
});
TextAreaControl.displayName = 'TextAreaControl';
const propFilter = (p) => ['autosize', 'rows', 'maxRows'].includes(p) || (0, is_prop_valid_1.default)(p);
const TextArea = (0, styled_1.default)(TextAreaControl, { shouldForwardProp: propFilter }) `
  ${input_1.inputStyles};
  min-height: 40px;
  padding: calc(${(0, space_1.default)(1)} - 1px) ${(0, space_1.default)(1)};
  line-height: 1.5em;
  ${p => p.autosize &&
    `
      height: auto;
      padding: calc(${(0, space_1.default)(1)} - 2px) ${(0, space_1.default)(1)};
      line-height: 1.6em;
    `}
`;
exports.default = TextArea;
//# sourceMappingURL=textarea.jsx.map