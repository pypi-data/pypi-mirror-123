Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const keyValueList_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/keyValueList"));
const getTransformedData_1 = (0, tslib_1.__importDefault)(require("./getTransformedData"));
const RichHttpContentClippedBoxKeyValueList = ({ data, title, defaultCollapsed = false, isContextData = false, meta, }) => {
    const getContent = (transformedData) => {
        // Sentry API abbreviates long query string values, sometimes resulting in
        // an un-parsable querystring ... stay safe kids
        try {
            return (<keyValueList_1.default data={transformedData.map(([key, value]) => ({
                    key,
                    subject: key,
                    value,
                    meta,
                }))} isContextData={isContextData}/>);
        }
        catch (_a) {
            return <pre>{data}</pre>;
        }
    };
    const transformedData = (0, getTransformedData_1.default)(data);
    if (!transformedData.length) {
        return null;
    }
    return (<clippedBox_1.default title={title} defaultClipped={defaultCollapsed}>
      <errorBoundary_1.default mini>{getContent(transformedData)}</errorBoundary_1.default>
    </clippedBox_1.default>);
};
exports.default = RichHttpContentClippedBoxKeyValueList;
//# sourceMappingURL=richHttpContentClippedBoxKeyValueList.jsx.map