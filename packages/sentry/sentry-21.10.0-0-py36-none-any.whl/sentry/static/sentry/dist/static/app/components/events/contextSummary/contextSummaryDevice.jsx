Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const deviceName_1 = (0, tslib_1.__importDefault)(require("app/components/deviceName"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const contextSummaryNoSummary_1 = (0, tslib_1.__importDefault)(require("./contextSummaryNoSummary"));
const generateClassName_1 = (0, tslib_1.__importDefault)(require("./generateClassName"));
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const ContextSummaryDevice = ({ data }) => {
    if (Object.keys(data).length === 0) {
        return <contextSummaryNoSummary_1.default title={(0, locale_1.t)('Unknown Device')}/>;
    }
    const renderName = () => {
        if (!data.model) {
            return (0, locale_1.t)('Unknown Device');
        }
        const meta = (0, metaProxy_1.getMeta)(data, 'model');
        return (<deviceName_1.default value={data.model}>
        {deviceName => {
                return <annotatedText_1.default value={deviceName} meta={meta}/>;
            }}
      </deviceName_1.default>);
    };
    const getSubTitle = () => {
        if (data.arch) {
            return {
                subject: (0, locale_1.t)('Arch:'),
                value: data.arch,
                meta: (0, metaProxy_1.getMeta)(data, 'arch'),
            };
        }
        if (data.model_id) {
            return {
                subject: (0, locale_1.t)('Model:'),
                value: data.model_id,
                meta: (0, metaProxy_1.getMeta)(data, 'model_id'),
            };
        }
        return null;
    };
    // TODO(dcramer): we need a better way to parse it
    const className = (0, generateClassName_1.default)(data.model);
    const subTitle = getSubTitle();
    return (<item_1.default className={className} icon={<span className="context-item-icon"/>}>
      <h3>{renderName()}</h3>
      {subTitle && (<textOverflow_1.default isParagraph data-test-id="context-sub-title">
          <Subject>{subTitle.subject}</Subject>
          <annotatedText_1.default value={subTitle.value} meta={subTitle.meta}/>
        </textOverflow_1.default>)}
    </item_1.default>);
};
exports.default = ContextSummaryDevice;
const Subject = (0, styled_1.default)('strong') `
  margin-right: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=contextSummaryDevice.jsx.map