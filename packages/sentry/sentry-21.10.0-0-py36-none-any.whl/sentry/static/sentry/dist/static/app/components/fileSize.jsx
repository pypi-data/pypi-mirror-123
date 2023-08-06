Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const utils_1 = require("app/utils");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
function FileSize(props) {
    const { className, bytes } = props;
    return (<Span className={className}>
      {(0, getDynamicText_1.default)({ value: (0, utils_1.formatBytesBase2)(bytes), fixed: 'xx KB' })}
    </Span>);
}
const Span = (0, styled_1.default)('span') `
  font-variant-numeric: tabular-nums;
`;
exports.default = FileSize;
//# sourceMappingURL=fileSize.jsx.map