Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const tag_1 = (0, tslib_1.__importStar)(require("app/components/tag"));
const locale_1 = require("app/locale");
const breadcrumbs_1 = require("app/types/breadcrumbs");
const Level = (0, react_1.memo)(function Level({ level, searchTerm = '' }) {
    switch (level) {
        case breadcrumbs_1.BreadcrumbLevelType.FATAL:
            return (<LevelTag type="error">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('Fatal')}</highlight_1.default>
        </LevelTag>);
        case breadcrumbs_1.BreadcrumbLevelType.ERROR:
            return (<LevelTag type="error">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('Error')}</highlight_1.default>
        </LevelTag>);
        case breadcrumbs_1.BreadcrumbLevelType.INFO:
            return (<LevelTag type="info">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('Info')}</highlight_1.default>
        </LevelTag>);
        case breadcrumbs_1.BreadcrumbLevelType.WARNING:
            return (<LevelTag type="warning">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('Warning')}</highlight_1.default>
        </LevelTag>);
        default:
            return (<LevelTag>
          <highlight_1.default text={searchTerm}>{level || (0, locale_1.t)('Undefined')}</highlight_1.default>
        </LevelTag>);
    }
});
exports.default = Level;
const LevelTag = (0, styled_1.default)(tag_1.default) `
  height: 24px;
  display: flex;
  align-items: center;
  ${tag_1.Background} {
    overflow: hidden;
  }
`;
//# sourceMappingURL=level.jsx.map