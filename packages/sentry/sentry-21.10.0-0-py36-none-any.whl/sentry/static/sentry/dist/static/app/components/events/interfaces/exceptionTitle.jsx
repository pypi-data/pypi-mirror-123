Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const ExceptionTitle = ({ type, exceptionModule }) => {
    if ((0, utils_1.defined)(exceptionModule)) {
        return (<tooltip_1.default title={(0, locale_1.tct)('from [exceptionModule]', { exceptionModule })}>
        <Title>{type}</Title>
      </tooltip_1.default>);
    }
    return <Title>{type}</Title>;
};
exports.default = ExceptionTitle;
const Title = (0, styled_1.default)('h5') `
  margin-bottom: ${(0, space_1.default)(0.5)};
  overflow-wrap: break-word;
  word-wrap: break-word;
  word-break: break-word;
`;
//# sourceMappingURL=exceptionTitle.jsx.map