Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const contextSummaryNoSummary_1 = (0, tslib_1.__importDefault)(require("./contextSummaryNoSummary"));
const generateClassName_1 = (0, tslib_1.__importDefault)(require("./generateClassName"));
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const ContextSummaryGeneric = ({ data, unknownTitle }) => {
    if (Object.keys(data).length === 0) {
        return <contextSummaryNoSummary_1.default title={unknownTitle}/>;
    }
    const renderValue = (key) => {
        const meta = (0, metaProxy_1.getMeta)(data, key);
        return <annotatedText_1.default value={data[key]} meta={meta}/>;
    };
    const className = (0, generateClassName_1.default)(data.name, data.version);
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderValue('name')}</h3>
      <textOverflow_1.default isParagraph>
        <Subject>{(0, locale_1.t)('Version:')}</Subject>
        {!data.version ? (0, locale_1.t)('Unknown') : renderValue('version')}
      </textOverflow_1.default>
    </item_1.default>);
};
exports.default = ContextSummaryGeneric;
const Subject = (0, styled_1.default)('strong') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=contextSummaryGeneric.jsx.map