Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const contextData_1 = (0, tslib_1.__importDefault)(require("app/components/contextData"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const getTransformedData_1 = (0, tslib_1.__importDefault)(require("./getTransformedData"));
function RichHttpContentClippedBoxBodySection({ data, meta, inferredContentType }) {
    if (!(0, utils_1.defined)(data)) {
        return null;
    }
    function getContent() {
        switch (inferredContentType) {
            case 'application/json':
                return (<contextData_1.default data-test-id="rich-http-content-body-context-data" data={data} preserveQuotes/>);
            case 'application/x-www-form-urlencoded':
            case 'multipart/form-data': {
                const transformedData = (0, getTransformedData_1.default)(data).map(([key, v]) => ({
                    key,
                    subject: key,
                    value: v,
                    meta,
                }));
                if (!transformedData.length) {
                    return null;
                }
                return (<keyValueList_1.default data-test-id="rich-http-content-body-key-value-list" data={transformedData} isContextData/>);
            }
            default:
                return (<pre data-test-id="rich-http-content-body-section-pre">
            <annotatedText_1.default value={data && JSON.stringify(data, null, 2)} meta={meta} data-test-id="rich-http-content-body-context-data"/>
          </pre>);
        }
    }
    const content = getContent();
    if (!content) {
        return null;
    }
    return (<clippedBox_1.default title={(0, locale_1.t)('Body')} defaultClipped>
      <errorBoundary_1.default mini>{content}</errorBoundary_1.default>
    </clippedBox_1.default>);
}
exports.default = RichHttpContentClippedBoxBodySection;
//# sourceMappingURL=richHttpContentClippedBoxBodySection.jsx.map