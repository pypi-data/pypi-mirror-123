Object.defineProperty(exports, "__esModule", { value: true });
exports.TagAndMessageWrapper = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function UnhandledTag() {
    return (<TagWrapper>
      <tooltip_1.default title={(0, locale_1.t)('An unhandled error was detected in this Issue.')}>
        <tag_1.default type="error">{(0, locale_1.t)('Unhandled')}</tag_1.default>
      </tooltip_1.default>
    </TagWrapper>);
}
const TagWrapper = (0, styled_1.default)('div') `
  margin-right: ${(0, space_1.default)(1)};
`;
const TagAndMessageWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
exports.TagAndMessageWrapper = TagAndMessageWrapper;
exports.default = UnhandledTag;
//# sourceMappingURL=unhandledTag.jsx.map