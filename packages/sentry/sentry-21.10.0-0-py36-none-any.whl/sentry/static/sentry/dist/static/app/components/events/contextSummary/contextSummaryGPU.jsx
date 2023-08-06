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
const ContextSummaryGPU = ({ data }) => {
    if (Object.keys(data).length === 0 || !data.name) {
        return <contextSummaryNoSummary_1.default title={(0, locale_1.t)('Unknown GPU')}/>;
    }
    const renderName = () => {
        const meta = (0, metaProxy_1.getMeta)(data, 'name');
        return <annotatedText_1.default value={data.name} meta={meta}/>;
    };
    let className = (0, generateClassName_1.default)(data.name);
    const getVersionElement = () => {
        if (data.vendor_name) {
            className = (0, generateClassName_1.default)(data.vendor_name);
            return {
                subject: (0, locale_1.t)('Vendor:'),
                value: data.vendor_name,
                meta: (0, metaProxy_1.getMeta)(data, 'vendor_name'),
            };
        }
        return {
            subject: (0, locale_1.t)('Vendor:'),
            value: (0, locale_1.t)('Unknown'),
        };
    };
    const versionElement = getVersionElement();
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      <textOverflow_1.default isParagraph>
        <Subject>{versionElement.subject}</Subject>
        <annotatedText_1.default value={versionElement.value} meta={versionElement.meta}/>
      </textOverflow_1.default>
    </item_1.default>);
};
exports.default = ContextSummaryGPU;
const Subject = (0, styled_1.default)('strong') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=contextSummaryGPU.jsx.map